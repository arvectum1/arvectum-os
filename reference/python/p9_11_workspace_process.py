#!/usr/bin/env python3
"""Exact-release Productive Workspace process lifecycle helper.

This owner-local helper is not a daemon or a service manager. It proves that the
loopback Workspace listener belongs to an installed exact release before it is
reported ready or, during a P7.06 transition, gracefully stopped.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen

import p7_06_governed_deploy as p706

PORT = 8769
HOST = "127.0.0.1"
PROCESS_SCHEMA = "arvectum.p9_11.workspace-process/1"
STOP_SCHEMA = "arvectum.p9_11.workspace-stop/1"
MAX_WAIT_SECONDS = 30.0
POLL_SECONDS = 0.25
ASSET_HREF = re.compile(rb'(?:src|href)="/(assets/[A-Za-z0-9_-]+\.(?:js|css))"')

NOT_RUNNING = "NOT_RUNNING"
CURRENT_EXACT = "CURRENT_EXACT"
STALE_KNOWN_EXACT = "STALE_KNOWN_EXACT"
UNKNOWN = "UNKNOWN"


class WorkspaceProcessError(RuntimeError):
    pass


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _current_release(root: Path) -> str:
    return p706.current_release(root)


def _release_paths(root: Path, release: str) -> tuple[Path, Path, Path, Path]:
    release_root = root / "releases" / release
    source = release_root / "source/reference/python"
    return (
        root / "venvs" / release / "bin/python",
        source / "p9_03_workspace.py",
        source,
        source / "workspace_frontend/dist/index.html",
    )


def _command(args: list[str]) -> str:
    try:
        result = subprocess.run(args, check=False, capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise WorkspaceProcessError(f"process inspection command failed: {args[0]}") from exc
    if result.returncode not in {0, 1}:
        raise WorkspaceProcessError(f"process inspection command failed: {args[0]}")
    return result.stdout


def _listener() -> tuple[int, str] | None:
    output = _command(["lsof", "-nP", f"-iTCP:{PORT}", "-sTCP:LISTEN", "-Fpcn"])
    pid: int | None = None
    command = ""
    address = ""
    listeners: list[tuple[int, str, str]] = []
    for line in output.splitlines():
        if not line:
            continue
        field, value = line[0], line[1:]
        if field == "p":
            if pid is not None and address:
                listeners.append((pid, command, address))
            pid = int(value) if value.isdigit() else None
            command = ""
            address = ""
        elif field == "c":
            command = value
        elif field == "n":
            address = value
    if pid is not None and address:
        listeners.append((pid, command, address))
    if not listeners:
        return None
    if len(listeners) != 1 or listeners[0][2] != f"{HOST}:{PORT}":
        raise WorkspaceProcessError("listener is not exactly one IPv4 loopback Workspace socket")
    return listeners[0][0], listeners[0][1]


def _process_cwd(pid: int) -> Path | None:
    output = _command(["lsof", "-n", "-a", "-p", str(pid), "-d", "cwd", "-Fn"])
    for line in output.splitlines():
        if line.startswith("n"):
            return Path(line[1:]).resolve()
    return None


def _process_command(pid: int) -> str:
    return _command(["ps", "-ww", "-p", str(pid), "-o", "command="]).strip()


def _fetch(path: str) -> bytes:
    try:
        with urlopen(f"http://{HOST}:{PORT}{path}", timeout=3) as response:
            if response.status != 200:
                raise WorkspaceProcessError(f"Workspace HTTP returned {response.status}")
            return response.read(4 * 1024 * 1024)
    except (URLError, OSError) as exc:
        raise WorkspaceProcessError("Workspace HTTP is unavailable") from exc


def _live_assets_match(index: Path) -> bool:
    try:
        expected = index.read_bytes()
        live = _fetch("/")
    except (OSError, WorkspaceProcessError):
        return False
    if live != expected:
        return False
    for asset in ASSET_HREF.findall(expected):
        path = index.parent / asset.decode("ascii")
        if not path.is_file() or _fetch("/" + asset.decode("ascii")) != path.read_bytes():
            return False
    return True


def status(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    current = _current_release(root)
    listener = _listener()
    if listener is None:
        return {"state": NOT_RUNNING, "current_release": current}
    pid, listener_command = listener
    command = _process_command(pid)
    cwd = _process_cwd(pid)
    if "p9_03_workspace.py serve" not in command or cwd is None:
        return {"state": UNKNOWN, "current_release": current, "pid": pid, "reason": "listener is not a Workspace serve process"}
    releases = root / "releases"
    try:
        release = cwd.relative_to(releases).parts[0]
        python, entrypoint, source, index = _release_paths(root, release)
        p706.verify_release(root, release, allow_legacy_repository=True)
    except (ValueError, IndexError, OSError, p706.P706Error):
        return {"state": UNKNOWN, "current_release": current, "pid": pid, "reason": "Workspace source is not an admitted exact release"}
    if cwd != source.resolve() or not python.is_file() or not entrypoint.is_file() or not _live_assets_match(index):
        return {"state": UNKNOWN, "current_release": current, "pid": pid, "reason": "Workspace listener does not match its exact release"}
    state = CURRENT_EXACT if release == current else STALE_KNOWN_EXACT
    return {"state": state, "current_release": current, "release_sha": release, "pid": pid, "listener_command": listener_command}


def _require_p702_health(root: Path, release: str) -> None:
    python, _, source, _ = _release_paths(root, release)
    runtime = source / "p7_02_persistent_runtime.py"
    result = subprocess.run(
        [str(python), str(runtime), "check", "--runtime-root", str(root), "--expected-release", release, "--max-age-seconds", "20"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise WorkspaceProcessError("P7.02 exact-current runtime health verification failed")


def _write_process_metadata(root: Path, release: str, pid: int) -> None:
    _, _, _, index = _release_paths(root, release)
    release_payload = json.loads((index.parent.parent.parent / "workspace_app/release.json").read_text(encoding="utf-8"))
    _atomic_json(root / "run/workspace-process.json", {
        "schema": PROCESS_SCHEMA,
        "classification": "non-canonical operational telemetry",
        "pid": pid,
        "release_sha": release,
        "workspace_release": release_payload["release_id"],
        "started_at": _utc_now(),
        "bind": f"{HOST}:{PORT}",
    })


def start(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    before = status(root)
    if before["state"] == CURRENT_EXACT:
        return before
    if before["state"] != NOT_RUNNING:
        raise WorkspaceProcessError(f"Workspace start refused: {before['state']}")
    release = _current_release(root)
    python, entrypoint, source, _ = _release_paths(root, release)
    if not python.is_file() or not entrypoint.is_file():
        raise WorkspaceProcessError("current exact release lacks Workspace process files")
    _require_p702_health(root, release)
    checked = subprocess.run([str(python), str(entrypoint), "check"], cwd=source, check=False, capture_output=True, text=True, timeout=30)
    if checked.returncode != 0:
        raise WorkspaceProcessError("current exact Workspace check failed")
    logs = root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    os.chmod(logs, 0o700)
    stdout = (logs / "workspace.stdout.log").open("w", encoding="utf-8")
    stderr = (logs / "workspace.stderr.log").open("w", encoding="utf-8")
    os.chmod(stdout.name, 0o600)
    os.chmod(stderr.name, 0o600)
    process = subprocess.Popen([str(python), str(entrypoint), "serve"], cwd=source, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, start_new_session=True)
    stdout.close()
    stderr.close()
    deadline = time.monotonic() + MAX_WAIT_SECONDS
    while time.monotonic() < deadline:
        observed = status(root)
        if observed["state"] == CURRENT_EXACT and observed.get("pid") == process.pid:
            _write_process_metadata(root, release, process.pid)
            return observed
        if process.poll() is not None:
            break
        time.sleep(POLL_SECONDS)
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass
    raise WorkspaceProcessError("exact Workspace process did not become ready")


def stop_for_update(root: Path) -> dict[str, Any]:
    root = root.expanduser().resolve()
    before = status(root)
    if before["state"] == NOT_RUNNING:
        return before
    if before["state"] not in {CURRENT_EXACT, STALE_KNOWN_EXACT}:
        raise WorkspaceProcessError("Workspace stop refused: listener is UNKNOWN")
    pid = int(before["pid"])
    revalidated = status(root)
    if revalidated.get("state") != before["state"] or revalidated.get("pid") != pid or revalidated.get("release_sha") != before.get("release_sha"):
        raise WorkspaceProcessError("Workspace stop refused: process identity changed")
    os.kill(pid, signal.SIGTERM)
    deadline = time.monotonic() + MAX_WAIT_SECONDS
    while time.monotonic() < deadline:
        if status(root)["state"] == NOT_RUNNING:
            _atomic_json(root / "run/workspace-last-stop.json", {
                "schema": STOP_SCHEMA,
                "classification": "non-canonical operational telemetry",
                "pid": pid,
                "release_sha": before["release_sha"],
                "stopped_at": _utc_now(),
                "bind": f"{HOST}:{PORT}",
            })
            return {"state": NOT_RUNNING, "stopped_pid": pid, "stopped_release": before["release_sha"]}
        time.sleep(POLL_SECONDS)
    raise WorkspaceProcessError("known Workspace process did not stop gracefully")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arvectum OS exact-release Workspace process helper")
    parser.add_argument("command", choices=("status", "start", "stop-for-update"))
    parser.add_argument("--runtime-root", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        root = Path(args.runtime_root)
        value = status(root) if args.command == "status" else start(root) if args.command == "start" else stop_for_update(root)
    except (WorkspaceProcessError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"P9.11 Workspace process FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

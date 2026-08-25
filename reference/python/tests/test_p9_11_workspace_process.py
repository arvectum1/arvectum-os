import importlib.util
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
SPEC = importlib.util.spec_from_file_location("p9_11_workspace_process", HERE / "p9_11_workspace_process.py")
process = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(process)


class WorkspaceProcessStatusTests(unittest.TestCase):
    def _root(self, current: str, listener: str) -> pathlib.Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = pathlib.Path(temporary.name)
        for release in {current, listener}:
            source = root / "releases" / release / "source/reference/python"
            source.mkdir(parents=True)
            (root / "venvs" / release / "bin").mkdir(parents=True)
            (root / "venvs" / release / "bin/python").touch()
            (source / "p9_03_workspace.py").touch()
            (source / "workspace_frontend/dist").mkdir(parents=True)
            (source / "workspace_frontend/dist/index.html").touch()
            (source / "workspace_app").mkdir()
            (source / "workspace_app/release.json").write_text(json.dumps({"release_id": "p9.11.2", "app_api_contract": 11}))
        return root.resolve()

    def _status(self, root: pathlib.Path, listener_release: str):
        source = root / "releases" / listener_release / "source/reference/python"
        python = root / "venvs" / listener_release / "bin/python"
        with (
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_listener", return_value=(30686, "Python")),
            mock.patch.object(process, "_process_command", return_value=f"{python} p9_03_workspace.py serve"),
            mock.patch.object(process, "_process_cwd", return_value=source),
            mock.patch.object(process, "_live_assets_match", return_value=True),
            mock.patch.object(process.p706, "verify_release"),
        ):
            return process.status(root)

    def test_current_exact_requires_exact_listener_release(self):
        root = self._root("current", "current")
        self.assertEqual(self._status(root, "current")["state"], process.CURRENT_EXACT)

    def test_historical_exact_listener_is_stale_known_exact(self):
        root = self._root("current", "historical")
        observed = self._status(root, "historical")
        self.assertEqual(observed["state"], process.STALE_KNOWN_EXACT)
        self.assertEqual(observed["pid"], 30686)

    def test_non_workspace_listener_is_unknown(self):
        root = self._root("current", "current")
        with (
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_listener", return_value=(30686, "Python")),
            mock.patch.object(process, "_process_command", return_value="unrelated"),
            mock.patch.object(process, "_process_cwd", return_value=None),
        ):
            self.assertEqual(process.status(root)["state"], process.UNKNOWN)

    def test_no_listener_is_not_running(self):
        root = self._root("current", "current")
        with mock.patch.object(process, "_current_release", return_value="current"), mock.patch.object(process, "_listener", return_value=None):
            self.assertEqual(process.status(root)["state"], process.NOT_RUNNING)

    def test_wrong_interpreter_is_unknown(self):
        root = self._root("current", "current")
        source = root / "releases/current/source/reference/python"
        wrong = root / "other-python"
        wrong.touch()
        with (
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_listener", return_value=(30686, "Python")),
            mock.patch.object(process, "_process_command", return_value=f"{wrong} p9_03_workspace.py serve"),
            mock.patch.object(process, "_process_cwd", return_value=source),
            mock.patch.object(process, "_live_assets_match", return_value=True),
            mock.patch.object(process.p706, "verify_release"),
        ):
            self.assertEqual(process.status(root)["reason"], "exact invocation provenance is unavailable")

    def test_wrong_entrypoint_is_unknown(self):
        root = self._root("current", "current")
        source = root / "releases/current/source/reference/python"
        python = root / "venvs/current/bin/python"
        with (
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_listener", return_value=(30686, "Python")),
            mock.patch.object(process, "_process_command", return_value=f"{python} other.py serve"),
            mock.patch.object(process, "_process_cwd", return_value=source),
            mock.patch.object(process.p706, "verify_release"),
        ):
            self.assertEqual(process.status(root)["reason"], "wrong entrypoint")

    def test_ambiguous_listener_is_unknown(self):
        root = self._root("current", "current")
        with mock.patch.object(process, "_current_release", return_value="current"), mock.patch.object(process, "_listener", side_effect=process.WorkspaceProcessError("ambiguous/non-loopback listener")):
            observed = process.status(root)
        self.assertEqual(observed["state"], process.UNKNOWN)
        self.assertEqual(observed["reason"], "ambiguous/non-loopback listener")

    def test_framework_interpreter_requires_managed_provenance(self):
        root = self._root("current", "current")
        source = root / "releases/current/source/reference/python"
        framework = root / "framework-python"
        framework.touch()
        with (
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_listener", return_value=(30686, "Python")),
            mock.patch.object(process, "_process_command", return_value=f"{framework} p9_03_workspace.py serve"),
            mock.patch.object(process, "_process_cwd", return_value=source),
            mock.patch.object(process, "_process_start_identity", return_value="start"),
            mock.patch.object(process, "_live_assets_match", return_value=True),
            mock.patch.object(process.p706, "verify_release"),
        ):
            self.assertEqual(process.status(root)["state"], process.UNKNOWN)
            process._write_process_metadata(root, "current", 30686, "start")
            observed = process.status(root)
        self.assertEqual(observed["state"], process.CURRENT_EXACT)
        self.assertEqual(observed["proof_mode"], "MANAGED_SPAWN_PROOF")

    def test_pid_reuse_rejects_managed_metadata(self):
        root = self._root("current", "current")
        process._write_process_metadata(root, "current", 30686, "old-start")
        source = root / "releases/current/source/reference/python"
        framework = root / "framework-python"
        framework.touch()
        with (
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_listener", return_value=(30686, "Python")),
            mock.patch.object(process, "_process_command", return_value=f"{framework} p9_03_workspace.py serve"),
            mock.patch.object(process, "_process_cwd", return_value=source),
            mock.patch.object(process, "_process_start_identity", return_value="new-start"),
            mock.patch.object(process, "_live_assets_match", return_value=True),
            mock.patch.object(process.p706, "verify_release"),
        ):
            self.assertEqual(process.status(root)["state"], process.UNKNOWN)

    def test_stop_refuses_unknown_without_signalling(self):
        with (
            mock.patch.object(process, "status", return_value={"state": process.UNKNOWN}),
            mock.patch.object(process.os, "kill") as kill,
            self.assertRaises(process.WorkspaceProcessError),
        ):
            process.stop_for_update(pathlib.Path("/tmp/runtime"))
        kill.assert_not_called()

    def test_stop_revalidates_stale_process_before_signalling(self):
        stale = {"state": process.STALE_KNOWN_EXACT, "pid": 7, "release_sha": "a" * 40, "proof_mode": "DIRECT_OS_PROOF", "process_start_identity": "start"}
        with (
            mock.patch.object(process, "status", side_effect=[stale, stale, {"state": process.NOT_RUNNING}]),
            mock.patch.object(process.os, "kill") as kill,
            mock.patch.object(process, "_atomic_json"),
        ):
            observed = process.stop_for_update(pathlib.Path("/tmp/runtime"))
        kill.assert_called_once_with(7, process.signal.SIGTERM)
        self.assertEqual(observed["state"], process.NOT_RUNNING)

    def test_stop_does_not_signal_when_identity_changes(self):
        before = {"state": process.STALE_KNOWN_EXACT, "pid": 7, "release_sha": "a" * 40, "proof_mode": "DIRECT_OS_PROOF"}
        after = {"state": process.STALE_KNOWN_EXACT, "pid": 8, "release_sha": "a" * 40, "proof_mode": "DIRECT_OS_PROOF"}
        with (
            mock.patch.object(process, "status", side_effect=[before, after]),
            mock.patch.object(process.os, "kill") as kill,
            self.assertRaises(process.WorkspaceProcessError),
        ):
            process.stop_for_update(pathlib.Path("/tmp/runtime"))
        kill.assert_not_called()

    def test_stop_does_not_signal_when_start_identity_changes(self):
        before = {"state": process.STALE_KNOWN_EXACT, "pid": 7, "release_sha": "a" * 40, "proof_mode": "DIRECT_OS_PROOF", "process_start_identity": "A"}
        after = {**before, "process_start_identity": "B"}
        with (
            mock.patch.object(process, "status", side_effect=[before, after]),
            mock.patch.object(process.os, "kill") as kill,
            self.assertRaises(process.WorkspaceProcessError),
        ):
            process.stop_for_update(pathlib.Path("/tmp/runtime"))
        kill.assert_not_called()

    def test_stop_refuses_known_state_without_proof_mode(self):
        stale = {"state": process.STALE_KNOWN_EXACT, "pid": 7, "release_sha": "a" * 40}
        with (
            mock.patch.object(process, "status", return_value=stale),
            mock.patch.object(process.os, "kill") as kill,
            self.assertRaises(process.WorkspaceProcessError),
        ):
            process.stop_for_update(pathlib.Path("/tmp/runtime"))
        kill.assert_not_called()

    def test_process_metadata_uses_release_payload_beside_workspace_source(self):
        root = self._root("current", "current")
        release = root / "releases/current/source/reference/python"
        (release / "workspace_app/release.json").write_text(json.dumps({"release_id": "p9.11.2", "app_api_contract": 11}))
        process._write_process_metadata(root, "current", 123, "start")
        payload = json.loads((root / "run/workspace-process.json").read_text())
        self.assertEqual(payload["workspace_release"], "p9.11.2")
        self.assertEqual(payload["requested_python"], str(root / "venvs/current/bin/python"))
        self.assertEqual(payload["observed_process_start_identity"], "start")

    def test_start_uses_exact_argv_cwd_and_check_before_popen(self):
        root = self._root("current", "current")
        source = root / "releases/current/source/reference/python"
        python = root / "venvs/current/bin/python"
        entrypoint = source / "p9_03_workspace.py"
        ready = {"state": process.CURRENT_EXACT, "pid": 42, "release_sha": "current", "proof_mode": "MANAGED_SPAWN_PROOF", "process_start_identity": "start"}
        child = mock.Mock(pid=42)
        child.poll.return_value = None
        with (
            mock.patch.object(process, "status", side_effect=[{"state": process.NOT_RUNNING}, ready]),
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_require_p702_health"),
            mock.patch.object(process.subprocess, "run", return_value=mock.Mock(returncode=0)) as check,
            mock.patch.object(process.subprocess, "Popen", return_value=child) as popen,
            mock.patch.object(process, "_process_start_identity", return_value="start"),
            mock.patch.object(process, "_write_process_metadata"),
        ):
            observed = process.start(root)
        self.assertEqual(observed["proof_mode"], "MANAGED_SPAWN_PROOF")
        self.assertEqual(check.call_args.args[0], [str(python), str(entrypoint), "check"])
        self.assertEqual(popen.call_args.args[0], [str(python), str(entrypoint), "serve"])
        self.assertEqual(popen.call_args.kwargs["cwd"], source)

    def test_start_missing_identity_terminates_only_own_child(self):
        root = self._root("current", "current")
        child = mock.Mock(pid=42)
        child.poll.return_value = None
        with (
            mock.patch.object(process, "status", return_value={"state": process.NOT_RUNNING}),
            mock.patch.object(process, "_current_release", return_value="current"),
            mock.patch.object(process, "_require_p702_health"),
            mock.patch.object(process.subprocess, "run", return_value=mock.Mock(returncode=0)),
            mock.patch.object(process.subprocess, "Popen", return_value=child),
            mock.patch.object(process, "_process_start_identity", return_value=None),
            self.assertRaises(process.WorkspaceProcessError),
        ):
            process.start(root)
        child.terminate.assert_called_once_with()


class LifecycleShellTests(unittest.TestCase):
    def test_update_stops_workspace_after_backup_and_restarts_target(self):
        text = (HERE / "p7_06_macos_deploy.sh").read_text()
        update = text[text.index("update_runtime()"):text.index("rollback_last()")]
        self.assertLess(update.index('backup_preupdate "$source"'), update.index("workspace_stop_for_update"))
        self.assertLess(update.index("workspace_stop_for_update"), update.index('sh "$P705" uninstall'))
        self.assertIn("Workspace listener is UNKNOWN; operator investigation required", update)
        self.assertIn("target Workspace exact-release restart failed", update)
        self.assertIn('"workspace_listener_disposition"', text)
        self.assertIn('printf \'%s\\n\' "$workspace_was_running" > "$txdir/workspace-was-running"', update)
        self.assertIn('source observer did not unload', update)
        self.assertIn('source runtime did not stop', update)
        restore = text[text.index("restore_plist_and_start()"):text.index("backup_preupdate()")]
        self.assertLess(restore.index("workspace_stop_for_update"), restore.index('rm -f "$RUNTIME_ROOT/current"'))
        self.assertIn('workspace-was-running" ]; then', text)

    def test_launcher_requires_current_exact_not_http_200(self):
        text = (HERE / "macos_launcher/launcher.sh").read_text()
        self.assertIn('= "CURRENT_EXACT"', text)
        self.assertIn('start --runtime-root "$RUNTIME_ROOT"', text)
        self.assertNotIn("http_code", text)

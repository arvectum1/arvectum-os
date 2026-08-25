# P9.11 Workspace Listener Lifecycle Remediation

Status: `Implemented / verification pending selected-Mac governed update`

Canonical live observation: [`P9-11-F05-workspace-listener-live-state.md`](P9-11-F05-workspace-listener-live-state.md).

## Scope

`P9.11-F05` addresses the observed split between the exact current installed
release and a historical loopback Productive Workspace listener. It adds
`reference/python/p9_11_workspace_process.py`, an owner-local, stdlib-only
process helper. It is not a service manager and creates no new LaunchAgent.

## Observed Finding

Finding: `P9.11-F05 — Workspace listener lifecycle not reconciled across governed runtime update`.

The governed P7.06 transaction `2195aa1b9cecb3fd201798f4a9b59d011e145612c577049dfe85a5f69f48ae69` completed with result `PASS` and retained backup SHA-256 `778f0a29eefd602d8b7ce176d1ad0584293d07782e4d76dc008862f81b4b0e48`. Runtime before was `7dc7ceff986df41c1cd8be8668d51280c871e677`, Workspace `p9.11.1`, app contract `10`. Exact current runtime after deployment is `fdde2cde9b06722cff9716b9f580bb46692c7dcd`, containing Workspace `p9.11.2` and app contract `11`.

P7.02 and P7.05 were `HEALTHY`; the exact-current Workspace check passed. However, the observed loopback-only listener `127.0.0.1:8769`, PID `30686`, continued serving historical release `7dc7ceff986df41c1cd8be8668d51280c871e677` / Workspace `p9.11.1`. Live exact-current HTTP verification therefore failed. PID `30686` was not signalled and no runtime mutation was performed during F05 implementation. Owner recheck was not executed and remains pending.

The P7.06 deployment transaction itself succeeded. F05 concerns live application-process lifecycle reconciliation, not failure to install the target release.

## Case-C Process Provenance

The canonical live-state observation is the sole factual source for PID `30686`. Strict inspection recognizes its historical release, CWD, entrypoint, manifest and assets, but cannot reconstruct its original venv invocation from the macOS Python.framework executable representation. It remains `UNKNOWN` with proof mode `NONE`; no managed metadata is created retroactively and it is never automatically signalled.

Future Workspace processes created by this helper receive schema `arvectum.p9_11.workspace-process/2` owner-local spawn provenance. The metadata records only the requested release executable, entrypoint, CWD, PID, bind and observable process-start identity. That identity prevents PID reuse from admitting an unrelated process; metadata is supplementary to independent listener, release, CWD, entrypoint and asset verification.

The helper classifies the listener on `127.0.0.1:8769` as `NOT_RUNNING`,
`CURRENT_EXACT`, `STALE_KNOWN_EXACT`, or `UNKNOWN`. Classification requires a
single loopback socket, `p9_03_workspace.py serve` process semantics, exact
installed release provenance, matching source CWD, and matching live SPA index
and referenced assets. `UNKNOWN` is fail-closed and cannot be stopped.

## Governed Transition

P7.06 records the listener disposition, rejects `UNKNOWN` before mutation,
backs up before stopping a known listener, and starts the exact target only if
the Workspace had been running. On failure or manual rollback, the helper is
started only after the exact source release has been restored. The launcher
uses `CURRENT_EXACT`, not HTTP 200, as readiness and does not stop stale or
unknown listeners.

P7.02 remains network-listener-free. This work does not deploy a release,
terminate the observed historical PID, alter Workspace release/contract, or
close P9.11, R32, or M9.

## Evidence

- `uv run pytest -q reference/python/tests/test_p9_11_workspace_process.py reference/python/tests/test_p7_06_macos_deploy.py`: `38 passed`.
- `uv run ruff check reference/python/p9_11_workspace_process.py reference/python/tests/test_p9_11_workspace_process.py`: passed.
- Selected-Mac governed-update and rollback evidence remains required before
  this implementation is treated as operationally verified.
- The immutable P7.06 plan now records conditional Workspace classification,
  post-backup stop, and exact-target start/verification steps. These are
  non-canonical operational process transitions, not canonical mutation or
  external-effect authorization.

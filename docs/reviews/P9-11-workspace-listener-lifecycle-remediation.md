# P9.11 Workspace Listener Lifecycle Remediation

Status: `Implemented / verification pending selected-Mac governed update`

## Scope

`P9.11-F05` addresses the observed split between the exact current installed
release and a historical loopback Productive Workspace listener. It adds
`reference/python/p9_11_workspace_process.py`, an owner-local, stdlib-only
process helper. It is not a service manager and creates no new LaunchAgent.

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

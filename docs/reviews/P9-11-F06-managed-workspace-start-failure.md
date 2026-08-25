# P9.11-F06 — Managed Workspace Start Failure After Selected-Mac Reconciliation

Status: `Root cause established / bounded repair under review`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## 1. Canonical basis

Checked against canonical `arvectum1/arvectum-os` after the merged F05 implementation and the approved one-time legacy-listener decision:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted`;
- F05 implementation merge `0958b97661d51281b069820fd2d1f5ce338a11ec`;
- owner decision `DECISION-2026-08-25-P9-11-F05-ONE-TIME-LEGACY-WORKSPACE-TERMINATION` — `Approved`;
- approval commit and selected-Mac target `6ed9dade96417251d3dd5fc8cb175c7136682b63`.

No higher-authority conflict is identified by this observation.

## 2. One-time legacy-listener decision consumption

The selected-Mac execution reported that every pre-signal gate for historical PID `30686` passed:

- exact PID: PASS;
- loopback `127.0.0.1:8769`: PASS;
- exact historical CWD: PASS;
- exact historical `p9_03_workspace.py serve` entrypoint: PASS;
- historical release manifest: PASS;
- historical index/assets: PASS;
- historical Workspace: `p9.11.1`;
- strict helper pre-state: `UNKNOWN`;
- strict helper proof: `NONE`.

Exactly one owner-authorized `SIGTERM` was sent. No `SIGKILL` was used. PID `30686` exited and port `8769` became free.

The one-time termination authorization is therefore consumed. It is not reusable for another process or another signal attempt.

## 3. Governed runtime reconciliation result

P7.06 then completed successfully against canonical target `6ed9dade96417251d3dd5fc8cb175c7136682b63`:

- preflight: PASS;
- update: PASS;
- transaction: `215cb1390708bd4a0e72b567cf9060e4a84173147af618a064c464ca31640ff0`;
- backup SHA-256: `dbbe6c822385e0cdeccfb87729fdd12359dc8cae8a7531d3fff5be9e2fa4fa2c`;
- runtime after: `6ed9dade96417251d3dd5fc8cb175c7136682b63`;
- runtime equals canonical target: YES;
- P7.02: HEALTHY;
- P7.05: HEALTHY;
- installed Workspace payload: `p9.11.2`;
- app API contract: `11`;
- product/external effect replay: NO.

This establishes successful runtime reconciliation. It does not establish live Workspace readiness.

## 4. Root cause — F06

### Evidence chain

- real PID `52092` reached Uvicorn application startup;
- port `127.0.0.1:8769` became live;
- no application exception occurred (no traceback in stderr);
- helper never admitted `CURRENT_EXACT`;
- helper cleanup then produced the observed graceful `SIGTERM` shutdown;
- `workspace-process.json` absent after the failed attempt (expected: matching cleanup removed it);
- deterministic path-with-spaces regression reproduces the identity rejection.

### Root cause

The canonical process identity recognizer (`_process_identity()`) parsed raw macOS `ps command` display text with shell-oriented `shlex.split()`. Exact release paths under `~/Library/Application Support/...` contain whitespace (`Application Support`), so `shlex.split()` produced 4 tokens instead of 3, and the helper rejected the healthy exact Workspace command as `"not Workspace command"` before managed provenance could be evaluated.

### macOS framework Python nuance

On macOS, `ps command` displays the framework Python path (`Python.app/Contents/MacOS/Python`) rather than the venv Python symlink chain. These are genuinely different binaries (different inodes) within the same Python installation. Therefore `DIRECT_OS_PROOF` is structurally impossible on macOS for venv-spawned processes when `ps command` shows the framework path. The repair correctly returns `(False, None)` for structurally valid commands where the interpreter is not genuinely the same file, allowing `MANAGED_SPAWN_PROOF` to establish exact invocation.

`os.path.samefile()` grants `DIRECT_OS_PROOF` only for genuinely identical executable files; macOS framework-path divergence remains non-direct and is admitted only through `MANAGED_SPAWN_PROOF`.

### Absence of workspace-process.json

After the failed attempt, `workspace-process.json` is absent. This is expected behavior from matching cleanup (`_cleanup_own_spawn()` invalidates metadata matching the failed PID/release/start_identity). It is not evidence that metadata write was the primary failure.

## 5. Bounded repair

Branch: `p9-11-f06-space-safe-process-identity`

### Changes

1. **`_process_identity()`** — Replaced `shlex.split()` with right-to-left suffix matching:
   - Matches absolute entrypoint suffix (`/{exact_path} serve`);
   - Matches relative entrypoint suffix (`p9_03_workspace.py serve`);
   - Extracts executable display by removing suffix from the right (no splitting on internal whitespace);
   - Guards against flags/extra arguments in executable display;
   - Uses `os.path.samefile()` for interpreter comparison (handles macOS framework vs venv symlink chains);
   - Returns `(False, None)` for structurally valid commands where interpreter doesn't exactly match, allowing managed proof.

2. **`_cleanup_own_spawn()`** — When child has already exited before cleanup runs, now invalidates matching metadata instead of silently returning. Prevents stale metadata from remaining after failed spawns.

3. **`start()` readiness diagnostics** — Timeout error now includes `state`, `reason`, and `proof_mode` from the last observed status. Prevents opaque 30-second failures.

### Security non-regression

- UNKNOWN unsignallable: preserved;
- PID-reuse protection: preserved;
- process-start-identity revalidation: preserved;
- exact entrypoint/CWD/release/manifest/assets: preserved;
- owner-only metadata: preserved;
- P7.06 fail closed on UNKNOWN: preserved;
- P7.02 `network_listener_mode = none`: preserved;
- no second production service lifecycle: preserved;
- no `SIGKILL` normal path: preserved.

## 6. Current safety state

- historical PID `30686`: terminated by the consumed one-time owner decision;
- no repeated signal is authorized by that decision;
- current runtime: exact canonical `6ed9dade96417251d3dd5fc8cb175c7136682b63`;
- P7.02/P7.05: healthy;
- current Workspace payload: `p9.11.2` / contract `11`;
- live Workspace: `NOT_RUNNING`;
- owner recheck: **blocked / not yet executable**, because the Desktop launcher was neither refreshed nor opened and no live Workspace reached `CURRENT_EXACT`;
- P9.11 remains `Current`;
- R32 remains locked;
- no synthetic owner-session evidence is permitted.

## 7. Required next steps

After the bounded repair is merged:

1. retry managed Workspace start through the exact helper;
2. verify `CURRENT_EXACT` with `MANAGED_SPAWN_PROOF`;
3. refresh Desktop launcher from exact canonical release;
4. open Desktop launcher for owner recheck;
5. stop automation at real owner feedback.

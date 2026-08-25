# P9.11-F06 — Managed Workspace Start Failure After Selected-Mac Reconciliation

Status: `Operationally verified`
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
- F06 executable-path repair PR `#4` merged through `3b4d2b2be4a095ff04e5703b36b3ef189c3d4057`;
- selected-Mac runtime before F06 deployment remains `6ed9dade96417251d3dd5fc8cb175c7136682b63`.

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
- runtime equals that canonical target: YES;
- P7.02: HEALTHY;
- P7.05: HEALTHY;
- installed Workspace payload: `p9.11.2`;
- app API contract: `11`;
- product/external effect replay: NO.

This establishes successful F05 runtime reconciliation. It does not establish live Workspace readiness after the F06 repair merge.

## 4. Root cause — F06

### Evidence chain

- real PID `52092` reached Uvicorn application startup;
- port `127.0.0.1:8769` became live;
- no application exception occurred (no traceback in stderr);
- helper never admitted `CURRENT_EXACT`;
- helper cleanup then produced the observed graceful `SIGTERM` shutdown;
- `workspace-process.json` was absent after the failed attempt because matching cleanup removed it;
- deterministic path-with-spaces regression reproduced the identity rejection.

### Root cause

The canonical process identity recognizer (`_process_identity()`) parsed raw macOS `ps command` display text with shell-oriented `shlex.split()`. Exact release paths under `~/Library/Application Support/...` contain whitespace (`Application Support`), so `shlex.split()` produced four tokens instead of three and rejected the healthy exact Workspace command as `not Workspace command` before managed provenance could be evaluated.

### macOS framework Python nuance

On macOS, `ps command` may display the framework Python path (`Python.app/Contents/MacOS/Python`) rather than the exact requested venv Python path. These can be genuinely different files. `DIRECT_OS_PROOF` therefore applies only when `os.path.samefile()` confirms the observed executable and requested release Python are genuinely identical. Framework-path divergence remains non-direct and requires `MANAGED_SPAWN_PROOF`.

### Absence of workspace-process.json

After the failed attempt, `workspace-process.json` was absent. This is expected matching cleanup behavior and is not evidence that metadata write was the primary failure.

## 5. Canonical bounded repair

PR `#4` is merged through `3b4d2b2be4a095ff04e5703b36b3ef189c3d4057`.

The canonical repair:

1. replaces shell-token parsing of raw `ps command` display text with right-to-left exact entrypoint recognition that preserves legitimate executable paths containing whitespace;
2. validates the extracted executable as an executable file without treating internal whitespace as argument separation;
3. grants `DIRECT_OS_PROOF` only for genuinely identical executable files and leaves framework divergence to managed provenance;
4. preserves exact CWD, entrypoint, manifest, live-asset, PID and process-start-identity checks;
5. removes matching failed-spawn metadata when a newly created child has already exited;
6. exposes bounded last-state/reason/proof-mode readiness diagnostics.

Validation evidence before merge:

- focused F06 / Workspace lifecycle tests: PASS;
- exact venv Python and entrypoint paths containing `Application Support`: PASS;
- real start-to-real-status managed-provenance regression: PASS;
- framework + managed proof: `CURRENT_EXACT`;
- framework without managed proof: `UNKNOWN` / proof `NONE`;
- PID reuse and historical unproven-process fail-closed behavior: PASS;
- GitHub Reference Python CI / full `unittest discover`: PASS on exact reviewed head `99d4d1a130885c6a399e3077f4ac15a113d67a98`.

Two local Python `3.14.7` baseline failures were reproduced unchanged on canonical pre-F06 `main` and do not involve PR `#4`: one brittle P7.05 error-message assertion and one macOS `/var` → `/private/var` temporary-path equivalence assertion. They do not constitute F06 operational proof or waiver.

### Security non-regression

- `UNKNOWN` remains unsignallable;
- PID-reuse protection remains binding;
- process-start-identity revalidation remains binding;
- exact entrypoint/CWD/release/manifest/assets remain required;
- managed metadata remains owner-local and non-authoritative;
- P7.06 remains fail closed on `UNKNOWN`;
- P7.02 remains `network_listener_mode = none`;
- no second production service lifecycle is introduced;
- no normal `SIGKILL` path is introduced.

## 6. Current safety and operational state

- historical PID `30686`: terminated by the consumed one-time owner decision;
- no repeated signal is authorized by that decision;
- F06 repair: merged canonical;
- selected-Mac runtime equals canonical `470d4e310973ed873eb71d1bec3cf0985288be6b`;
- P7.02/P7.05: healthy;
- Workspace: `CURRENT_EXACT` with `MANAGED_SPAWN_PROOF`;
- exact live assets: PASS;
- Desktop launcher: refreshed and opened;
- the subsequent real owner recheck executed and created F07.
- P9.11 remains `Current`;
- R32 remains locked;
- no synthetic owner-session evidence is permitted.

F06 is therefore **operationally verified** in its bounded process-identity scope. It does not make the subsequent F07 owner recheck pass or deploy the unmerged remediation PR.

## 7. Required next steps

1. complete final review of F07 remediation PR `#6`;
2. merge and govern-deploy the revised Workspace release;
3. verify the exact post-deployment runtime, `CURRENT_EXACT` proof, and live assets;
4. refresh/open the exact-release Desktop launcher;
5. stop automation at the next real owner recheck and collect actual feedback.

# P9.11-F06 — Managed Workspace Start Failure After Selected-Mac Reconciliation

Status: `Observed / investigation pending`
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

## 4. New real finding

After the successful P7.06 update, the canonical managed Workspace lifecycle attempted to start the exact current Workspace.

Reported attempted child PID: `52092`.

The final observed state was:

- Workspace helper state: `NOT_RUNNING`;
- admissible Workspace proof: none reported;
- managed metadata: FAIL / absent or invalid after the failed start attempt;
- live exact assets: FAIL because no accepted live exact Workspace remained ready;
- Desktop launcher refresh: not executed;
- Desktop launcher open: not executed.

Therefore the selected Mac is now on the exact canonical runtime, but Productive Workspace is not live.

Finding:

`P9.11-F06 — Canonical managed Workspace spawn exits or disappears before CURRENT_EXACT readiness.`

The root cause is **not yet established** by this observation. Repository code shows that `start()` first performs the exact Workspace check, spawns the exact release Python/entrypoint, writes managed provenance, and waits for `CURRENT_EXACT`; a child that exits before readiness causes the helper to fail. The selected-Mac stdout/stderr and process evidence are required to determine the actual cause.

## 5. Current safety state

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

## 6. Required next evidence

Before any retry of `start()` or launcher execution, collect read-only selected-Mac evidence for the failed managed spawn, including at minimum:

- `workspace.stderr.log` and `workspace.stdout.log` from the failed attempt;
- whether PID `52092` still exists;
- whether any listener currently owns port `8769`;
- current strict helper `status` output;
- presence, ownership, mode and content identity of `run/workspace-process.json`, if it exists;
- exact `p9_03_workspace.py check` result on current release;
- exact target Python / `uvicorn` / `fastapi` import evidence;
- relevant current release paths and manifest verification.

No second Workspace start should be attempted until the failure mode is understood or a bounded repair/retry plan is reviewed.

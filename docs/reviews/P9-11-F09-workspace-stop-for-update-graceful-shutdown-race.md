# P9.11-F09 — Workspace Stop-for-Update Graceful-Shutdown Race

Status: `Repair under review`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform / operational lifecycle`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical Basis

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- F06 remains operationally verified in its bounded exact-process identity scope;
- F07 remains bounded owner-recheck PASS;
- F08 p9.11.5 semantic repair is merged, but deployment and real owner recheck remain pending;
- R32 remains locked.

## Real Failed Deployment

The selected-Mac p9.11.5 deployment attempted canonical target `edfd1e835a74c80bc49a94a85f2ab71965653afa` from runtime `dc0e0cff83a9031a3686191b5cf304ee03c2d1eb`.

- P7.06 preflight: `PASS`;
- pre-update backup SHA-256: `1fd797ead8a6aa8f077885e83ae9753baab507e26c165e59e117d8d3062c43bb`;
- update: `FAIL` with `Workspace HTTP is unavailable` during trusted stop-for-update;
- target activation and current-pointer mutation: `NO`;
- new P7.06 transaction: `NONE`; no historical transaction is fabricated;
- second signal/retry, SIGKILL, product/external effect, canonical mutation, and historical-effect replay: `NO`;
- post-state: source runtime remained `dc0e...`, P7.02/P7.05 were healthy, Workspace was `NOT_RUNNING`.

## Root Cause And Repair Boundary

`stop_for_update()` correctly required full exact process, release, HTTP index, and asset proof before its one `SIGTERM`. Its post-signal polling incorrectly called `status()`, which also performs HTTP and asset checks. During a graceful shutdown the HTTP server may disappear before the process exits and before the loopback listener is released. One asset fetch could also propagate `WorkspaceProcessError` rather than classify readiness as false.

The repair preserves full pre-signal `status()` and immediate identity revalidation. After `SIGTERM`, it uses only original PID start identity and exact loopback listener inspection. Successful stop requires both original process exit and port release. PID reuse, foreign/ambiguous listeners, and timeout fail closed; no second signal or SIGKILL is introduced. Metadata is removed only after both conditions hold. Asset fetch unavailability now classifies as an asset mismatch.

## Pre-Activation Failure Evidence

If a future trusted Workspace stop fails before target activation, P7.06 records an existing-schema `FAIL` transaction when recording is available. It does not query Workspace status again after the helper signal; the record explicitly marks that post-signal state as not queried. It states that target activation never began, the current pointer was unchanged, backup was retained, no rollback occurred, and operator investigation/retry is required. This does not retrospectively alter the historical failed attempt.

## Acceptance Evidence

- Full status/HTTP/assets verification remains mandatory before `SIGTERM`.
- No HTTP or asset status call occurs after `SIGTERM`.
- Original PID exit and port release are both required.
- PID reuse and foreign listener states fail closed without signaling another process.
- Exactly one `SIGTERM`; no `SIGKILL`.
- Workspace app release remains `p9.11.5`; app API remains `11`.
- No Workspace owner-task eligibility or F08 UI semantics change is admitted.

## Disposition

F09 blocks the next F08 deployment. After F09 merge, the selected Mac must govern-deploy the new canonical main from the current `NOT_RUNNING` Workspace state, verify exact runtime/assets, start the target Workspace once through its new exact helper, then resume the real F08 owner recheck. F08 remains open; P9.11 remains Current; R32 remains locked.

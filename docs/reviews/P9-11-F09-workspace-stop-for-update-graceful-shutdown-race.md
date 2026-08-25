# P9.11-F09 — Workspace Stop-for-Update Graceful-Shutdown Race

Status: `Resolved in bounded scope / operationally restored; live post-SIGTERM path not re-exercised`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform / operational lifecycle`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical Basis

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- F06 remains operationally verified in its bounded exact-process identity scope;
- F07 remains bounded owner-recheck PASS;
- F08 p9.11.5 semantic repair is merged and deployed; real owner recheck remains pending;
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

If a future trusted Workspace stop fails before target activation, P7.06 records an existing-schema `FAIL` transaction when recording is available. The adapter deliberately does not re-query Workspace after a failed stop-for-update helper call. The helper may have failed before or after its one permitted SIGTERM, so the adapter records `signal_disposition=unknown_to_adapter` unless separately proven; it performs no second signal or retry. The record states that target activation never began, the current pointer was unchanged, backup was retained, no rollback occurred, and operator investigation/retry is required. This does not retrospectively alter the historical failed attempt.

## Repository Review And Merge Evidence

- PR `#9` reviewed head: `a451451037f8f77382264418039dac1ed5a9089f`;
- targeted lifecycle validation: `90 passed`;
- Python compilation, shell syntax and `git diff --check`: `PASS`;
- exact-head Reference Python CI run `32890992380`: `PASS`;
- merge commit on canonical `main`: `8d10059c8b45abfd679891a0442bca3073a36dcc`;
- selected-Mac runtime mutation during repair/review: `NO`.

## Post-Merge Selected-Mac Restoration Evidence

The selected Mac then performed one governed deployment from the safe post-failure state where Workspace was already `NOT_RUNNING`.

- canonical target: `03ba2c72fb9460e97b628c4b3dac36ac496cb942`;
- source runtime: `dc0e0cff83a9031a3686191b5cf304ee03c2d1eb`;
- Workspace pre-state: `NOT_RUNNING`;
- P7.06 preflight: `PASS`;
- P7.06 update: `PASS`;
- transaction: `8d8893f5207cbd52eb67e99abad593f6ce069add3314c95373f081abdcd74ae0`;
- backup SHA-256: `ee93ae8fd9d4d4f5b8729e8309e3459ef3fbbfbf7995516d15c9ce5f836ce836`;
- Workspace stop invocation during deployment: `NO`;
- SIGTERM during deployment: `NO`;
- resulting runtime equals canonical target: `YES`;
- P7.02/P7.05: `HEALTHY`;
- Workspace remained `NOT_RUNNING` until an explicit managed start through the exact target helper;
- managed target start attempts: `1`;
- Workspace `p9.11.5` / app contract `11` reached `CURRENT_EXACT` with `MANAGED_SPAWN_PROOF`;
- listener remained loopback-only;
- exact live index/assets: `PASS`;
- Desktop launcher: `PASS`.

This establishes successful operational restoration and exact target deployment after the failed historical update. It does **not** prove that the real selected-Mac post-SIGTERM race was re-exercised after the repair, because the source Workspace was intentionally `NOT_RUNNING` before this deployment. The repaired post-SIGTERM branch remains covered by the exact repository regression suite and should receive natural live confirmation on a future ordinary update from a running exact Workspace rather than through an artificial mutation solely to manufacture evidence.

## Acceptance Evidence

- Full status/HTTP/assets verification remains mandatory before `SIGTERM`.
- No HTTP or asset status call occurs after `SIGTERM` in the repaired helper.
- Original PID exit and port release are both required.
- PID reuse and foreign listener states fail closed without signaling another process.
- Exactly one `SIGTERM`; no `SIGKILL`.
- Future pre-activation stop failures preserve signal uncertainty rather than claiming a signal occurred.
- Workspace app release remains `p9.11.5`; app API remains `11`.
- No Workspace owner-task eligibility or F08 UI semantics change is admitted.
- Selected-Mac canonical runtime and exact managed Workspace service were operationally restored without retrying the historical failed transition or replaying product/external effects.

## Disposition

F09 no longer blocks F08. The bounded defect is resolved in code, guarded by regression tests, merged, and the selected Mac has been operationally restored to exact canonical runtime `03ba2c72fb9460e97b628c4b3dac36ac496cb942` with Workspace `p9.11.5` `CURRENT_EXACT`. The exact real post-SIGTERM path was not re-exercised in this recovery deployment and that limitation remains explicit; natural verification may be recorded during a future ordinary update from a running exact Workspace. The current critical path returns to the real F08 owner recheck. P9.11 remains Current; R32 remains locked.

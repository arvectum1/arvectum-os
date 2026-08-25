# DECISION-2026-08-25 — P9.11-F05 One-Time Legacy Workspace Termination

Status: `Approved`
Decision date: `2026-08-25`
Owner / decision authority: `ООО «Арвектум»`
Task classification: `governance` with `platform operational recovery`
Decision subject: `P9.11-F05 — selected-Mac legacy Workspace listener reconciliation`
Constitution: `1.2.0` — `Ratified`
Architecture baseline: RFC-0001 through RFC-0008 `1.0.0` — `Accepted`; ADR-0001 — `Accepted`
Decision Authority Policy: `Proposed 0.2.1` — non-binding; residual authority remains with owner
Approval source: explicit owner approval `одобряю` in the Arvectum OS project conversation at `2026-08-25T09:38+03:00`
Canonical implementation baseline: `8dd0cad2dda498fc047a7f88bd8bcd987583d1e9`
Related implementation merge: PR `#3`, merge commit `0958b97661d51281b069820fd2d1f5ce338a11ec`

## 1. Decision

**APPROVED — one bounded operator-authorized graceful termination attempt may be made against the specifically observed historical Productive Workspace process PID `30686` on the selected Mac, solely to reconcile P9.11-F05.**

This approval exists because the canonical F05 implementation correctly classifies the historical process as `UNKNOWN` / proof `NONE`: available macOS process evidence proves the historical release, CWD, entrypoint, manifest and live assets, but does not reconstruct the original virtual-environment invocation strongly enough for the normal lifecycle controller to signal it automatically.

The approval does not weaken that normal fail-closed rule.

## 2. Exact authorized target

The one-time signal is authorized only if immediately before signalling all of the following are independently revalidated:

- PID exactly `30686`;
- exactly one listener owns `127.0.0.1:8769`;
- listener is IPv4 loopback only;
- process CWD exactly resolves to `~/Library/Application Support/ArvectumOS/persistent-internal/releases/7dc7ceff986df41c1cd8be8668d51280c871e677/source/reference/python`;
- Workspace entrypoint semantics resolve exactly to that historical release's `p9_03_workspace.py serve`;
- installed historical release `7dc7ceff986df41c1cd8be8668d51280c871e677` passes its admissible legacy-source manifest/provenance verification;
- live `/` equals the historical release Workspace index;
- all referenced live JS/CSS assets equal that historical release's exact assets;
- live Workspace release remains `p9.11.1`;
- no evidence indicates PID reuse, listener replacement, different CWD/entrypoint, different release, non-loopback exposure or other identity drift.

If any condition differs, the authorization is not applicable and the operation MUST stop without signalling the process.

## 3. Authorized operation

When every gate in section 2 passes, the operator may send exactly one normal graceful `SIGTERM` attempt to PID `30686`.

After the signal:

- wait a bounded interval for PID `30686` to exit and port `8769` to become free;
- do not use `SIGKILL`;
- do not send a second signal attempt under this decision;
- if graceful termination does not complete, stop and require a new explicit owner decision before any stronger or repeated termination action.

If PID `30686` has already exited naturally before the operation, no signal is required and the reconciliation may continue after confirming port/listener state.

## 4. One-time scope and consumption

This decision is not a permanent lifecycle exception.

It does not authorize signalling:

- any PID other than `30686`;
- any replacement process that later receives PID `30686` but fails the exact section-2 evidence;
- any future `UNKNOWN` Workspace listener;
- any arbitrary local process occupying port `8769`;
- a second termination attempt after the authorized attempt is consumed.

The normal P9.11 Workspace lifecycle remains fail-closed: `UNKNOWN` processes are unsignallable without a separate explicit operator/owner decision.

## 5. Post-termination reconciliation

After the historical listener is absent and port `8769` is free, the authorized operational sequence is:

1. reconcile the local canonical checkout to current canonical `main` without rewriting history;
2. execute P7.06 governed update from the installed source release to the exact current canonical target;
3. verify P7.02 and P7.05 healthy on the exact target;
4. verify Workspace payload remains `p9.11.2` / internal application contract `11`;
5. start Workspace only through the canonical P9.11 exact-release helper so the new process receives managed spawn provenance bound to PID and process-start identity;
6. require live status `CURRENT_EXACT` with an admissible proof mode before treating Workspace as ready;
7. refresh the local Desktop launcher from the exact canonical release if required, then open it;
8. stop automation at the real owner recheck and obtain actual owner feedback; no synthetic owner-session evidence may be created.

P7.06 rollback, backup, exact-source restoration, observer/runtime health, repository-identity and replay-safety rules remain binding.

## 6. Authority and security boundary

This decision authorizes only the bounded local operational process transition described above.

It does not:

- grant new Authorization or Organizational Authority beyond this exact owner decision;
- change canonical business state;
- authorize product external effects;
- authorize historical effect replay;
- relax Host/Origin/CSRF/session/Data Governance controls;
- introduce a second LaunchAgent or production-service lifecycle;
- change ADR-0001;
- change P7.02 `network_listener_mode = none`;
- permit retroactive managed provenance for PID `30686`.

## 7. Lifecycle and commercial non-claims

This approval does not close P9.11, unlock R32, achieve M9, promote any Platform Capability or Product Contract lifecycle, establish customer Production, create a public/stable API, or create SLA/support/conformance commitments.

P9.11 remains `Current` until real selected-Mac reconciliation, owner recheck and the remaining daily-use/friction evidence are factually completed.

## 8. Completion evidence required

Execution evidence must record at minimum:

- canonical target SHA used;
- pre-signal PID/listener/CWD/entrypoint/release/manifest/index/assets checks;
- whether a signal was actually sent;
- signal type (`SIGTERM`) and one-attempt count;
- whether PID exited and port became free;
- P7.06 transaction result and transaction identifier;
- exact runtime after reconciliation;
- P7.02/P7.05 health;
- live Workspace state, proof mode, PID, Workspace release and app contract;
- Desktop launcher refresh/open result;
- explicit statement that owner recheck evidence is pending until supplied by the owner.

A successful repository test or automated browser check does not substitute for the real owner recheck.

# P9.11-F05 — Workspace listener live-state observation

Status: `Observed / Repair in review`
Date: `2026-08-24`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## 1. Canonical basis

Checked against canonical `arvectum1/arvectum-os` `main` after the repository-identity migration:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted`;
- master roadmap `2.95.2`;
- Phase 9 roadmap `1.13.2`.

No higher-authority conflict is identified by this observation.

## 2. Real operational observation

The governed P7.06 transaction
`2195aa1b9cecb3fd201798f4a9b59d011e145612c577049dfe85a5f69f48ae69`
completed successfully and installed exact runtime release
`fdde2cde9b06722cff9716b9f580bb46692c7dcd`.

That installed release contains Productive Workspace application release
`p9.11.2`, internal application contract `11`.

The live Workspace listener did **not** move to that exact release. Read-only inspection found PID `30686` still serving historical release
`7dc7ceff986df41c1cd8be8668d51280c871e677`, Workspace `p9.11.1`.

Therefore the truthful state is:

- exact current runtime install: `fdde2cde...` — PASS;
- installed Workspace payload: `p9.11.2` / contract `11` — present;
- live Workspace listener: stale historical exact listener — FAIL for current-release continuity;
- P7.02/P7.05 runtime/observer health: retained as healthy in the real inspection context;
- historical listener PID was not signalled by this observation/record;
- owner recheck of the repaired live Workspace has not occurred.

This supersedes the narrower wording that described `p9.11.2 deployment` itself as still pending. The remaining blocker is live Workspace listener reconciliation and subsequent owner recheck.

## 3. Repair state

PR `#3 — P9.11 — reconcile exact-release Workspace listener lifecycle` contains a bounded repair proposal, but it is **not merged** as of this record.

Repository-level review on PR #3 identified material changes required before merge:

1. preserve the distinction between successful exact runtime installation and stale live Workspace activation;
2. retain reconstructable real F05 evidence;
3. strengthen process identity before any known listener may be signalled, including exact release-specific interpreter and entrypoint identity;
4. add focused lifecycle and spoof/ambiguity fail-closed regression coverage.

Until those findings are resolved and the repair is merged, PR #3 is not canonical implementation state.

## 4. Canonical status consequence

`P9.11` remains `Current`.

`R32` remains locked.

`P9.12` has not started.

`M9` remains open.

The next local operational proof after an acceptable merged repair is a governed selected-Mac reconciliation/update followed by real owner recheck of the live `p9.11.2` Productive Workspace.

No lifecycle, Production, Stable/public interface, SLA/support or conformance promotion is created by this observation.

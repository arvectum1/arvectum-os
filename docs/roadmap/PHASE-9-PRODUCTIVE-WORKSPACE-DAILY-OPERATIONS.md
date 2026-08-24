# Arvectum OS Phase 9 — Productive Workspace & Daily Operations

Status: `Active`
Version: `1.13.4`
Created: `2026-08-21`
Updated: `2026-08-24`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)

F05 Case-C disposition: historical PID `30686` remains `UNKNOWN`, is not retroactively attributed or signalled, and future helper-created Workspace processes use managed spawn provenance with PID-reuse protection. P9.11 remains Current, R32 locked, P9.12 not started and M9 open.
Milestone: `M9 — Daily-use organizational workbench`
Intermediate milestone: `M9-alpha — Usable Internal Workspace — Achieved / PASS`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `Accepted 1.0.0`; ADR-0001 `Accepted`
Predecessor: `Phase 8 / M8 — Complete / PASS`
Activation decision: [`DECISION-2026-08-21-PHASE-9-PRODUCTIVE-WORKSPACE-ACTIVATION`](../governance/decisions/DECISION-2026-08-21-PHASE-9-PRODUCTIVE-WORKSPACE-ACTIVATION.md)

## 1. Purpose

Phase 9 converts the proven Arvectum OS runtime and semantic foundation into a genuinely useful daily work environment for the owner/operator of ООО «Арвектум».

The governing question is:

> Can the owner use Arvectum OS as the normal daily interface for understanding what needs attention, finding organizational information, inspecting context, making governed decisions and working across products without relying on GitHub, terminal commands or internal identifiers for ordinary work?

The legacy P4/P7 browser surfaces remain diagnostic/reference/recovery evidence. Productive Workspace is a separate long-lived internal application boundary governed by ADR-0001.

## 2. Productive Workspace principles

1. Human work first; platform internals second.
2. Derived presentation is not canonical authority.
3. UI state/buttons/session do not create Authorization, Organizational Authority, Data Governance permission or Consequential Approval.
4. Products own product semantics and enter Workspace only through explicit governed boundaries.
5. AI proposes; Governed Execution acts.
6. Real daily usability is evidence; synthetic owner sessions are not.
7. Phase 9 is internal-first and creates no speculative public surface.

## 3. Work breakdown

| ID | Work item | Status | Exit outcome |
|---|---|---:|---|
| P9.00 | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS | Phase 9 activated |
| P9.01 | Real operator jobs-to-be-done + acceptance journeys | 🟩 Complete / PASS | six owner journeys fixed |
| P9.02 | Application architecture spike + frontend/BFF/session decision | 🟩 Complete / PASS | preferred topology selected |
| R29 | Productive Workspace Boundary Review | 🟩 Complete / PASS | ADR-0001 Accepted |
| P9.03 | Real application shell + navigation + Organization/user context | 🟩 Complete / PASS | ADR-0001 application shell |
| P9.04 | My Work / Needs Attention projection | 🟩 Complete / PASS | actionable owner queue |
| P9.05 | Human-friendly Records / Documents / Knowledge + global search | 🟩 Complete / PASS | understandable discovery/context |
| P9.06 | Executions / Decisions / governed actions UX | 🟩 Complete / PASS | authority-safe action UX |
| R30 | M9-alpha Usability / IA Review | 🟩 Complete / PASS | ordinary path usable |
| M9-alpha | Usable Internal Workspace | 🟩 Achieved / PASS | core browser work usable |
| P9.07 | Product-owned Workspace surfaces / composition | 🟩 Complete / PASS | two real product surfaces |
| P9.08 | Arvectum AI Copilot | 🟩 Complete / PASS | source-grounded bounded assistance |
| P9.09 | Activity / notifications / attention routing | 🟩 Complete / PASS | non-authoritative activity UX |
| P9.10 | ООО «Арвектум» organization composition | 🟩 Complete / PASS | company-level composition |
| R31 | Product Composition / AI Safety Review | 🟩 Complete / PASS | product/AI boundaries PASS |
| **P9.11** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current** | real owner sessions + material friction closure |
| R32 | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ Locked | pre-closure hardening PASS |
| P9.12 | Phase 9 / M9 closure review | ⬜ | exact-scope M9 closure |

## 4. Accepted application architecture

ADR-0001 is binding for the current `Local / Persistent Internal / owner-operated` Productive Workspace scope:

- React + TypeScript SPA;
- same-origin co-deployed Python BFF;
- opaque revocable server-side session;
- explicit server-side Organization/Actor and current Authorization/Data Governance checks;
- CSRF/Origin/Host protection for unsafe requests;
- non-authoritative rebuildable read models/projections;
- product UI compile-time composition through explicit registered boundaries;
- exact-release SPA+BFF deployment through P7.06;
- no public/stable BFF/API/browser compatibility promise.

## 5. P9.11 dogfooding mechanism

Canonical baseline: [`P9-11-real-daily-use-dogfooding-friction-backlog-closure.md`](../reviews/P9-11-real-daily-use-dogfooding-friction-backlog-closure.md).

The local dogfooding store records bounded Observations, not canonical Events or validated Knowledge. Real owner friction is classified by journey, Workspace surface, severity and boundary. Material/blocker items remain closure-blocking until factually resolved/rechecked or otherwise dispositioned through the allowed governed path.

P9.11 cannot close from repository tests or simulated clicks alone. Real owner work primarily through Workspace is required.

## 6. Real P9.11 findings to date

### F03 — owner-first information architecture

Real owner use found that the Workspace did not make ordinary work obvious enough. `p9.11.2` repairs the navigation/presentation around:

- Today;
- Work;
- Information;
- Arvectum AI;
- System.

Legacy deep routes and protected projection semantics remain available; product/security/authority semantics are unchanged.

### F04 — canonical repository identity migration

The first p9.11.2 governed deployment attempt failed closed because P7.06 still admitted only obsolete repository identity `arvectum/arvectum-os`.

The merged bounded migration now requires current checkout/new deployment targets from canonical `arvectum1/arvectum-os`, while old `arvectum/arvectum-os` identity may be recognized only as immutable historical installed-source provenance.

Focused F04 validation: `44 passed`; shell syntax and Python compilation PASS. The broad local reference suite remains blocked by pre-existing macOS `/var` symlink/topology fixture issues (`2 failures`, `62 errors`); no guard was weakened.

### F05 — exact-release live Workspace listener continuity

Canonical evidence: [`P9.11-F05 — Workspace listener live-state observation`](../reviews/P9-11-F05-workspace-listener-live-state.md).

The governed P7.06 transaction `2195aa1b9cecb3fd201798f4a9b59d011e145612c577049dfe85a5f69f48ae69` successfully installed exact runtime `fdde2cde9b06722cff9716b9f580bb46692c7dcd`, containing Workspace `p9.11.2` / internal application contract `11`.

However, the live loopback Workspace listener did not reconcile to that release. PID `30686` remained on historical exact release `7dc7ceff986df41c1cd8be8668d51280c871e677` / Workspace `p9.11.1`.

Truthful current state:

- current exact runtime installed: PASS;
- p9.11.2 payload installed: PASS;
- live listener current-release continuity: FAIL;
- observed listener is stale historical exact process;
- listener was not signalled by the observation/evidence step;
- owner recheck of p9.11.2 is pending.

PR #3 contains a repair proposal but is not merged. Repository-level review requires, before merge:

1. corrected distinction between installed exact runtime and stale live listener;
2. reconstructable real F05 evidence;
3. stronger fail-closed process identity, including release-specific interpreter and exact entrypoint, before a listener may be signalled;
4. additional spoof/ambiguity/start/stop lifecycle regression tests.

Therefore PR #3 initial scoped test results are implementation evidence only, not merge authority.

## 7. Current critical path

```text
revise PR #3 to close material review findings
        ↓
re-run focused/required regression evidence
        ↓
merge bounded listener-lifecycle repair
        ↓
governed selected-Mac reconciliation/update
        ↓
verify live Workspace = CURRENT_EXACT p9.11.2 / contract 11
        ↓
real owner recheck
        ↓
continue ordinary daily dogfooding
        ↓
disposition recurring material friction
        ↓
R32 hardening + M9 Code Health Gate
        ↓
P9.12 / M9 closure
```

## 8. Parallel work relationship

Parallel work does not change the Phase 9 critical path.

- Lane B integration design is internally complete through INT-B7 and waits for an exact real external endpoint/deployment/account.
- Lane C product↔Workspace work may continue only on evidence and Product Contract/product-local boundaries.
- Lane D reliability/DX/technical-debt work may continue when bounded and evidence-backed.
- Lane E remains discovery only for second-Organization/customer readiness.

See [`PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md`](PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md).

## 9. M9 exit criteria

M9 requires:

1. M9-alpha remains valid;
2. at least two real product-owned surfaces remain composed through explicit boundaries;
3. source-grounded, uncertainty-aware, authority-safe AI Copilot remains valid;
4. Activity/attention remains non-authoritative;
5. company-level composition remains useful without leaking organization/product semantics into Kernel behavior;
6. real owner working sessions are completed primarily through Workspace;
7. recurring material usability friction is dispositioned;
8. security/authority boundaries remain fail closed;
9. applicable ADR obligations remain satisfied;
10. R29–R32 material findings are closed or explicitly accepted by proper authority;
11. M9 Milestone Code Health Gate passes before closure.

## 10. Explicit non-goals

Phase 9 does not by itself establish public SaaS, customer Production, universal multi-tenancy, public/stable API or SDK, Stable Product Contracts, Active Platform Capabilities, external browser support matrix, SLA/support commitments, AI Organizational Authority or automatic promotion of Observations/generated outputs into validated Knowledge.

## 11. Current canonical action

> **P9.11-F05 — revise PR #3, close its material review findings, merge the bounded listener-lifecycle repair, reconcile the selected Mac to live CURRENT_EXACT p9.11.2, then perform the real owner recheck.**

R32 remains locked until P9.11 real-session evidence and friction closure criteria are met.

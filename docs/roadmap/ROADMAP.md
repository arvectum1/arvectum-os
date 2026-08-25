# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.95.5`
Created: `2026-08-07`
Updated: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS sequencing and concurrency. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

## 2. Version note

Version `2.95.5` records PR `#3` as merged canonical implementation through merge commit `0958b97661d51281b069820fd2d1f5ce338a11ec`. The F05 listener-lifecycle repair is now part of canonical code; the last selected-Mac observation still has PID `30686` as `UNKNOWN` / proof `NONE` serving historical `p9.11.1`, and no retrospective provenance or automatic signal is permitted. Governed selected-Mac reconciliation and the real owner recheck remain pending.

The canonical repository for current checkouts and new deployments is `arvectum1/arvectum-os`. Historical `arvectum/arvectum-os` identity is retained only where immutable provenance of already-installed historical releases requires it.

The governed P7.06 transaction `2195aa1b9cecb3fd201798f4a9b59d011e145612c577049dfe85a5f69f48ae69` successfully installed exact runtime `fdde2cde9b06722cff9716b9f580bb46692c7dcd`, containing Productive Workspace `p9.11.2`, internal application contract `11`. The remaining real P9.11 blocker is operational reconciliation of the selected Mac: the last live observation still has loopback PID `30686` serving historical exact release `7dc7ceff986df41c1cd8be8668d51280c871e677` / Workspace `p9.11.1`.

Canonical observation: [`P9.11-F05 — Workspace listener live-state observation`](../reviews/P9-11-F05-workspace-listener-live-state.md) — `Observed / implementation merged; operational reconciliation pending`.

PR `#3` passed repository review and Reference Python CI and is merged. The merge itself performed no selected-Mac runtime mutation and therefore does not prove live `CURRENT_EXACT`; `P9.11` remains Current, `R32` remains locked and owner recheck has not occurred.

Lane B is internally complete through prepared `INT-B7`; no additional internal integration-planning task is admitted until an exact real 1С/CRM/СЭД/ЭДО endpoint/deployment/account is available.

This update creates no public/stable API/connector/browser contract, no customer Production, no Stable Product Contract, no Active Platform Capability and no SLA/support/conformance promotion.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Productive Workspace Browser Application Topology`, `Accepted 2026-08-21`;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02, P6.06, P8.03 and P8.06 Product Contracts remain Provisional within their exact scopes;
- operating environment remains `Local / Persistent Internal / owner-operated` with scoped conformance;
- no public/stable SDK/API/wire/browser/connector surface, external/customer Production, SLA/support/certification or broader conformance claim exists.

## 4. Strategic roadmap

| Phase | Strategic scope | Status | Milestone |
|---|---|---:|---|
| `Phase 0` | Foundation / Architecture Bootstrap | 🟩 Complete | M0 |
| `Phase 1` | Reference Implementation | 🟩 Complete | M1 |
| `Phase 2` | Core Runtime | 🟩 Complete | M2 |
| `Phase 3` | Shared Platform Capabilities | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | 🟩 Complete | M4 |
| `Phase 5` | SDK, Contracts and Extension Experience | 🟩 Complete | M5 |
| `Phase 6` | Product-driven Platform Validation | 🟩 Complete / PASS | M6 |
| `Phase 7` | Operational / Enterprise Readiness | 🟩 Complete / PASS | M7 |
| `Phase 8` | Ecosystem and External Integration | 🟩 Complete / PASS | `M8` Governed external ecosystem baseline — exact activated one-Organization scope |
| **`Phase 9`** | **Productive Workspace & Daily Operations** | **🟨 Active** | **M9 — Daily-use organizational workbench** |

## 5. Active Phase 9

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.13.5`.

| ID | Work item | Status |
|---|---|---:|
| P9.00 | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS |
| P9.01 | Real operator jobs-to-be-done + acceptance journeys | 🟩 Complete / PASS |
| P9.02 | Application architecture spike + frontend/BFF/session decision | 🟩 Complete / PASS |
| R29 | Productive Workspace Boundary Review | 🟩 Complete / PASS |
| P9.03 | Real application shell + navigation + Organization/user context | 🟩 Complete / PASS |
| P9.04 | My Work / Needs Attention projection | 🟩 Complete / PASS |
| P9.05 | Human-friendly Records / Documents / Knowledge + global search | 🟩 Complete / PASS |
| P9.06 | Executions / Decisions / governed actions UX | 🟩 Complete / PASS |
| R30 | M9-alpha Usability / IA Review | 🟩 Complete / PASS |
| M9-alpha | Usable Internal Workspace | 🟩 Achieved / PASS |
| P9.07 | Product-owned Workspace surfaces / composition | 🟩 Complete / PASS |
| P9.08 | Arvectum AI Copilot | 🟩 Complete / PASS |
| P9.09 | Activity / notifications / attention routing | 🟩 Complete / PASS |
| P9.10 | ООО «Арвектум» organization composition | 🟩 Complete / PASS |
| R31 | Product Composition / AI Safety Review | 🟩 Complete / PASS |
| **P9.11** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current — selected-Mac reconciliation + owner recheck pending** |
| R32 | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ Locked |
| P9.12 | Phase 9 / M9 closure review | ⬜ |

### P9.11 live state

- `p9.11.1`: historical selected-Mac live listener observed before F05 repair;
- `p9.11.2` / app contract `11`: installed in exact runtime `fdde2cde...` before F05 repair merge;
- F03 owner-first IA repair: implemented in p9.11.2;
- F04 canonical repository identity migration: merged; new targets require `arvectum1/arvectum-os`;
- **F05 listener-lifecycle implementation:** merged in `0958b97661d51281b069820fd2d1f5ce338a11ec`; strict exact-process proof, managed spawn provenance, PID-reuse protection, P7.06 lifecycle reconciliation and launcher `CURRENT_EXACT` readiness are canonical;
- **last selected-Mac observation:** PID `30686` remains historical `p9.11.1`, classified `UNKNOWN` / proof `NONE`; it has not been signalled by the repair/review work;
- governed selected-Mac reconciliation: pending;
- owner recheck: pending;
- synthetic owner-session evidence: prohibited.

Current critical sequence:

```text
governed selected-Mac reconciliation/update
        ↓
verify live Workspace CURRENT_EXACT on p9.11.2 / contract 11
        ↓
real owner recheck / continued daily dogfooding
        ↓
friction backlog closure
        ↓
R32
        ↓
P9.12 / M9
```

## 6. Parallel development lanes

Detailed plan: [`PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md`](PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md) `1.1.0`.

| Lane | Scope | Current status |
|---|---|---:|
| A — Productive Workspace | P9.11 → R32 → P9.12 | 🟨 Critical path |
| B — Russian-market integrations | INT-B1…INT-B7 | 🟦 Internally complete / blocked on real endpoint |
| C — Product ↔ Workspace | product-owned projections / governed entry points | 🟦 Available on evidence |
| D — Reliability / DX / technical debt | CI, recovery, observability, evidence-backed cleanup | 🟦 Continuous |
| E — Future customer/external readiness | second Organization/customer/regulatory discovery | ⬜ Discovery only |

### Lane B state

- INT-B1 — Complete / PASS;
- INT-B2 — Complete / PASS;
- INT-B3 — Complete / PASS;
- INT-B4 — Complete / PASS;
- INT-B5 — Complete / PASS;
- INT-B6 — Complete / scoped PASS;
- INT-B7 — package prepared and cross-reviewed; **pilot NOT ADMITTED** without an exact real endpoint/deployment/account.

Preferred first prepared candidate remains a bounded read-only `1С:ERP 2.5` procurement projection. No synthetic endpoint/credential/pilot evidence is acceptable. When a real endpoint exists, populate and execute INT-B7 rather than inventing INT-B8 prematurely.

## 7. Quality / test state

- merged F04 repository-identity repair: focused P7.06 Python/shell validation `44 passed`; shell syntax and Python compilation PASS;
- merged F05 PR `#3`: final focused lifecycle/P7.06/P7.02 evidence `72 passed`; historical roadmap guards `4 passed`; GitHub `Reference Python CI` / `Full reference test suite` PASS on exact reviewed head `9474b846d316ed4fb038ce90a11999401b83fcc9`;
- F05 selected-Mac operational reconciliation has not yet been executed after merge, so no live `CURRENT_EXACT` or owner-recheck PASS is claimed;
- R32 remains locked and therefore no M9 code-health PASS is claimed.

## 8. M9 definition

M9 requires M9-alpha to remain valid plus real owner working sessions primarily through Workspace, recurring material friction disposition, real product composition and AI/Activity/company surfaces remaining valid, applicable ADR obligations satisfied, R29–R32 material findings closed, and the M9 Milestone Code Health Gate PASS.

Parallel integration progress cannot substitute for P9.11 operational evidence.

## 9. Current canonical actions

**Critical path:**

> **P9.11-F05 — execute the governed selected-Mac reconciliation/update from current canonical `main`, verify the live Workspace as `CURRENT_EXACT` on `p9.11.2` / app contract `11`, then perform the real owner recheck.**

**Lane B:**

> **No internally executable action. Resume INT-B7 only when an exact real integration endpoint/deployment/account is available.**

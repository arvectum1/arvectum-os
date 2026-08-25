# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.95.9`
Created: `2026-08-07`
Updated: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS sequencing and concurrency. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

## 2. Version note

Version `2.95.9` records the real F07 owner recheck as `FAIL` and the bounded remediation under PR `#6`. The screenshot reviewed a deployed Workspace from canonical runtime `470d4e310973ed873eb71d1bec3cf0985288be6b`, not PR `#6`; it found that Home still obscured the owner’s next action and mixed scenario evidence with ordinary work. PR `#6` is not deployed and requires final review before a later real owner recheck.

F06 is **operationally verified** in its bounded scope: selected-Mac runtime equals canonical `470d4e310973ed873eb71d1bec3cf0985288be6b`; P7.02/P7.05 are healthy; Workspace reached `CURRENT_EXACT` with `MANAGED_SPAWN_PROOF`; exact live assets passed; and the Desktop launcher was refreshed/opened. This does not make the unmerged PR `#6` deployed or make F07 pass.

Canonical evidence: [`P9.11-F06 — Managed Workspace Start Failure After Selected-Mac Reconciliation`](../reviews/P9-11-F06-managed-workspace-start-failure.md) — `Operationally verified`.

The earlier F05 operational reconciliation succeeded: the exact one-time owner decision for historical PID `30686` was consumed with one graceful `SIGTERM`; PID `30686` exited and port `8769` became free; P7.06 transaction `215cb1390708bd4a0e72b567cf9060e4a84173147af618a064c464ca31640ff0` then updated the selected Mac to runtime `6ed9dade96417251d3dd5fc8cb175c7136682b63`; P7.02/P7.05 were healthy; no product/external effect replay occurred.

The canonical repository for current checkouts and new deployments is `arvectum1/arvectum-os`. Historical `arvectum/arvectum-os` identity is retained only where immutable provenance of already-installed historical releases requires it.

The one-time owner decision `DECISION-2026-08-25-P9-11-F05-ONE-TIME-LEGACY-WORKSPACE-TERMINATION` is consumed. It is not reusable for another PID or another signal attempt. Normal `UNKNOWN` Workspace listeners remain fail-closed and unsignallable without a separate exact owner decision.

`P9.11` remains Current and `R32` remains locked. The next owner recheck is pending final review, merge, governed deployment, and launch of the revised `p9.11.3` Workspace.

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

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.13.8`.

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
| **P9.11** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current — F06 verified; F07 owner recheck failed, remediation under review** |
| R32 | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ Locked |
| P9.12 | Phase 9 / M9 closure review | ⬜ |

### P9.11 live state

- F03 owner-first IA repair remains implemented in deployed Workspace `p9.11.2`;
- F04 canonical repository identity migration is merged;
- F05 listener-lifecycle implementation is merged in `0958b97661d51281b069820fd2d1f5ce338a11ec`;
- F05 selected-Mac operational reconciliation succeeded: historical PID `30686` exited after the single approved `SIGTERM`, port `8769` was freed, and the authorization is consumed;
- P7.06 transaction `215cb1390708bd4a0e72b567cf9060e4a84173147af618a064c464ca31640ff0` updated the selected Mac successfully to runtime `6ed9dade96417251d3dd5fc8cb175c7136682b63`; last verified P7.02/P7.05 state there was healthy;
- F06 operational verification reached runtime `470d4e310973ed873eb71d1bec3cf0985288be6b`, `CURRENT_EXACT`, `MANAGED_SPAWN_PROOF`, exact live assets PASS, and refreshed/opened launcher;
- F06 real failed start: PID `52092` reached Uvicorn startup but helper identity recognition rejected the healthy path-with-spaces command before managed proof, then gracefully cleaned up its own child;
- **F06 implementation repair:** PR `#4` merged at `3b4d2b2be4a095ff04e5703b36b3ef189c3d4057`; exact executable paths containing whitespace are space-safe, managed provenance remains strict, failed-child cleanup/readiness diagnostics are hardened;
- **F07 real owner recheck:** FAIL on a screenshot of deployed canonical `470d…`, not PR `#6`; owner could not identify what to do, scenario fixtures looked live, raw technical evidence leaked on Home, actions were secondary, and branding was unacceptable;
- **F07 remediation:** PR `#6` revises Home to live-only action-first presentation and advances the unmerged Workspace release to `p9.11.3` / contract `11`;
- owner recheck: pending after final PR review, merge, governed deployment, and launcher refresh/open;
- synthetic owner-session evidence: prohibited.

Current critical sequence:

```text
complete final review of F07 remediation PR #6
        ↓
merge and govern-deploy exact Workspace p9.11.3 / contract 11
        ↓
verify P7.02/P7.05, CURRENT_EXACT, admissible proof, and exact live assets
        ↓
refresh/open exact-release Desktop launcher
        ↓
real owner recheck
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
| E — Future customer/external readiness | second Organization/customer readiness | ⬜ Discovery only |

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
- merged F05 PR `#3`: final focused lifecycle/P7.06/P7.02 evidence `72 passed`; historical roadmap guards `4 passed`; GitHub Reference Python CI / full suite PASS on exact reviewed head `9474b846d316ed4fb038ce90a11999401b83fcc9`;
- merged F06 PR `#4`: exact `Application Support` executable/entrypoint regressions PASS, framework + managed proof reaches `CURRENT_EXACT`, framework without managed proof remains `UNKNOWN` / `NONE`, PID-reuse and historical unproven-process guards PASS, and GitHub full Reference Python CI PASS on exact reviewed head `99d4d1a130885c6a399e3077f4ac15a113d67a98`;
- local Python `3.14.7` full suite reported `1340 passed` plus two baseline failures reproduced unchanged on pre-F06 canonical `main`: one P7.05 error-message-string assertion and one macOS `/var` → `/private/var` temporary-path equivalence assertion; neither involves PR `#4` files and neither is treated as a waiver or selected-Mac readiness proof;
- no post-merge F06 selected-Mac `CURRENT_EXACT` or owner-recheck PASS is claimed;
- R32 remains locked and therefore no M9 code-health PASS is claimed.

## 8. M9 definition

M9 requires M9-alpha to remain valid plus real owner working sessions primarily through Workspace, recurring material friction disposition, real product composition and AI/Activity/company surfaces remaining valid, applicable ADR obligations satisfied, R29–R32 material findings closed, and the M9 Milestone Code Health Gate PASS.

Parallel integration progress cannot substitute for P9.11 operational evidence.

## 9. Current canonical actions

**Critical path:**

> **P9.11-F07 — complete final review of the owner-first UX remediation in PR `#6`; after merge, govern-deploy the exact release, verify exact runtime/readiness/launcher evidence, then stop at the next real owner recheck. F06 is operationally verified; F07 owner recheck failed; P9.11 remains Current and R32 remains locked.**

**Lane B:**

> **No internally executable action. Resume INT-B7 only when an exact real integration endpoint/deployment/account is available.**

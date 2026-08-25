# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.95.14`
Created: `2026-08-07`
Updated: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS sequencing and concurrency. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

## 2. Version note

Version `2.95.14` records successful governed deployment of F08 `p9.11.4` to `dc0e0cff83a9031a3686191b5cf304ee03c2d1eb`: P7.02/P7.05, exact manifest/assets, `CURRENT_EXACT`, `MANAGED_SPAWN_PROOF`, and launcher verification passed. The real owner recheck nevertheless failed: the clearer presentation still projected a preflight-only proof as an urgent owner task with no concrete requested outcome. The next candidate is `p9.11.5` / contract `11`, which removes that false owner work and retains UI4 as diagnostics.

The live `p9.11.3` Workspace was reviewed by the owner before this merge: the Home page is understandable and visually acceptable, the top-level navigation is clear, and the owner-provided Arvectum Block logo is accepted in that bounded presentation scope. F07 is therefore closed only for Home/navigation/branding.

The same real session exposed **P9.11-F08 — Task-to-Governed Action Comprehension and Actionability**. After entering the urgent task, the owner could not understand the task-detail/governed-action flow: raw English and internal governance terminology dominated the screens; `Открыть` versus `Открыть выполнение` was ambiguous and visually crowded; the focused task was duplicated in the queue so the list-level `Открыть` could appear non-functional; and the visually primary `Run governed preflight` control did not explain in plain Russian what it did or whether it was safe.

Repository review confirms the binding truthfulness boundary. The current P7.06-UI4 bridge intentionally supplies none of the four RFC-0005 action-specific decisions and exposes no consequential action request. Its preflight only re-evaluates retained evidence and records minimized owner-local non-canonical proof evidence; it requests no canonical mutation or external effect and grants no authority or approval. The current Workspace therefore has no admitted in-Workspace path to satisfy those four decisions. F08 improves owner-facing comprehension without manufacturing approval/authority controls that do not exist.

Canonical evidence:

- [`P9.11-F07 — Owner-first Workspace UX repair`](../reviews/P9-11-F07-owner-first-workspace-ux-repair.md) — `Owner recheck PASS in bounded Home/navigation/branding scope`;
- [`P9.11-F08 — Task-to-Governed Action Comprehension and Actionability`](../reviews/P9-11-F08-task-to-governed-action-comprehension.md) — `Open / owner-task eligibility repair required`.

F06 remains **operationally verified** in its bounded process-identity scope. F08 does not reopen F05/F06 and does not authorize any new effect, authority grant or decision path.

The earlier F05 one-time owner decision for historical PID `30686` remains consumed and non-reusable. Normal `UNKNOWN` Workspace listeners remain fail-closed and unsignallable without a separate exact owner decision.

`P9.11` remains Current and `R32` remains locked. The next canonical action is review and merge the bounded `p9.11.5` owner-task eligibility repair, then governed deployment and a real owner recheck. No repository test or synthetic click can substitute for that owner evidence.

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

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.13.13`.

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
| **P9.11** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current — F07 bounded PASS; F08 owner-task eligibility repair** |
| R32 | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ Locked |
| P9.12 | Phase 9 / M9 closure review | ⬜ |

### P9.11 live state

- F03 owner-first IA repair remains historical P9.11 evidence;
- F04 canonical repository identity migration is merged;
- F05 listener-lifecycle repair and one-time historical-listener reconciliation are complete in their exact scope; the PID `30686` authorization is consumed;
- F06 process-identity repair is merged and operationally verified;
- F07 implementation repair PR `#6` merged at `3e0b472a015bde7a44ac8202f364fbf5ea568ebb`, advancing Workspace to `p9.11.3` / app contract `11`;
- **F07 bounded owner recheck:** PASS for Home first-glance orientation, primary actions, top-level navigation and Arvectum branding;
- **F08 real owner finding:** FAIL for the urgent-task detail and governed-action path — raw English/internal terminology, ambiguous/crowded actions, apparent same-route `Открыть` behavior, and unclear safety/purpose of `Run governed preflight`;
- **F08 p9.11.4 deployment:** target `dc0e0cff83a9031a3686191b5cf304ee03c2d1eb` reached P7.02/P7.05 healthy, exact manifest/assets, `CURRENT_EXACT`, and `MANAGED_SPAWN_PROOF`;
- **F08 p9.11.4 owner recheck:** FAIL. UI4's preflight-only proof was still projected as high-urgency owner work despite no concrete requested action or resolution path;
- **F08 p9.11.5 candidate:** remove UI4 from ordinary attention and Activity alerts; retain it under Settings technical diagnostics, preserve the four gates and safe re-check, and keep contract `11`;
- repository inspection confirms the current preflight is non-consequential (`canonical_mutation_requested=false`, `external_effect_requested=false`, authority/approval not provided) and only records minimized local non-canonical proof evidence;
- repository inspection also confirms no admitted in-Workspace path currently exists to satisfy the four missing RFC-0005 decisions; UI must not imply otherwise or manufacture approval controls;
- next owner recheck: pending after review, merge, and governed deployment of the p9.11.5 eligibility repair;
- synthetic owner-session evidence: prohibited.

Current critical sequence:

```text
review + merge p9.11.5 owner-task eligibility repair
        ↓
governed P7.06 update selected Mac and verify exact runtime/readiness/assets/launcher
        ↓
real owner recheck of urgent-task journey
        ↓
continue ordinary daily dogfooding
        ↓
disposition recurring material friction
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
- F06 selected-Mac operational verification: P7.02/P7.05 healthy, `CURRENT_EXACT`, `MANAGED_SPAWN_PROOF`, exact live assets PASS, Desktop launcher refreshed/opened on runtime `470d4e310973ed873eb71d1bec3cf0985288be6b`;
- merged F07 PR `#6`: reviewed head `5e5db4b0dbf84774cc5915baccce5a21e109d267`; frontend `27 passed`; typecheck, no-Web-Storage guard, build and diff check PASS; Productive Workspace CI `32850241215` PASS; Reference Python CI `32850241199` PASS;
- local F07 targeted backend/reference run reported `41 passed` plus one macOS `/var` symlink-policy baseline failure reproduced on canonical `main`; it is not treated as a waiver or post-deploy readiness proof;
- real `p9.11.3` owner recheck proves F07 Home/navigation/branding improvement but also proves F08 downstream usability failure;
- merged F08 PR `#7`: reviewed head `d2949821347fc3078757303d5858a67dfdd7e23b`; frontend `32 passed`; typecheck/build/diff check PASS; Productive Workspace CI `32856696161` PASS including SPA and BFF security/context jobs; Reference Python CI `32856696061` full reference suite PASS;
- F08 p9.11.4 selected-Mac deployment passed exact runtime/readiness/assets/launcher checks, but the real owner recheck failed on the absence of a concrete owner action;
- R32 remains locked and therefore no M9 code-health PASS is claimed.

## 8. M9 definition

M9 requires M9-alpha to remain valid plus real owner working sessions primarily through Workspace, recurring material friction disposition, real product composition and AI/Activity/company surfaces remaining valid, applicable ADR obligations satisfied, R29–R32 material findings closed, and the M9 Milestone Code Health Gate PASS.

Parallel integration progress cannot substitute for P9.11 operational evidence.

## 9. Current canonical actions

**Critical path:**

> **P9.11-F08 — review and merge the bounded `p9.11.5` owner-task eligibility repair. A preflight/proof/health observation must not become owner work solely because a governance gate is Waiting; a real task requires a concrete product-owned requested outcome. Keep UI4 diagnostics available without authority or effects, then govern-deploy and stop at a real owner recheck. F07 remains bounded PASS; P9.11 remains Current and R32 remains locked.**

**Lane B:**

> **No internally executable action. Resume INT-B7 only when an exact real integration endpoint/deployment/account is available.**

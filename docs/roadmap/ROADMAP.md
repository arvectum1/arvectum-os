# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.95.1`
Created: `2026-08-07`
Updated: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing and concurrency. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.95.1` preserves `P9.11 — Real daily-use dogfooding + friction/backlog closure` as the current **critical-path** action. It records the deployed `p9.11.1` RU-first/brand repair and the new real owner finding `P9.11-F03`: the first-level taxonomy did not make a daily workflow obvious. The bounded owner-first IA implementation repair is `p9.11.2`; owner recheck remains pending.

`INT-B7 — First real connector pilot admission package` is now canonically prepared and cross-reviewed, but the pilot is **NOT ADMITTED** because no exact real 1С/CRM/СЭД/ЭДО endpoint/deployment/account has been supplied. The integration block is therefore `Internally complete / operational continuation externally blocked`.

No synthetic endpoint, credential, metadata, failure result or pilot evidence may be created merely to make the lane appear complete. When an exact real endpoint becomes available, Lane B resumes by populating and executing the existing INT-B7 package rather than inventing a new planning task.

M9-alpha remains achieved and P9.07–P9.10 plus R31 remain `Complete / PASS`. P9.11 depends materially on real owner working sessions; bounded parallel work remains permitted only where it does not falsify or bypass required evidence.

Canonical parallel-workstream plan: [`PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md`](PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md) `1.0.0`.

This update does not create a new numbered phase, public/stable connector/API/SDK, customer Production, Stable Product Contract, Active Platform Capability, SLA/support/certification or broader conformance claim.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- `ADR-0001 — Productive Workspace Browser Application Topology` — `Accepted 2026-08-21` for the exact internal Phase 9 application topology;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02, P6.06, P8.03 and P8.06 Product Contracts remain Provisional within their exact scopes;
- operating environment remains `Local / Persistent Internal / owner-operated` with scoped conformance;
- no public/stable SDK/API/wire/browser/connector surface, external/customer Production, SLA/support/certification or broader conformance claim exists.

## 4. Strategic roadmap

| Phase | Strategic scope | Status | Milestone |
|---|---|---:|---|
| `Phase 0` | Foundation / Architecture Bootstrap | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | 🟩 Complete | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | 🟩 Complete | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | 🟩 Complete / PASS | `M6` Real-product validation across materially distinct workflows |
| `Phase 7` | Operational / Enterprise Readiness | 🟩 Complete / PASS | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | 🟩 Complete / PASS | `M8` Governed external ecosystem baseline — exact activated one-Organization scope |
| **`Phase 9`** | **Productive Workspace & Daily Operations** | **🟨 Active** | **`M9` Daily-use organizational workbench** |

## 5. Active Phase 9 — Productive Workspace & Daily Operations

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.13.0`.

| ID | Work item | Status |
|---|---|---:|
| `P9.00` | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS |
| `P9.01` | Real operator jobs-to-be-done + acceptance journeys | 🟩 Complete / PASS |
| `P9.02` | Application architecture spike + frontend/BFF/session decision | 🟩 Complete / PASS |
| `R29` | Productive Workspace Boundary Review | 🟩 Complete / PASS |
| `P9.03` | Real application shell + navigation + organization/user context | 🟩 Complete / PASS |
| `P9.04` | `My Work` / Needs Attention projection | 🟩 Complete / PASS |
| `P9.05` | Human-friendly Records / Documents / Knowledge + global search | 🟩 Complete / PASS |
| `P9.06` | Executions / Decisions / governed actions UX | 🟩 Complete / PASS |
| `R30` | M9-alpha Usability / Information Architecture Review | 🟩 Complete / PASS |
| `M9-alpha` | Usable Internal Workspace | 🟩 Achieved / PASS |
| `P9.07` | Product-owned workspace surfaces / composition | 🟩 Complete / PASS |
| `P9.08` | Arvectum AI Copilot + source-grounded organizational assistance | 🟩 Complete / PASS |
| `P9.09` | Activity, notifications and attention routing | 🟩 Complete / PASS |
| `P9.10` | ООО «Арвектум» organization composition | 🟩 Complete / PASS |
| `R31` | Product Composition / AI Safety Review | 🟩 Complete / PASS |
| **`P9.11`** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current — implementation ready / real sessions pending** |
| `R32` | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ gate |
| `P9.12` | Phase 9 / M9 closure review | ⬜ |

P9.11 remains the critical path to M9. The `p9.11.0` internal Workspace release contains the bounded real-session Observation/backlog mechanism; `p9.11.1` repaired RU-first/brand presentation and `p9.11.2` repairs owner-first information architecture. Synthetic owner-session evidence is not accepted; none of these implementation repairs closes P9.11 before owner recheck.

## 6. Parallel development lanes

Detailed concurrency rules and boundaries: [`PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md`](PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md).

| Lane | Scope | Status | May progress during P9.11? |
|---|---|---:|---:|
| **A — Productive Workspace dogfooding** | real UI use, friction capture/repair, P9.11 → R32 → P9.12 | 🟨 Critical path | yes — primary |
| **B — Russian-market integrations** | portfolio/design/security gate + first real connector admission boundary | 🟦 Internally complete / operational continuation externally blocked | only when exact real endpoint exists |
| **C — Product ↔ Workspace composition** | Tender/Discount/Creative/Proxy product-owned projections and governed entry points | 🟦 Available | yes, within Product Contract/product-local boundaries |
| **D — Reliability / DX / technical debt** | CI, dependencies, observability, recovery regressions, evidence-backed cleanup | 🟦 Continuous | yes |
| **E — Future external/customer readiness** | second-Organization/customer/deployment/regulatory discovery only | ⬜ Discovery | yes, no customer-Production implementation |

### 6.1 Lane A — current critical path

Current action:

> **P9.11 — Real daily-use dogfooding + friction/backlog closure.**

The owner uses the Productive Workspace for real work, records friction, and validates whether ordinary work can remain inside the Workspace rather than escaping to terminal/GitHub/internal identifiers. Material defects are fixed as they appear. R32 remains locked until real-session evidence and backlog disposition satisfy P9.11.

### 6.2 Lane B — Russian-market integration block

Canonical integration sequence and state:

1. `INT-B1 — Integration portfolio baseline` — **Complete / PASS**;
2. `INT-B2 — Domain-neutral connector boundary pattern` — **Complete / PASS**;
3. `INT-B3 — 1С first-candidate design` — **Complete / PASS**;
4. `INT-B4 — CRM designs` — **Complete / PASS**;
5. `INT-B5 — СЭД/ECM/ЭДО design` — **Complete / PASS**;
6. `INT-B6 — Integration security/reliability review` — **Complete / scoped PASS** for bounded read-only pilot admission;
7. [`INT-B7 — First real connector pilot admission package`](../architecture/INT-B7-first-real-connector-pilot-admission-package.md) `1.0.0` — **Prepared / blocked on exact real endpoint**; cross-review [`INT-B7 functional cross-review`](../reviews/INT-B7-functional-cross-review.md) — **PASS for package completeness / pilot NOT ADMITTED**, 3 of maximum 7 iterations.

The current Lane-B block has no further internally executable task. `INT-B8` is not invented because the existing roadmap has no evidence-based need for one before a real pilot exists.

#### INT-B7 prepared material

The prepared package already contains:

- preferred first candidate: `1С:ERP 2.5` read-only procurement projection;
- bounded outcome statement;
- exact read-only operation allowlist;
- endpoint intake record/schema;
- external-authority and Organization binding requirements;
- dedicated least-privilege credential requirements without storing secrets;
- data-purpose/classification/minimization/retention/deletion/portability intake;
- compatibility discovery procedure;
- freshness/completeness and stale-state requirements;
- authentication/authorization/network/source/pagination/schema/credential failure-test matrix;
- deterministic duplicate/reconciliation requirements;
- connector disable/termination test;
- Product Contract gate;
- ADR trigger disposition;
- explicit current decision `NOT ADMITTED` while the real endpoint is absent.

#### Resume condition

Lane B resumes only when an exact real binding exists for one of the already-designed candidates, preferably the INT-B3 `1С:ERP 2.5` candidate:

- actual deployment/account/portal/box identity;
- actual reachable integration endpoint;
- actual deployment/API/configuration metadata;
- dedicated least-privilege integration principal/credential binding;
- concrete bounded data scope and purpose.

At that point the existing INT-B7 package is populated and executed. Real evidence then determines whether the pilot is admitted. No synthetic customer/deployment evidence is acceptable.

All business writes/effects remain closed: 1С posting/writes/payments, CRM writes/stage transitions, Directum approvals/workflow mutation, Диадок signing/sending/annulment and arbitrary vendor API passthrough require later operation-specific governed design and authority gates.

## 7. Concurrency map

```text
                         ┌─ Lane A: P9.11 real UI dogfooding ──→ R32 ─→ P9.12/M9
                         │
current canonical main ──┼─ Lane B: internally complete
                         │          └─ resume INT-B7 only on exact real endpoint
                         │
                         ├─ Lane C: product ↔ Workspace composition
                         ├─ Lane D: reliability / DX / technical debt
                         └─ Lane E: future external/customer discovery
```

Only Lane A is on the current critical path to M9. Parallel lanes must revalidate against current `main` before merge and must not silently change shared Workspace/BFF/session/security or connector-contract boundaries.

## 8. M9 definition

`M9 — Daily-use organizational workbench` requires:

- M9-alpha remains valid;
- at least two real product-owned surfaces composed through explicit boundaries;
- source-grounded, uncertainty-aware and authority-safe AI Copilot;
- non-authoritative activity/notification projections;
- useful ООО «Арвектум» company-level composition without Kernel product/company leakage;
- real owner working sessions completed primarily through Workspace;
- recurring usability friction dispositioned;
- applicable ADR obligations satisfied;
- R29–R32 material findings closed or explicitly accepted;
- pre-closure M9 Milestone Code Health Gate PASS.

Parallel integration progress is not itself an M9 closure criterion and therefore cannot replace P9.11 evidence.

## 9. Current canonical actions

**Critical path:**

> **P9.11 — Real daily-use dogfooding + friction/backlog closure.**

**Lane B:**

> **No current internally executable action. INT-B7 is prepared and blocked on an exact real endpoint.**

When the external prerequisite becomes available, resume the existing INT-B7 package. Until then, do not create synthetic pilot evidence and do not invent a follow-on integration task merely to keep the lane active.

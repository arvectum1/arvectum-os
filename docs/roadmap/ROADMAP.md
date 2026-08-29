# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.97.4`
Created: `2026-08-07`
Updated: `2026-08-29`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS sequencing and concurrency. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase evidence remains in the corresponding phase roadmaps, reviews, decisions and repository history rather than being duplicated indefinitely here.

## 2. Version note

Version `2.97.4` closes [`P10.04 — Company Asset Library UX + version/handling lifecycle`](../reviews/P10-04-company-asset-library-closure-review.md) as `Complete / PASS` for its exact bounded internal owner-facing/reference-runtime scope and advances the critical path to `P10.05 — Reviewed generated-output promotion boundary`.

P10.04 exposes the P10.03 governed Organizational Asset admission path through Productive Workspace without creating a new authority surface. Four truthful lifecycle views separate staged drafts/review from canonical accepted/superseded history; exact version/digest/handling is reviewed before admission; productive admission requires a separate exact P7.04 `company.asset.admit-staged-version` authorization grant and independently evaluated Actor Assurance, Organizational Authority, Data Governance, Validation and Consequential Approval; canonical mutation remains exclusively behind the P10.03 guarded entrypoint; immutable version/currentness/supersession and canonical Document/designation/Event provenance remain reconstructable in the bounded runtime; bounded export remains Organization-scoped; and Company DOCX generation requires an exact admitted source while the generated result remains `TransientOutput`.

P10.04 retains the P10.03 no-new-durable-mechanism boundary: no database, object store, durable transaction manager/idempotency ledger, stable serialization/wire contract, public API/SDK or separate service topology is selected. Therefore P10.04 does not claim restart-durable canonical persistence, M10-alpha, P10.05 generated-output promotion, customer Production or broader conformance.

P10.01 authority/admission and real-work source semantics remain recorded in [`P10-01-asset-admission-real-work-authority-matrix`](../reviews/P10-01-asset-admission-real-work-authority-matrix.md) — `Complete / PASS`.

P10.02 remains lifecycle-current [`Provisional 0.2.0`](../contracts/P10-02-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.2.0.md), approved in [`DECISION-2026-08-27-P10-02-PROVISIONAL-APPROVAL`](../governance/decisions/DECISION-2026-08-27-P10-02-PROVISIONAL-APPROVAL.md) and closed by [`P10-02-product-contract-publication-closure`](../reviews/P10-02-product-contract-publication-closure.md) — `Complete / PASS`.

The owner-approved Product Contract substance remains exact Draft blob `a92c1d1aac54d565d3d32ce746925620c9d1fd12`. P10.04 does not alter that contract, promote it to `Stable`, promote CAP-001 to `Active`, establish customer Production or broaden conformance/support commitments.

Phase 10 remains grounded in real M9/F11 evidence:

- Company materials can be received as `StagedNonCanonical` and P10.04 now presents the bounded governed admission lifecycle through Workspace;
- P10.03 provides the bounded domain-neutral canonical admission path and P10.04 provides the bounded owner-facing composition, but M10-alpha still requires a real owner-operated Workspace asset cycle;
- generated document output remains `TransientOutput` by default;
- generated-output promotion is contractually bounded but remains unavailable for real reliance until P10.05 implementation/review;
- M9 proved a usable owner-operated Workspace but did not prove the full real organizational-asset lifecycle or a naturally occurring genuine task → governed-action loop;
- the first natural genuine action remains the truthful deferred F08 recheck and is carried into Phase 10 without synthetic evidence.

This roadmap update creates no Constitution/RFC amendment, new Kernel primitive, public/stable API/browser contract, customer Production, Stable Product Contract, Active Platform Capability, SLA/support/certification or broader conformance claim.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Productive Workspace Browser Application Topology`, `Accepted 2026-08-21`;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- Arvectum Company ↔ Productive Workspace Product Contract is lifecycle-current `Provisional 0.2.0` for its exact declared scope;
- R33, P10.03 and P10.04 are `Complete / PASS` inside the R33/P10.02 constraints;
- operating environment remains `Local / Persistent Internal / owner-operated` with scoped conformance;
- current canonical repository for new checkouts/deployments is `arvectum1/arvectum-os`;
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
| `Phase 8` | Ecosystem and External Integration | 🟩 Complete / PASS | M8 — exact activated one-Organization scope |
| `Phase 9` | Productive Workspace & Daily Operations | 🟩 Complete / PASS | `M9 — Daily-use organizational workbench` |
| **`Phase 10`** | **Operational Work & Organizational Assets** | **🟨 Active** | **`M10 — Governed Daily Operations Baseline`** |

## 5. Completed Phase 9 baseline

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Complete / PASS 1.14.0`.

Closure review: [`P9-12-phase-9-m9-closure-review.md`](../reviews/P9-12-phase-9-m9-closure-review.md) — `Complete / PASS`.

`M9 = Achieved / PASS` only for the exact `Local / Persistent Internal / owner-operated` Productive Workspace scope.

The first naturally occurring genuine actionable task still rechecks the repaired F08 task-detail → governed-action journey. No synthetic natural task evidence is admitted.

## 6. Active Phase 10 — Operational Work & Organizational Assets

Detailed roadmap: [`PHASE-10-OPERATIONAL-WORK-ORGANIZATIONAL-ASSETS.md`](PHASE-10-OPERATIONAL-WORK-ORGANIZATIONAL-ASSETS.md) — `Active`.

Activation decision: [`DECISION-2026-08-27-PHASE-10-OPERATIONAL-WORK-ACTIVATION`](../governance/decisions/DECISION-2026-08-27-PHASE-10-OPERATIONAL-WORK-ACTIVATION.md) — `Approved`.

### 6.1 Milestones

- `M10-alpha — First Governed Company Asset Cycle`;
- `M10 — Governed Daily Operations Baseline`.

M10-alpha requires one real Company-owned material to move through staged receipt → explicit owner review → Governed Execution canonical admission → immutable asset/version/provenance → later retrieval/use through Workspace.

M10 additionally requires at least one naturally occurring genuine product/company action to move through owner-facing actionable context → current server-side authority/gate revalidation → Governed Execution → truthful completed/blocked/failed/uncertain result with reconstruction evidence.

### 6.2 Work breakdown

| ID | Work item | Status |
|---|---|---:|
| `P10.00` | Post-M9 outcome selection + Phase 10 activation baseline | 🟩 Complete / PASS |
| `P10.01` | Asset/admission + real-work authority matrix | 🟩 Complete / PASS |
| `P10.02` | Product Contract evolution for Company assets + operational work | 🟩 Complete / PASS — `Provisional 0.2.0` effective |
| `R33` | Asset / Product Contract / Authority Boundary Review | 🟩 Complete / PASS — 6 iterations |
| **`P10.03`** | **Domain-neutral organizational-asset admission execution path** | **🟩 Complete / PASS** |
| **`P10.04`** | **Company Asset Library UX + version/handling lifecycle** | **🟩 Complete / PASS** |
| **`P10.05`** | **Reviewed generated-output promotion boundary** | **🟨 Current** |
| `R34` | M10-alpha Asset Governance / Usability Review | ⬜ gate |
| `M10-alpha` | First Governed Company Asset Cycle | ⬜ |
| `P10.06` | Real Action Request / Actionable Work boundary | ⬜ |
| `P10.07` | First real governed operational action | ⬜ — waits for genuine request |
| `P10.08` | Product operational entry-point composition | ⬜ |
| `R35` | Operational Work / Product Boundary / AI Authority Review | ⬜ gate |
| `P10.09` | Source-grounded use of admitted assets in Workspace / AI / generation | ⬜ |
| `P10.10` | Real daily-operations dogfooding + friction closure | ⬜ |
| `P10.11` | Lifecycle / platform-reuse / capability disposition | ⬜ |
| `R36` | M10 Hardening + Milestone Code Health Gate | ⬜ gate |
| `P10.12` | Phase 10 / M10 closure review | ⬜ |

### 6.3 Critical-path sequencing

```text
P10.01 ✓
   ↓
P10.02 ✓
   ↓
R33 ✓
   ↓
P10.03 ✓
   ↓
P10.04 ✓
   ↓
P10.05 ← CURRENT
   ↓
R34
   ↓
M10-alpha
   ↓
P10.06 → P10.07 → P10.08
   ↓
R35
   ↓
P10.09 → P10.10 → P10.11
   ↓
R36
   ↓
P10.12 / M10
```

P10.06 design may overlap the asset stream because P10.01 semantics are fixed and the Product Contract is effective, but P10.07 cannot execute until the applicable owning-product Product Contract is effective and a genuine action request naturally exists.

## 7. Phase 10 authority boundaries

### 7.1 Organizational assets

- `StagedNonCanonical` receipt is not canonical admission;
- generated output remains `TransientOutput` by default;
- canonical Company asset/version admission is a consequential canonical mutation through RFC-0005 Governed Execution;
- admitted documents/assets do not automatically become RFC-0007 validated Knowledge;
- historical immutable versions are not overwritten;
- asset handling remains Organization/access/classification/purpose/rights/retention/deletion constrained;
- P10.03 supplies the bounded domain-neutral admission execution path and P10.04 supplies the owner-facing/product composition while keeping Company taxonomy product-owned and all unresolved required evidence fail-closed.

### 7.2 Real work

Phase 10 does not create a universal Kernel `Task` primitive.

Concrete requests remain product/company-owned. Workspace may provide a domain-neutral non-authoritative Actionable Work projection, but it cannot invent urgency, responsibility, permission, approval or Organizational Authority.

### 7.3 Product Contract

The lifecycle-current Company Workspace Product Contract is `Provisional 0.2.0` for the exact owner-approved boundary. It admits Company asset canonical-admission semantics and bounded Actionable Work/product-entry semantics, but actual downstream consequential product effects still require the owning product's exact effective Product Contract and governed operation.

P10.03/P10.04 remain inside the R33-reviewed `0.2.0` boundary; no Product Contract `0.2.1` was required.

### 7.4 AI

AI may retrieve, explain, summarize, compare, draft and propose. It cannot independently admit assets, approve consequential actions, create authority or promote documents into validated Knowledge.

## 8. Parallel lanes

| Lane | Scope | Status |
|---|---|---:|
| **A — Organizational Assets** | P10.03–P10.05 → R34 → M10-alpha | 🟨 P10.05 current |
| **B — Real Operational Work** | P10.06–P10.08 → R35 | 🟦 design available; real execution waits genuine request + applicable contract |
| **C — Product ↔ Workspace** | product-owned operational surfaces/entry points | 🟦 bounded on Product Contract/product-local evidence |
| **D — External integrations** | existing INT-B7 real connector pilot | ⏸ blocked on exact real endpoint/deployment/account |
| **E — Reliability / DX / technical debt** | CI, recovery, observability, dependency/security, evidence-backed refactoring | 🟦 continuous |

### Lane D — integration state

INT-B1 through INT-B6 are complete/scoped PASS. INT-B7 is prepared and cross-reviewed but the pilot remains `NOT ADMITTED` until an exact real 1С/CRM/СЭД/ЭДО endpoint/deployment/account and least-privilege credential binding exist.

Preferred prepared candidate remains a bounded read-only `1С:ERP 2.5` procurement projection. Do not invent INT-B8 or synthetic endpoint evidence merely to keep the lane moving.

## 9. M10 closure definition

M10 requires:

1. M10-alpha remains valid with a real governed Company asset cycle;
2. receipt/staging, canonical admission and generated-output promotion remain distinct;
3. immutable asset versions/provenance/authority/handling are reconstructable;
4. owner can perform ordinary asset work through Workspace without terminal/GitHub/internal identifiers;
5. one genuine action reaches a truthful governed outcome or truthful blocked/failed/uncertain state with complete reconstruction evidence;
6. Actionable Work does not manufacture tasks/urgency/authority;
7. effective Product Contracts cover actual platform reliance;
8. product business semantics remain product-owned;
9. AI remains proposal/source-grounded and does not become authority or Knowledge-promotion source;
10. external source-of-truth declarations remain intact;
11. real daily-operations dogfooding has no unresolved material closure blockers;
12. R33–R36 material findings are closed or properly dispositioned;
13. M10 Milestone Code Health Gate passes before closure.

If no genuine action naturally exists, Phase 10 may reach M10-alpha and remain Active rather than fabricating P10.07 evidence.

## 10. Current canonical actions

**Critical path:**

> **P10.05 — Reviewed generated-output promotion boundary.**

Extend the exact-version generation journey so a generated `TransientOutput` can be explicitly reviewed and either rejected/kept transient or requested for governed promotion. Any promotion must create a new governed Company Document/Asset version only through the applicable Product Contract and RFC-0005 Governed Execution path, preserve exact admitted input/output/provenance and handling evidence, and remain distinct from RFC-0007 validated Knowledge, legal approval, signing, external send or publication.

**Parallel integrations:**

> **No internally executable INT-B follow-on. Resume INT-B7 only when an exact real external endpoint/deployment/account exists.**
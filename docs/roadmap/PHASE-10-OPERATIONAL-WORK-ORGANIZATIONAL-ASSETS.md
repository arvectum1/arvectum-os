# Arvectum OS Phase 10 — Operational Work & Organizational Assets

Status: `Active`
Version: `1.0.2`
Created: `2026-08-27`
Updated: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`, `product_specific` and `governance`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Predecessor: `Phase 9 / M9 — Complete / PASS`
Milestone: `M10 — Governed Daily Operations Baseline`
Intermediate milestone: `M10-alpha — First Governed Company Asset Cycle`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `Accepted 1.0.0`; ADR-0001 `Accepted`
Activation decision: [`DECISION-2026-08-27-PHASE-10-OPERATIONAL-WORK-ACTIVATION`](../governance/decisions/DECISION-2026-08-27-PHASE-10-OPERATIONAL-WORK-ACTIVATION.md)
Activation review: [`P10-00-post-M9-outcome-selection-and-phase-10-activation.md`](../reviews/P10-00-post-M9-outcome-selection-and-phase-10-activation.md)

## 0. Version note

Version `1.0.2` records [`R33 — Asset / Product Contract / Authority Boundary Review`](../reviews/R33-asset-product-contract-authority-boundary-review.md) as `Complete / PASS after 6 iterations` and advances the Phase 10 critical path to `P10.03 — Domain-neutral organizational-asset admission execution path`.

R33 found no material conflict requiring Product Contract `0.2.1`, a new foundational RFC, a new ADR merely for the review, or any lifecycle promotion. It fixed mandatory P10.03 implementation constraints:

- Company asset taxonomy and `company.*` product semantics remain product-owned and must not become Kernel/CAP-001 business semantics;
- `StagedNonCanonical`, canonical Document/Asset state and generated `TransientOutput` remain distinct;
- canonical admission remains RFC-0005 Governed Execution with separate Authorization, Organizational Authority, Data Governance, validation and Consequential Approval;
- because Decision Authority Policy remains `Proposed` and no exact delegation is approved, first-slice admission retains explicit owner Organizational Authority/approval;
- external authority remains `External Reference` where declared;
- unresolved required purpose/classification/rights/retention/deletion state fails closed rather than being invented by implementation;
- browser/BFF/projection/AI remain non-authoritative;
- P10.03 must reopen the ADR gate before material reliance on a new durable persistence/object-store/transaction/evidence-integrity/stable-serialization/separate-service mechanism.

Canonical P10.01 evidence: [`P10-01-asset-admission-real-work-authority-matrix`](../reviews/P10-01-asset-admission-real-work-authority-matrix.md) — `Complete / PASS`.

Canonical P10.02 evidence:

- exact reviewed Draft `0.2.0` blob `a92c1d1aac54d565d3d32ce746925620c9d1fd12`;
- [`DECISION-2026-08-27-P10-02-PROVISIONAL-APPROVAL`](../governance/decisions/DECISION-2026-08-27-P10-02-PROVISIONAL-APPROVAL.md) — `Approved`;
- [`P10-02-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.2.0`](../contracts/P10-02-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.2.0.md) — lifecycle-current `Provisional 0.2.0`;
- [`P10-02-product-contract-publication-closure`](../reviews/P10-02-product-contract-publication-closure.md) — `Complete / PASS`.

R33 does not alter the approved Product Contract substance and does not establish P10.03 implementation PASS, Stable Product Contract status, Active Platform Capability status, customer Production or broader conformance/support commitments.

## 1. Purpose

Phase 9 proved that the private owner-operated Productive Workspace is usable as a daily organizational workbench. It also exposed the next practical gap: ordinary company work still stops at the boundary between useful presentation and governed organizational state/action.

Phase 10 converts the Workspace from a primarily observational/productive shell into a place where ООО «Арвектум» can safely perform two real organizational loops:

1. **Organizational Asset loop** — receive or create a real company material, review it, explicitly admit it where appropriate, preserve immutable version/provenance/handling semantics, find it later and use its exact version in subsequent work.
2. **Operational Work loop** — receive or identify a genuine product/company action request, understand it in Workspace, perform the permitted governed action through the applicable Product Contract and Governed Execution path, and see the truthful result/reconciliation state.

The Phase 10 governing question is:

> Can the owner perform useful real company work through Arvectum OS such that important company materials and consequential actions become durable, governed, reconstructable organizational state without requiring GitHub/terminal/internal identifiers on the ordinary path and without granting the UI or AI undeclared authority?

Phase 10 is intentionally internal-first. It is not a public-SaaS, multi-tenant, customer-Production, public-API or capability-promotion phase.

## 2. Post-M9 evidence base

Phase 10 starts from these canonical facts:

- `Phase 9 / M9 = Complete / Achieved — PASS` in the exact `Local / Persistent Internal / owner-operated` scope;
- Productive Workspace release at the M9 closure baseline is `p9.11.10`, internal application contract `11`;
- F11 proved useful owner-local `StagedNonCanonical` Company material intake, exact version/digest/provenance retention and exact-version DOCX generation as `TransientOutput`;
- F11 Product Contract `Provisional 0.1.0` remains immutable historical evidence; P10.02 evolved the same contract lineage to lifecycle-current `Provisional 0.2.0` for bounded canonical Company asset-admission and operational-entry semantics;
- R33 has now passed the exact asset/Product Contract/authority boundary for P10.03 implementation, with mandatory constraints retained below;
- generated-output promotion is contractually bounded by `0.2.0` but remains unavailable for real reliance until P10.05 implementation/review;
- F08 false-task projection was repaired; the first naturally occurring genuine actionable task still remains the truthful real-world recheck of task-detail → governed-action comprehension;
- CAP-001 through CAP-004 remain `Incubating / Provisional` unless separately governed;
- no Product Contract is promoted to `Stable` and no capability to `Active` by R33 closure;
- Lane B integration design is internally complete through prepared INT-B7, but a real connector pilot remains blocked on an exact external endpoint/deployment/account.

Phase 10 uses these facts as evidence rather than reopening completed M9 work.

## 3. Binding architectural boundaries

### 3.1 Organizational Asset is a designation, not a new Kernel primitive

RFC-0002 and RFC-0008 govern the asset/document model. Phase 10 MUST NOT create a sixth Kernel primitive or infer a mandatory physical database/inheritance model.

A staged upload, generated artifact, preview, cache, extracted text or AI result does not become a Governed Organizational Asset merely because it exists or is useful.

Canonical admission is explicit and versioned.

### 3.2 Receipt/generation is separate from canonical admission

The existing F11 flow may receive real Company material into `StagedNonCanonical` state and may generate exact-version `TransientOutput`.

Canonical admission of a Company material/version is a consequential canonical mutation and MUST occur only through the admitted RFC-0005 Governed Execution path with current applicable checks for:

- Authentication/session identity context where relevant;
- Authorization;
- Organizational Authority;
- Data Governance;
- validation/review requirements;
- Consequential Approval where applicable;
- exact Product Contract version;
- exact material/content/version inputs.

### 3.3 Product Contract before new governed reliance

The lifecycle-current Company Workspace Product Contract is `Provisional 0.2.0` for the exact owner-approved Draft blob `a92c1d1aac54d565d3d32ce746925620c9d1fd12`.

It admits the minimum sufficient boundary for:

- Company asset canonical admission operations;
- external-reference admission preserving external authority;
- the later reviewed generated-output promotion boundary, with real reliance deferred until P10.05;
- non-authoritative Actionable Work projection;
- no-side-effect Workspace product-operation entry/routing.

Actual downstream consequential product actions still require the owning product's exact effective Product Contract and product-owned governed workflow/operation. R33 confirms that P10.03 may implement only the domain-neutral asset-admission part of this boundary.

### 3.4 No universal Task primitive by default

Phase 10 does not introduce a universal Kernel `Task` type.

Concrete action requests remain product/company-owned unless evidence proves a reusable domain-neutral platform responsibility. Workspace may expose a domain-neutral **Actionable Work projection** over explicit product/company-owned requests and Governed Execution state, but the projection is non-authoritative and cannot manufacture work, urgency, permission or Organizational Authority.

### 3.5 AI remains proposal/execution assistance

AI may classify, summarize, draft, compare, retrieve and propose actions or asset metadata. It MUST NOT silently:

- admit an asset into canonical state;
- approve an organizational asset;
- create Organizational Authority;
- mark a product action as approved;
- promote document contents into validated Knowledge;
- broaden retention/reuse/Organization scope;
- execute a consequential external effect outside the applicable Governed Execution path.

## 4. Milestone definitions

### M10-alpha — First Governed Company Asset Cycle

M10-alpha is achieved only when a real Company-owned material completes the following live owner-operated journey through Workspace:

1. receive/upload the real material into staged non-canonical state;
2. inspect exact version, digest, provenance, classification/handling and intended Company role;
3. explicitly review the material for admission;
4. perform admitted Governed Execution for canonical asset/version admission;
5. verify immutable canonical identity/version and provenance;
6. find/open the admitted asset later through ordinary Workspace navigation/search;
7. use the exact admitted version as an input to one subsequent bounded real work item, such as generating a Company document;
8. preserve the generated result as `TransientOutput` unless a separate admitted promotion occurs.

No terminal, GitHub or internal identifier knowledge may be required for the ordinary owner path.

### M10 — Governed Daily Operations Baseline

M10 requires both:

- the governed Company asset lifecycle to be useful in real work; and
- at least one naturally occurring genuine product/company action to complete end-to-end from owner-facing actionable context through current Governed Execution and truthful outcome/reconciliation.

M10 does not require customer Production, public interfaces, multi-Organization operation, Stable Product Contracts or Active Platform Capabilities.

## 5. Work breakdown

| ID | Work item | Status | Exit outcome |
|---|---|---:|---|
| `P10.00` | Post-M9 outcome selection + Phase 10 activation baseline | 🟩 Complete / PASS | Phase 10 bounded scope, milestone, non-goals and gates activated |
| `P10.01` | Asset/admission + real-work authority matrix | 🟩 Complete / PASS | exact subject classes, authority modes, owner decisions, retention/classification, action-request sources and consequentiality matrix fixed |
| `P10.02` | Product Contract evolution for Company assets + operational work | 🟩 Complete / PASS — `Provisional 0.2.0` | effective minimum-sufficient Provisional boundary exists before governed reliance |
| `R33` | Asset / Product Contract / Authority Boundary Review | 🟩 Complete / PASS — 6 iterations | no hidden authority, product leakage, competing truth or accidental stable/public surface; P10.03 constraints fixed |
| **`P10.03`** | **Domain-neutral organizational-asset admission execution path** | **🟨 Current** | staged material can enter canonical asset history only through explicit Governed Execution |
| `P10.04` | Company Asset Library UX + version/handling lifecycle | ⬜ | owner can review, admit, find, inspect, supersede/version and export/download admitted assets through Workspace |
| `P10.05` | Reviewed generated-output promotion boundary | ⬜ | generated `TransientOutput` can be reviewed and, only when admitted, promoted to a governed Company document/asset version |
| `R34` | M10-alpha Asset Governance / Usability Review | ⬜ gate | real asset cycle safe, understandable and reconstructable |
| `M10-alpha` | First Governed Company Asset Cycle | ⬜ | first real asset cycle owner PASS |
| `P10.06` | Real Action Request / Actionable Work boundary | ⬜ | concrete product/company requests can appear truthfully without a universal Task primitive |
| `P10.07` | First real governed operational action | ⬜ — waits genuine request | one natural genuine action reaches Governed Execution and truthful terminal/uncertain state |
| `P10.08` | Product operational entry-point composition | ⬜ | Workspace can start/continue admitted product-owned actions without embedding product business logic in platform |
| `R35` | Operational Work / Product Boundary / AI Authority Review | ⬜ gate | action semantics, authority and product ownership remain correct |
| `P10.09` | Source-grounded use of admitted assets in Workspace / AI / generation | ⬜ | exact admitted assets can be retrieved/used with provenance without automatic Knowledge promotion |
| `P10.10` | Real daily-operations dogfooding + friction closure | ⬜ | owner completes real asset + action work primarily through Workspace and dispositions material friction |
| `P10.11` | Lifecycle / platform-reuse / capability disposition | ⬜ | evidence-based keep-incubating/promote/defer/contain decisions; no automatic Active/Stable transition |
| `R36` | M10 Hardening + Milestone Code Health Gate | ⬜ gate | security, supply chain, maintainability, recoverability, UX and code-health PASS |
| `P10.12` | Phase 10 / M10 closure review | ⬜ | exact-scope M10 closure or explicit non-closure |

## 6. P10.00 — activation result

P10.00 is `Complete / PASS` because:

- M9 is canonically closed and the master roadmap explicitly requires a separate governed activation for any successor numbered phase;
- real M9/F11 evidence demonstrates a concrete post-M9 gap rather than a speculative platform idea;
- the owner explicitly directed creation and implementation of a detailed Phase 10 roadmap;
- the scope is bounded to the existing internal owner-operated environment;
- the phase reuses Accepted RFC-0002/0004/0005/0007/0008 semantics rather than requiring a Constitution or foundational RFC change;
- new Product Contract scope is governed through P10.02 before new implementation reliance;
- capability lifecycle promotion is not implied by activation;
- the work remains reversible and evidence-driven.

## 7. P10.01 — Asset/admission + real-work authority matrix

P10.01 is `Complete / PASS` in [`P10-01-asset-admission-real-work-authority-matrix`](../reviews/P10-01-asset-admission-real-work-authority-matrix.md).

### Purpose

Fix the exact organizational and authority meaning before writing admission/action code.

### P10.01-A — real Company asset classes

The first-slice classes are bounded to:

- brandbook;
- logo/brand assets;
- Company document templates;
- Company source/reference materials;
- governed external references;
- project-bound generated documents considered for internal acceptance only through the later explicit promotion path.

For each class the P10.01 matrix fixes or requires the owner/product semantic role, authority mode, classification/purpose, rights basis, retention/deletion expectation, versioning/supersession semantics, parsing/extraction boundary and Knowledge non-promotion rule.

### P10.01-B — admission decision matrix

For every first-slice admission operation the matrix separates:

- Authentication/Actor resolution;
- Authorization;
- Organizational Authority;
- Data Governance;
- validation/review;
- Consequential Approval;
- exact inputs/version pins;
- canonical state/effect;
- resulting Event/provenance evidence;
- failure/cancellation/retry behavior.

The current owner-operated flow may be simple, but no UI button or session may collapse these distinctions.

### P10.01-C — generated-output decision matrix

Lifecycle remains:

`TransientOutput → owner review → reject / keep transient / request governed promotion`.

No generated result is canonical merely because the owner downloaded or opened it.

### P10.01-D — real Action Request source classes

Eligible source classes include:

- a Company document/asset review/admission request;
- a Tender Operator/Tender Agent result requiring owner disposition where its own effective Product Contract admits the operation;
- a Discount Parser controlled publication/approval request where its own effective Product Contract admits the operation;
- another explicit product-owned request with a truthful product/canonical source.

Chat/model suggestion alone does not create a governed request. No synthetic request is created solely to satisfy M10.

### P10.01-E — selection of first action journey

The first real action remains unselected until a genuine request exists. The repaired F08 journey remains eligible for natural recheck only when such a request appears.

### Exit result

P10.01 PASS establishes complete R33 inputs without implementing canonical admission or fabricating real-action evidence.

## 8. P10.02 — Product Contract evolution

P10.02 is `Complete / PASS` for Product Contract definition/publication.

The existing Arvectum Company ↔ Productive Workspace Product Contract Subject lineage was evolved from historical `Provisional 0.1.0` to lifecycle-current `Provisional 0.2.0` rather than creating an unrelated contract.

The exact owner-approved Draft blob is:

`a92c1d1aac54d565d3d32ce746925620c9d1fd12`

The effective Provisional contract declares:

- canonical Company asset admission operations;
- allowed asset classes and explicit exclusions;
- CAP-001 reliance and exact governed asset/document semantics;
- exact Governed Execution operation/effect classes;
- Company-owned semantic roles and approval rules;
- staging versus canonical state boundary;
- generated-output review/promotion semantics;
- actionable-work/product entry-point boundary;
- security/data/retention/portability rules;
- failure/reconciliation behavior;
- compatibility/migration from F11 `0.1.0`;
- explicit non-claims.

The contract deliberately does not authorize arbitrary downstream product side effects. Materially independent Tender Agent, Discount Parser or other product actions remain governed by their owning product's exact effective Product Contract and workflow/operation.

Approval/publication integrity:

- approval record commit `0675b50d7d035ee8000edfb2c05a825d655d1894`;
- Provisional publication commit `8ce6935cd7aed7c754bfb14c6029ede20ac42b19`;
- approval commit precedes publication commit;
- closure review `Complete / PASS`.

The owner additionally recorded that the approval request should have presented the decision substance more clearly before requesting exact approval. Future governance gates must provide a human-readable brief before checksum/version confirmation; checksum identity is not a substitute for explainability.

## 9. R33 — Asset / Product Contract / Authority Boundary Review

R33 is `Complete / PASS after 6 iterations` in [`R33-asset-product-contract-authority-boundary-review`](../reviews/R33-asset-product-contract-authority-boundary-review.md).

It reviewed all ten Phase 10 questions and found no unresolved material objection. Mandatory P10.03 constraints are now explicit:

1. Company-specific taxonomy and product-facing `company.*` semantics must not leak into Kernel/CAP-001 business semantics;
2. staged receipt, canonical admission, asset designation and generated-output promotion remain distinct;
3. every canonical mutation remains RFC-0005 Governed Execution;
4. Authentication, Authorization, Organizational Authority, Data Governance, validation and Consequential Approval remain separate;
5. absent approved exact delegation, current first-slice admission records explicit owner Organizational Authority/approval;
6. exact effective Product Contract/workflow/input/control versions are pinned for consequential reliance;
7. external authority remains external where declared;
8. unresolved required purpose/classification/rights/retention/deletion state fails closed;
9. browser/BFF/projection/AI remain non-authoritative and no stable/public API promise is created;
10. a new materially constraining durable implementation mechanism reopens the ADR gate before reliance.

R33 does not change Product Contract `0.2.0`, promote CAP-001, or prove P10.03 implementation.

## 10. P10.03 — domain-neutral organizational-asset admission path

**Status: Current.**

Implement the smallest reusable platform mechanism required by the admitted Product Contract and the R33 gate.

Required behavior:

- accept an exact staged item/version reference;
- resolve current Organization/Actor and applicable access;
- pin exact content/digest/provenance and contract/workflow versions;
- evaluate Authorization, Organizational Authority, Data Governance, validation and applicable Consequential Approval separately;
- under current governance, preserve explicit owner Organizational Authority/approval unless a separately approved exact delegation applies;
- create immutable canonical Document/Artifact version and explicit Governed Organizational Asset designation where approved;
- preserve source/rights/classification/retention metadata proportionately and fail closed when required governance state cannot be resolved;
- preserve `External Reference` authority/freshness/conflict semantics where applicable;
- emit canonical Event/provenance evidence proportionate to the admission consequence;
- be idempotent for the same admitted intent and represent blocked/failed/uncertain/reconciliation-required outcomes truthfully;
- fail closed on stale/revoked/mismatched inputs;
- never mutate an already admitted version or relabel the staged candidate into canonical history;
- keep Company asset taxonomy/product rules outside shared platform semantics;
- keep projections/browser/AI non-authoritative;
- support explicit rejection/cancellation without creating a canonical asset version;
- reopen the ADR gate before any materially new durable persistence/object-store/transaction/evidence-integrity/stable serialization/separate-service choice.

P10.03 does not implement generated-output promotion or downstream product actions and creates no lifecycle/public/Production claim.

## 11. P10.04 — Company Asset Library UX

Owner-facing capabilities:

- `Материалы компании` separates `Черновики / На рассмотрении / Принято / Архив/заменено` as truthful lifecycle views;
- staged versus canonical status is visually unambiguous;
- owner can inspect human-readable metadata first and technical identity/provenance on demand;
- admission review shows exact version/digest/source/role/classification/retention before confirmation;
- owner can reject, admit, and create a new version without overwriting history;
- current effective version is clear;
- prior versions remain inspectable subject to retention/access;
- exact admitted version can be selected for document generation;
- ordinary use requires no terminal/GitHub/internal UUID knowledge.

Workspace remains presentation/application boundary, not authority source.

## 12. P10.05 — reviewed generated-output promotion

Extend the existing exact-version DOCX generation journey with a truthful review lifecycle:

1. generate output from exact admitted input versions;
2. keep result `TransientOutput`;
3. owner reviews/open/downloads it;
4. owner either rejects, keeps transient, or requests admitted promotion;
5. admitted promotion creates a new governed Document/Asset version through Governed Execution;
6. any later external send/sign/publish remains outside scope unless separately contracted.

This task does not turn document generation into validated Knowledge or legal approval.

## 13. R34 / M10-alpha

R34 requires real owner evidence, not synthetic fixtures, for the first asset cycle.

Review at least:

- usability;
- exact-version truthfulness;
- provenance;
- authority/gate correctness;
- retention/classification presentation;
- failure/retry behavior;
- generated-output classification;
- backup/restore/update compatibility;
- no hidden product/platform coupling.

After R34 PASS and the real owner journey passes, `M10-alpha = Achieved / PASS`.

## 14. P10.06 — Real Action Request / Actionable Work boundary

Define a domain-neutral Workspace envelope over real product/company-owned action requests without standardizing product business semantics.

The Workspace projection may expose:

- human-readable request title/context;
- owning product/company source;
- current state/freshness;
- why owner attention is needed;
- allowed next-step descriptions;
- applicable governed execution/preflight state;
- exact source/provenance on demand.

It MUST NOT infer urgency, owner responsibility, approval need or action availability solely from incomplete governance gates or AI suggestions.

No request becomes real merely because the Workspace renders it.

## 15. P10.07 — First real governed operational action

Use the first naturally occurring genuine action admitted by P10.01/P10.02.

Required end-to-end evidence:

`real source request → Workspace context → owner decision → server-side gate revalidation → Governed Execution → canonical/external effect or explicit block/failure/uncertainty → reconstruction evidence`.

Historical replay MUST NOT repeat an external effect without new authorization.

This task is also the natural deferred F08 recheck. If no genuine action exists yet, P10.07 remains waiting rather than synthesizing one.

## 16. P10.08 — Product operational entry-point composition

After the first action works, determine what is genuinely reusable across product actions.

Platform-owned surface may include only domain-neutral mechanics such as:

- action request registration/discovery;
- exact source/contract/version references;
- server-side access/context resolution;
- governed command invocation envelope;
- truthful terminal/blocked/failed/uncertain presentation;
- reconstruction/provenance links.

Tender, Discount, Creative, Proxy or other business semantics remain product-owned.

No universal product-action API is declared Stable in Phase 10.

## 17. R35 — Operational Work / Product Boundary / AI Authority Review

Review:

- no product schema/business approval rule leaked into platform;
- Product Contract is exact and current;
- UI visibility does not equal permission;
- AI recommendation does not equal approval;
- current gate revalidation occurs at command time;
- uncertain external outcomes are not represented as success;
- replay/idempotency/reconciliation semantics are correct;
- external authority is preserved;
- product entry points do not create hidden BFF/private-import coupling.

## 18. P10.09 — source-grounded asset use in Workspace / AI / generation

Admitted assets should become useful, not merely stored.

Permit bounded retrieval/use with:

- exact current/effective asset version;
- clear source/provenance;
- Organization/access/classification/purpose enforcement;
- freshness/applicability where relevant;
- derived previews/search indexes as non-authoritative projections;
- AI summaries/drafts as transient outputs;
- exact version pins when an asset materially affects consequential work.

This task does not automatically extract or promote document contents into RFC-0007 validated Knowledge. A real need for governed Knowledge requires its own explicit promotion scope/Product Contract dependency.

## 19. P10.10 — daily-operations dogfooding

The owner uses Phase 10 features in ordinary work.

Minimum real sessions should cover, when naturally available:

- stage and admit a real Company material;
- retrieve and inspect an admitted asset later;
- create a new immutable version/supersession;
- generate a real Company document from exact admitted inputs;
- review the generated output and exercise the admitted promotion/rejection path;
- complete one genuine action request through Governed Execution;
- inspect truthful result/provenance/reconstruction without terminal/GitHub.

Material friction becomes a bounded Observation/backlog and blocks M10 until dispositioned. Synthetic owner PASS is prohibited.

## 20. P10.11 — lifecycle / reuse disposition

Phase 10 evidence may justify lifecycle discussion, but no automatic transition.

For each relevant mechanism decide explicitly:

- keep product-local;
- keep platform mechanism `Incubating`;
- promote only after applicable governance/readiness prerequisites;
- contain/deprecate/retire unused mechanism;
- split a product-specific mechanism back out of platform.

CAP-001 `Active` promotion is not an M10 requirement. Any `Active` transition must satisfy Accepted RFC prerequisites, including applicable approved decision-authority and operational-readiness governance.

Product Contract `Stable` is not an M10 requirement.

## 21. R36 — M10 Hardening + Milestone Code Health Gate

Before M10 closure review:

- exact-head Productive Workspace CI PASS;
- Reference Python CI PASS;
- security/authority regression PASS;
- supply-chain checks PASS;
- code-health inventory and bounded refactoring of material hotspots;
- no unresolved material architecture/product-boundary finding;
- backup/restore/update/rollback compatibility rechecked for new persistent canonical asset state;
- real owner dogfooding backlog has no unresolved material closure blockers;
- retained known debt explicitly dispositioned rather than hidden.

R36 is engineering evidence, not lifecycle promotion, production approval or conformance certification.

## 22. P10.12 / M10 exit criteria

M10 closes only if all applicable criteria pass:

1. M10-alpha remains valid with at least one real governed Company asset cycle;
2. receipt/staging, canonical admission and generated-output promotion remain distinct and truthful;
3. immutable asset version/provenance/authority/handling semantics are reconstructable;
4. owner can perform ordinary asset work without terminal/GitHub/internal identifiers;
5. one naturally occurring genuine action completes the P10.07 governed path or reaches a truthful blocked/failed/uncertain outcome with complete reconstruction evidence;
6. Actionable Work does not manufacture tasks/urgency/authority;
7. Product Contracts cover actual platform reliance and remain within their declared lifecycle scope;
8. product business semantics remain product-owned;
9. AI remains source-grounded/proposal-only and creates no independent authority or Knowledge promotion;
10. external sources of truth remain authoritative where declared;
11. real daily-operations dogfooding has no unresolved material closure blockers;
12. R33–R36 material findings are closed or explicitly dispositioned by proper authority;
13. M10 Milestone Code Health Gate passes before closure.

If a genuine action does not naturally occur, Phase 10 may complete M10-alpha and remain Active rather than fabricating P10.07 evidence.

## 23. Parallel development lanes during Phase 10

Phase 10 intentionally supports bounded concurrency.

### Lane A — Organizational Assets — primary early critical path

`P10.01 ✓ → P10.02 ✓ → R33 ✓ → P10.03 CURRENT → P10.04 → P10.05 → R34 → M10-alpha`.

### Lane B — Real Operational Work

May design P10.06 in parallel because P10.01 semantics are fixed and the Workspace contract now contains the bounded Actionable Work/product-entry envelope. P10.07 still waits for the owning product's applicable effective Product Contract and a genuine real action request.

### Lane C — Product ↔ Workspace operational composition

Product-local UI/action adapters may proceed in parallel when they remain inside existing Product Contracts or after the required new Product Contract is effective.

### Lane D — External integrations

Existing INT-B7 package remains prepared. Resume only when an exact real 1С/CRM/СЭД/ЭДО endpoint/deployment/account exists. Phase 10 does not fabricate that prerequisite.

### Lane E — Reliability / DX / technical debt

CI, recovery, observability, dependency/security, deterministic build and evidence-backed refactoring work may proceed continuously, provided it does not change Phase 10 authority/Product Contract boundaries silently.

## 24. Concurrency map

```text
                         ┌─ Lane A: Assets
                         │   P10.01 ✓ → P10.02 ✓ → R33 ✓ → P10.03 CURRENT → P10.04 → P10.05 → R34 → M10-alpha
                         │
Phase 10 current main ───┼─ Lane B: Real work
                         │   P10.06 ──[genuine request + owning-product contract]──→ P10.07 → P10.08 → R35
                         │
                         ├─ Lane C: product-owned operational surfaces
                         ├─ Lane D: INT-B7 ──[wait real external endpoint]
                         └─ Lane E: reliability / DX / technical debt

M10-alpha + R35
      ↓
P10.09 → P10.10 → P10.11 → R36 → P10.12 / M10
```

## 25. Explicit non-goals

Phase 10 does not by itself establish:

- customer/public Production;
- universal multi-tenancy or a second Organization;
- public/stable API/SDK/browser compatibility;
- autonomous AI approval;
- a universal Kernel Task primitive;
- automatic document-to-Knowledge promotion;
- electronic signature, legal filing or external document delivery;
- CRM/1С/СЭД business writes without separately governed design;
- Stable Product Contracts;
- Active Platform Capabilities;
- SLA/support/certification/conformance expansion;
- remote execution authority over development/test hosts merely because Workspace displays a project.

## 26. Current canonical action

> **P10.03 — Domain-neutral organizational-asset admission execution path.**

Implement the smallest reusable platform admission mechanism within [`R33`](../reviews/R33-asset-product-contract-authority-boundary-review.md): exact staged input/version; immutable canonical Document/Asset version and explicit asset designation; separate current gate evaluation with explicit owner authority under current governance; exact Product Contract/workflow/input pins; external-authority fidelity; fail-closed rights/data-governance semantics; idempotent/reconstructable outcomes; no Company taxonomy in shared platform semantics; no public/stable/lifecycle overclaim; ADR re-trigger before any new materially constraining durable mechanism.

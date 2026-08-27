# P10.02 — Arvectum Company ↔ Productive Workspace Product Contract

Status: `Draft`
Version: `0.2.0`
Created: `2026-08-27`
Updated: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform`, `product_specific` and `governance`
Roadmap work item: `P10.02 — Product Contract evolution for Company assets + operational work`
Predecessor contract: [`P9.11-F11 Provisional 0.1.0`](P9-11-F11-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.1.0.md)
Authority: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` — `Accepted`; ADR-0001 — `Accepted`
P10.01 authority baseline: [`P10-01-asset-admission-real-work-authority-matrix`](../reviews/P10-01-asset-admission-real-work-authority-matrix.md) — `Complete / PASS`
Lifecycle note: this Draft is **not effective for new governed reliance** until the owner explicitly approves this exact version and a canonical `Provisional 0.2.0` publication exists.

## 1. Purpose and version decision

This Draft evolves the existing Arvectum Company ↔ Productive Workspace Product Contract lineage from `Provisional 0.1.0` to a proposed `0.2.0` boundary.

The change is materially version-worthy because `0.1.0` permits staged Company material intake, exact-version generation and read-only Company portfolio projection but explicitly excludes canonical Company asset admission and arbitrary product action execution.

Version `0.2.0` proposes the minimum sufficient boundary for Phase 10 to:

1. canonically admit reviewed Company materials and external references as governed Document/Artifact/Organizational Asset state through RFC-0005 Governed Execution;
2. separately promote an exact reviewed generated `TransientOutput` into governed Company document/asset state when the later P10.05 implementation is admitted;
3. expose truthful non-authoritative Actionable Work projections and a governed product-operation entry envelope without moving product-specific action semantics or side-effect authority into the Workspace/platform contract.

This Draft deliberately **does not** authorize arbitrary Tender Agent, Discount Parser or other product actions by itself. A concrete product operation remains governed by the owning product's exact effective Product Contract and product-owned workflow/operation semantics before any consequential effect is allowed.

## 2. Product and contract identity

The Product Contract Subject Identity is retained from version `0.1.0`; this is an evolution, not an unrelated new contract.

- Product identity: `product/arvectum-company-workspace@organization/arvectum-company`;
- Product architectural owner: `ООО «Арвектум»`;
- Product Contract subject: `product-contract-subject/p9-11-f11-arvectum-company-workspace@organization/arvectum-company`;
- proposed Product Contract version: `product-contract-version/p9-11-f11-arvectum-company-workspace-v0.2.0@organization/arvectum-company`;
- Product Contract semantic type: `platform.product-contract`;
- Product Contract record authority mode: `Native`;
- Product Contract authority scope: `platform.product-contract/boundary`;
- lifecycle: `Draft`;
- Organization scope: exactly one Organization — `ООО «Арвектум»`.

The stable contract subject lineage preserves the same Company ↔ Workspace responsibility boundary. New material semantics are represented by this new immutable contract version rather than by mutating `0.1.0`.

Possession, discovery, rendering or approval status of this Product Contract does not itself grant Authentication, Authorization, Organizational Authority, Data Governance permission or product-operation authority.

## 3. Scope retained from Provisional 0.1.0

Unless narrowed below, `0.2.0` preserves the admitted `0.1.0` scope:

- Organization-scoped staged Company material/template intake;
- exact staging version, digest and provenance retention;
- exact-version Company document generation;
- generated output as `TransientOutput` by default;
- Company-owned semantic roles and generation behavior remaining outside shared platform semantics;
- explicit Company project registry;
- read-only portfolio projection derived from explicitly registered canonical roadmap/status sources;
- exact source revision/freshness/provenance and visible stale/conflict/unavailable/reconciliation states;
- descriptive execution-target presentation without remote-execution authority;
- Productive Workspace browser/BFF surface remaining internal and release-scoped under ADR-0001.

Nothing in this Draft weakens the existing `0.1.0` exclusions for external sending/signing/filing/publication, roadmap writes, ambient remote execution, cross-Organization reuse, automatic Knowledge promotion or public/stable compatibility commitments.

## 4. New Company asset scope

### 4.1 First-slice admitted material classes

Subject to the exact admission gates in this contract, `0.2.0` may admit the following first-slice Company asset classes identified in P10.01:

1. `Брендбук`;
2. `Логотип` and bounded Company brand assets;
3. `Шаблон документа` and bounded Company document/presentation templates;
4. `Организационный источник` and bounded Company-held source/reference materials;
5. governed external references to Company-relevant source material while preserving external authority;
6. an exact project-bound generated document only after explicit human review and the separate governed promotion operation is available.

Company semantic roles, business meaning, branding rules, document types, usefulness criteria and product-specific approval rules remain Company-owned. These labels do not become Kernel or shared platform semantic types.

### 4.2 First-slice exclusions

The asset admission boundary excludes:

- executable files, scripts and installers;
- macro-enabled Office formats and uncontrolled active content;
- archives with uncontrolled nested content;
- arbitrary local-disk or home-directory indexing;
- content whose type, purpose, source/rights basis or Organization scope cannot be resolved safely;
- automatic external sending, signing, filing or publication;
- electronic signature or legal-validity decisions;
- automatic conversion of any admitted document into Policy, Standard, Decision or validated Knowledge;
- cross-Organization admission, sharing or reuse;
- silent canonicalization caused by persistence, preview, download, repeated use, AI confidence or successful generation.

A later expansion requires a new Product Contract version or separate contract where the responsibility boundary is materially independent.

## 5. Exact platform dependencies

| Dependency | Lifecycle / authority evidence | `0.2.0` reliance | Boundary use |
|---|---|---|---|
| `CAP-001 — Document & Artifact Governance` | `Incubating / Provisional` | required for new Company asset scope | domain-neutral Document/Artifact identity/version, asset designation, provenance, handling and exact-version resolution |
| Productive Workspace application boundary | ADR-0001 `Accepted`; internal release-scoped application | required | owner-facing review/composition, same-origin BFF, server-side scope/gate enforcement, non-authoritative projections |
| RFC-0005 Governed Execution | `Accepted 1.0.0` | required for every consequential canonical admission/promotion and later product command actually executed through platform | exact execution context, Product Contract/version pinning, gate separation, idempotency/retry/uncertainty semantics |
| RFC-0006 Event/Provenance | `Accepted 1.0.0` | required proportionately for consequential execution evidence | append-only canonical Event/provenance where required; telemetry remains non-canonical by default |
| RFC-0008 Document/Artifact semantics | `Accepted 1.0.0` | required | receipt/generation distinct from admission; immutable Document versions; `TransientOutput` default; governed promotion |

### 5.1 CAP-002 — Memory & Knowledge Governance

CAP-002 is **not** added as a required dependency by `0.2.0`.

Admitted documents, extracted text, summaries, generated drafts and recurring use do not become validated Knowledge. Any later governed Knowledge reliance or promotion requires an explicit Product Contract version and RFC-0007-compliant validation/promotion semantics.

### 5.2 CAP-003 and CAP-004

This Draft does not promote or require CAP-003/CAP-004 as new shared product dependencies merely because Workspace offers bounded discovery and reconstructable evidence. Internal rebuildable discovery and RFC-required execution/provenance evidence may remain within the current bounded implementation unless real reliance proves a separate capability dependency.

## 6. New operation contract

### 6.1 `company.asset.admit-staged-version`

Effect class: `canonical mutation`.

Purpose: take one exact `StagedNonCanonical` Company-held material version and, after current gate evaluation, create an immutable governed Document/Artifact version plus an explicit Governed Organizational Asset designation within the declared Company scope.

Required contract semantics:

- exact Organization and attributable Actor resolved server-side;
- deny-by-default Authorization for the exact resource/operation;
- current Organizational Authority evaluated independently;
- current Data Governance purpose/classification/rights/retention/deletion/reuse requirements evaluated independently;
- validation of exact content class, content digest, source/provenance and Company-owned semantic role;
- explicit Consequential Approval where current governance requires it;
- exact staged item/version, content digest, effective Product Contract version and materially relied-upon workflow/control versions pinned before the effect;
- one immutable canonical lineage and explicit asset designation; staged state is not relabeled in place;
- idempotency sufficient to prevent duplicate admission of the same governed intent;
- truthful completed/blocked/failed/uncertain result and required reconstruction evidence;
- fail closed if exact input, current gate state, evidence path or canonical outcome is uncertain.

Under the current governance state, residual Organizational Authority remains with the owner unless a separately approved exact delegation applies.

### 6.2 `company.asset.admit-external-reference`

Effect class: `canonical mutation`.

Purpose: create or version a governed Company asset/reference while preserving an external system/source as authoritative for the underlying declared content/fact scope.

In addition to the same gate separation as staged admission, the operation must declare and preserve:

- external authoritative system/source and object identity where applicable;
- authority scope;
- retrieval/freshness semantics material to reliance;
- conflict and unavailability behavior;
- permitted local transformations;
- rights/purpose/classification/retention/deletion/portability constraints;
- exact governed reference version relied upon.

The operation cannot silently convert an `External Reference` into `Native` authority merely because a local copy, cache, generated representation or newer retrieval exists.

### 6.3 `company.generated-output.promote-reviewed`

Effect class: `canonical mutation`.

Purpose: after explicit owner review, promote one exact generated `TransientOutput` into a governed Company Document/Artifact version and, where declared, a Governed Organizational Asset designation.

This contract version may govern the boundary, but the operation **must remain unavailable for real reliance until P10.05 implements and reviews the promotion path**.

Required semantics:

- exact transient artifact identity/digest and generation provenance;
- exact materially relied-upon admitted input versions and generation configuration/instruction version where retained;
- explicit human review disposition;
- current Authorization, Organizational Authority, Data Governance and Consequential Approval re-evaluated at promotion time;
- immutable new canonical Document/Artifact version; the transient candidate is not silently rewritten into canonical history;
- rejection / keep-transient / blocked / failed / uncertain outcomes remain truthful;
- no validated Knowledge status is created.

Opening, downloading, previewing or editing a generated output does not satisfy this operation.

### 6.4 `workspace.actionable-work.project-request`

Effect class: `read-only / non-canonical projection`.

Purpose: project an explicit current product/company-owned request into an owner-facing Actionable Work view.

The projection:

- must identify the owning product/company source and exact source/version/freshness where material;
- may summarize, explain and propose next steps;
- must not manufacture a request, urgency, assignment, approval, permission or Organizational Authority;
- must not infer a current request solely from chat/model memory, a roadmap heading, stale cache or technical capability;
- must visibly represent stale/unavailable/conflict/reconciliation-required source state;
- is never sufficient evidence that a consequential operation remains authorized.

No universal Kernel `Task` primitive is created by this operation.

### 6.5 `workspace.product-operation.enter`

Effect class: `routing / no product side effect by itself`.

Purpose: allow Productive Workspace to enter a product-owned governed operation from an explicit Actionable Work source without embedding product business logic into shared Workspace/platform semantics.

This operation may:

1. resolve the exact product/request/source identity and current version;
2. resolve the exact effective Product Contract governing the intended product operation;
3. assemble owner-facing context and product-specific entry UI through the declared product composition boundary;
4. initiate or continue the **downstream product-owned governed command path only when that downstream contract explicitly admits it**.

This operation must not itself:

- authorize an arbitrary Tender Agent, Discount Parser or other product side effect;
- invent a product workflow or approval rule;
- convert descriptive execution-target metadata into remote-execution authority;
- bypass the downstream product's current Authorization, Organizational Authority, Data Governance, validation, Consequential Approval or exact-version checks;
- create a public/stable generic task/action API.

The actual consequential product operation remains governed by the owning product's exact effective Product Contract and workflow/operation definition. If no such effective contract exists, Workspace must stop with a truthful blocked/unavailable state.

## 7. Staging, canonical admission and asset designation

The following states remain semantically distinct:

```text
received/stored candidate
        ↓
StagedNonCanonical
        ↓ optional review/request
Governed Execution admission
        ↓ success only
Canonical Document/Artifact Version
        ↓ explicit governed designation where applicable
Governed Organizational Asset
```

Rules:

1. receipt and staging create no canonical asset state;
2. persistence alone creates no asset designation;
3. canonical admission never mutates the staged candidate into historical canonical truth by relabeling;
4. each admitted version is immutable;
5. a new content/version creates a new immutable canonical version under the same subject only when the logical subject remains the same;
6. supersession/retirement does not erase historical versions or prior asset designation, subject to lawful retention/deletion;
7. exact Version Identity is pinned before consequential use of a mutable governed subject.

## 8. Generated-output lifecycle

The contract preserves this lifecycle:

```text
TransientOutput
      ↓ explicit owner review
reject / keep transient / request governed promotion
                             ↓
                 current gate revalidation
                             ↓
                     Governed Execution
                             ↓ success only
             governed Company Document/Asset Version
```

Generated output remains transient if the owner merely opens, downloads, comments on or uses it as a draft. Promotion is a separate consequential operation with its own exact inputs and evidence.

External sending/signing/publication remains outside `0.2.0`.

## 9. Platform-owned vs Company/product-owned semantics

### 9.1 Platform-owned, domain-neutral mechanics

Arvectum OS may own only reusable mechanics such as:

- stable Subject/Version Identity and immutable canonical lineage;
- generic Document/Artifact and asset-designation semantics;
- Organization/Actor attribution;
- safe staging/admission envelope;
- domain-neutral Authorization/Data Governance enforcement points;
- Governed Execution envelope, exact-version pinning and truthful outcome semantics;
- generic provenance/Event/reconstruction mechanics;
- rebuildable non-authoritative projection infrastructure;
- generic portability/export mechanics;
- internal Workspace security/navigation/application composition under ADR-0001.

### 9.2 Company/product-owned semantics

Arvectum Company and each product retain responsibility for:

- asset-role taxonomy and business meaning;
- brand/style/template/document semantics;
- product-specific rights/usage business rules beyond shared structural controls;
- product approval criteria and domain workflows;
- Action Request meaning, state, priority, urgency and assignment;
- product-specific operation names, side effects and validation;
- product-specific UX and owner disposition vocabulary;
- source descriptors/adapters whose interpretation is product-specific.

Shared platform code must not absorb these semantics simply because Productive Workspace renders them.

## 10. Authority and source-of-truth rules

### 10.1 Company-held admitted assets

A successfully admitted Company-held exact Document/Artifact version is `Native` for the Company-held governed version and its Arvectum OS governance envelope.

That declaration does not override third-party rights, external factual authority or legal ownership. Source/right provenance remains required where applicable.

### 10.2 External references

An external source remains authoritative within the declared `External Reference` scope. Arvectum OS governs its identity/reference/provenance and permitted reliance, not the underlying fact merely by referencing it.

### 10.3 Product requests and roadmaps

Product/company request state and product roadmaps remain authoritative only in their declared product/company sources. Workspace projections and caches are derived/non-canonical and cannot silently replace those sources.

### 10.4 Generated output

A generated candidate has no canonical authority by default. A successful later promotion establishes authority only for the exact admitted Company-held governed version and declared scope.

## 11. Browser/BFF and command-side enforcement

ADR-0001 remains binding.

For every state-changing browser request covered by this Product Contract:

- the browser has no ambient authority;
- the BFF/session is not a canonical source and does not mint Organizational Authority;
- CSRF/origin/session success is insufficient for consequential approval;
- the server-side command path resolves current Actor and exactly one Organization scope;
- applicable Authorization, Organizational Authority, Data Governance, validation and approval are re-evaluated before consequential effect;
- exact mutable governed inputs and Product Contract/workflow versions materially relied upon are pinned;
- stale browser/read-model state cannot authorize the command;
- a detected release mismatch or materially uncertain current state fails safely for consequential behavior.

The browser/BFF exchange remains internal and release-scoped. This Product Contract creates no public/stable `/bff/*` or browser compatibility promise.

## 12. Security, rights, classification, purpose and retention

Within `0.2.0`:

1. all real data is scoped to `ООО «Арвектум»`;
2. cross-Organization reads/writes/reuse are denied by default;
3. access is deny-by-default and least privilege applies;
4. unresolved Organization scope fails closed;
5. uploaded/linked/generated content is processed only for declared permitted purpose;
6. classification/handling state must be resolvable where it affects access, logging, retention, generation, export or external processing;
7. rights/source affirmation is required proportionate to the asset class and intended use;
8. raw Company content, secrets and reusable credentials are not duplicated into logs/telemetry merely for audit convenience;
9. derived previews/extractions/summaries inherit applicable Organization/classification/purpose/retention constraints unless a governed rule validly changes them;
10. each admitted governed asset resolves to an applicable retention/deletion rule where required;
11. physical deletion requirements and historical lineage/evidence retention remain distinguishable; the system does not claim reconstructability beyond retained evidence;
12. no upload content is executed;
13. arbitrary storage paths, external URLs or repository paths supplied by the browser are not treated as trusted authority.

Concrete retention durations remain subordinate approved policy/product decisions and are not invented by this contract.

## 13. Portability and exit

The product boundary must preserve a usable exit path.

For admitted Company assets, an authorized export must preserve or explicitly account for, where applicable:

- stable subject/version identities;
- retained lawful original bytes or governed external references;
- canonical lineage and asset-designation history;
- authority mode and external source identity;
- Company-owned semantic role metadata;
- classification/handling constraints;
- rights/source declarations or references;
- retention/deletion state;
- provenance and materially relevant relationships;
- integrity/manifest metadata.

Non-canonical staging, search, Actionable Work and portfolio caches may be purged/rebuilt and are not portability authorities.

If this contract is Deprecated/Retired, Company composition may be disabled without corrupting canonical platform history. No product may depend on hidden Workspace tables/imports/private streams for continued access to governed meaning.

## 14. Event, provenance and reconstruction boundary

Canonical Events are required only where the admitted consequential operation/event contract requires them; ordinary UI clicks, reads, search queries and projection refreshes remain telemetry/non-canonical by default.

For each successful consequential admission/promotion the reconstruction boundary must preserve or reference, proportionate to scope:

- attributable Actor and Organization;
- exact effective Product Contract Version Identity;
- exact workflow/operation definition version;
- exact staged/transient/reference input version and content digest where material;
- materially relied-upon governed control versions;
- Authorization/Organizational Authority/Data Governance/validation/approval evidence sufficient to explain the decision without retaining unnecessary secrets/content;
- resulting canonical Subject/Version Identity and asset designation where applicable;
- canonical Event/provenance references required by the operation;
- truthful terminal outcome.

Historical replay or reconstruction never repeats a consequential effect without a new applicable authorization/Governed Execution.

## 15. Failure, retry and reconciliation

### 15.1 Asset admission/promotion

On unsupported/unsafe content, stale input, authority/gate failure, rights/data-governance failure, storage/canonicalization failure, evidence-path failure or uncertain outcome:

- fail closed;
- do not claim canonical admission/promotion unless the canonical effect is established;
- do not silently create a second canonical head;
- expose `blocked`, `failed` or `uncertain/reconciliation-required` truthfully;
- preserve only permitted evidence needed for retry/reconstruction;
- retry must not duplicate a consequential effect whose prior outcome may already have succeeded.

### 15.2 External reference

On external source unavailability/freshness/conflict uncertainty, do not silently convert cached/local state into current authority. Surface the limitation and require the declared reconciliation path before consequential reliance where material.

### 15.3 Product operational entry

If the owning product request is stale/unavailable, the intended product operation lacks an effective Product Contract, a current gate cannot be evaluated, or the downstream outcome is uncertain, Workspace must stop or expose the exact blocked/failed/uncertain/reconciliation state. It must not infer success from UI navigation or technical dispatch.

## 16. Compatibility and migration from Provisional 0.1.0

### 16.1 Contract lineage

`0.2.0` retains the same Product Contract Subject Identity and creates a new immutable Product Contract Version Identity. `0.1.0` remains immutable historical contract evidence.

### 16.2 Existing staged Company materials

Existing `0.1.0` F11 staged materials remain `StagedNonCanonical` after `0.2.0` becomes effective. No pre-existing staged item is retroactively admitted merely because the contract gains an admission operation.

An existing staged exact version may later become an admission input only after current `0.2.0` gates review that exact version.

### 16.3 Existing generated outputs

Existing F11 generated files remain `TransientOutput`. No historical output is retroactively promoted. A retained exact candidate may enter a later promotion request only if P10.05 admits the operation and the current gates are evaluated then.

### 16.4 Existing portfolio projection

F11B remains read-only and non-authoritative. No project roadmap/status source moves into Workspace authority. Existing cache/projection data may be rebuilt without canonical migration.

### 16.5 Existing product actions

This contract does not grandfather any historical or existing product execution path into Workspace authority. Each actual product action requires its own exact currently effective product boundary and gate evaluation.

### 16.6 No bulk canonical migration

No staged file, cache, generated artifact, chat history, model memory, roadmap card, telemetry record or legacy product row is bulk-promoted into canonical platform state by this version transition.

## 17. Explicit non-claims

This Draft, and any later `Provisional 0.2.0` publication with the same reviewed substance, does not establish:

- `Stable` Product Contract lifecycle;
- an `Active` Platform Capability;
- customer/external Production readiness;
- public/stable API, SDK, browser or BFF compatibility;
- remote host execution authority;
- a universal platform `Task` primitive;
- automatic external sending, signing, filing or publication;
- electronic-signature/legal-validity semantics;
- automatic Knowledge promotion or platform learning from Company assets;
- cross-Organization sharing/reuse;
- SLA/support/certification/conformance expansion;
- legal ownership or expanded reuse rights merely through asset designation;
- approval of any particular Tender Agent, Discount Parser or other product consequential action.

## 18. Lifecycle gate and effective-state rule

### 18.1 Current Draft state

This file is `Draft 0.2.0`. It is reviewable design evidence only.

No implementation may rely on the new canonical admission/promotion or operational-entry scope as an effective Product Contract until all are true:

1. functional cross-review has no unresolved material objection;
2. the exact reviewed Draft blob/version is identified;
3. the owner explicitly approves that exact bounded contract version;
4. an independent canonical approval record exists;
5. a lifecycle-current `Provisional 0.2.0` publication is created without materially changing the approved substance;
6. roadmap and contract pointers are synchronized and read-after-write verified.

### 18.2 Provisional meaning

If explicitly approved and published as `Provisional 0.2.0`, the contract permits bounded implementation and real validation only within the exact declared scope. It does not prove implementation PASS, owner-usefulness PASS, operational readiness, Stable lifecycle, Active capability status or external compatibility/support commitments.

### 18.3 R33

R33 remains the blocking Asset / Product Contract / Authority Boundary Review before P10.03 implementation. Product Contract publication does not bypass R33.

## 19. Functional cross-review — Draft 0.2.0

Maximum allowed iterations: 7.

### Iteration 1 — lineage and minimum-sufficient boundary

Finding: canonical asset work extends the same Company material/Workspace reliance already governed by F11; a new unrelated Product Contract would fragment one responsibility lineage.

Resolution: preserve the existing Product Contract Subject Identity and create version `0.2.0` as an immutable material evolution. Keep product-specific consequential operations out of this boundary.

Result: `PASS after revision`.

### Iteration 2 — asset / authority / generated-output boundary

Finding: risk of conflating staging, canonical admission, asset designation, owner review and generated-output promotion.

Resolution: define separate staged, canonical and transient states; define separate `admit-*` and `promote-reviewed` governed operations; keep Authentication, Authorization, Organizational Authority, Data Governance, validation and Consequential Approval distinct.

Result: `PASS after revision`.

### Iteration 3 — operational work / product ownership boundary

Finding: a generic Workspace action contract could accidentally authorize arbitrary product side effects or absorb product business workflow semantics.

Resolution: `workspace.actionable-work.project-request` is read-only/non-authoritative and `workspace.product-operation.enter` has no product side effect by itself. Actual product effects require the owning product's exact effective Product Contract and workflow/operation.

Result: `PASS after revision`.

### Iteration 4 — security, migration and public-surface boundary

Finding: risk of retroactive admission of existing staged/generated material, cache/roadmap authority drift, browser authority or accidental stable BFF/API commitment.

Resolution: no retroactive admission/promotion; portfolio and Actionable Work remain derived; command-side gate revalidation remains server-side; browser/BFF surface remains internal/release-scoped; no Stable/public claim.

Result: `PASS`.

Material objections after iteration 4: **none at Draft design level**.

This functional review does not constitute owner approval, Product Contract lifecycle promotion, R33 PASS, Platform Capability promotion, operational-readiness approval or delegated Organizational Authority.

## 20. Draft disposition

- Product Contract lineage decision: **evolve existing Arvectum Company ↔ Productive Workspace subject**;
- proposed new version: `0.2.0`;
- lifecycle: `Draft`;
- P10.01 prerequisite: `Complete / PASS` on the working branch;
- functional design review: `PASS after 4 iterations`, no material unresolved objection;
- owner approval of the exact Draft: **pending**;
- `Provisional 0.2.0` publication: **not yet allowed**;
- new governed reliance: **not yet allowed**;
- R33: remains blocked until effective Product Contract publication.

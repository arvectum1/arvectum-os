# P10.04 — Company Asset Library UX + version/handling lifecycle — Closure Review

Status: `Complete / PASS`
Date: `2026-08-29`
Owner: `ООО «Арвектум»`
Task classification: `product_contract`

## 1. Authority baseline

Checked before and during implementation:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted`;
- [`P10-01-asset-admission-real-work-authority-matrix`](P10-01-asset-admission-real-work-authority-matrix.md) — `Complete / PASS`;
- [`P10-02-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.2.0`](../contracts/P10-02-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.2.0.md) — lifecycle-current `Provisional 0.2.0`;
- [`R33-asset-product-contract-authority-boundary-review`](R33-asset-product-contract-authority-boundary-review.md) — `Complete / PASS after 6 iterations`;
- [`P10-03-organizational-asset-admission-closure-review`](P10-03-organizational-asset-admission-closure-review.md) — `Complete / PASS`;
- [`ROADMAP.md`](../roadmap/ROADMAP.md) and [`PHASE-10-OPERATIONAL-WORK-ORGANIZATIONAL-ASSETS.md`](../roadmap/PHASE-10-OPERATIONAL-WORK-ORGANIZATIONAL-ASSETS.md).

No conflict with a higher-authority source was found. P10.04 remains subordinate to the Accepted semantic owners and does not amend Constitution, RFC or Accepted ADR meaning.

## 2. Reviewed implementation scope

P10.04 exposes the already-admitted P10.03 Organizational Asset semantics through the owner-facing Productive Workspace while keeping staging/review/product UX product-owned and non-authoritative.

The reviewed path provides:

1. four truthful owner-facing lifecycle views: `Черновики / На рассмотрении / Принято / Архив / заменено`;
2. explicit visual and payload separation of `StagedNonCanonical` review state from canonical admission;
3. human-readable role/classification/purpose/rights/retention/deletion/reuse information before technical identifiers;
4. exact staged version, digest and handling review before admission;
5. explicit owner rejection with no canonical mutation;
6. productive owner-operated admission through the existing P10.03 guarded Governed Execution entrypoint;
7. independent current Actor Assurance, Authorization, Organizational Authority, Data Governance, Validation and Consequential Approval evidence;
8. a distinct least-privilege P7.04 authorization grant for `company.asset.admit-staged-version` rather than reuse of `workspace.open`;
9. explicit one-time grant provisioning that grants authorization only and does not provide Organizational Authority or Consequential Approval;
10. immutable admitted version/currentness projection and linear successor enforcement;
11. preservation of historical superseded admitted versions rather than overwrite;
12. visible canonical Document/designation/Event provenance on owner-requested technical drill-down;
13. ordinary owner creation of a new staged immutable version without UUID/GitHub/terminal knowledge;
14. Organization-scoped bounded export;
15. generated DOCX use only from an exact admitted Company Asset version, while the result remains `TransientOutput`;
16. exact review-evidence and handling-policy continuity into the governed admission command;
17. idempotent repeated owner admission of the same exact reviewed intent;
18. productive `build_workspace_app()` composition of the governed executor with fail-closed behavior when the exact admission grant is absent.

## 3. Boundary findings

### 3.1 Staging and review remain non-canonical

A staged upload remains `StagedNonCanonical` before and after admission. Review state is stored in product-local staging metadata and is explicitly marked `canonical_authority: false`.

Submitting for review or rejecting a staged version does not mutate canonical state. Only the successful P10.03 guarded admission path creates the immutable canonical Document Version, separate Organizational Asset designation and canonical admission Event.

### 3.2 Workspace access is not admission authorization

The pre-existing P7.04 `workspace.open` grant is not reused as permission to admit an asset.

P10.04 introduces an exact product-side operational authorization check for:

- operation `company.asset.admit-staged-version`;
- resource `company-assets`;
- access path `local`;
- the current attributable enabled human owner principal;
- the current active P7.04 credential and exact Organization.

The grant must be explicitly provisioned. Productive Workspace does not auto-grant it during startup, session bootstrap, review or button rendering.

The grant supplies Authorization evidence only. P7.04 continues to state that operational access supplies neither Organizational Authority nor Consequential Approval.

### 3.3 Organizational Authority and owner approval remain independent

Under the current P10.01 matrix and the still-`Proposed` Decision Authority Policy, residual Organizational Authority remains with the owner unless an applicable approved delegation exists.

P10.04 therefore preserves a distinct current owner Organizational Authority basis and a distinct exact owner-command Consequential Approval basis. Neither basis is inferred from login, button visibility, Product Contract possession, review state or authorization grant.

The bounded product-local Workflow used by the command adds no new business policy: it projects the already-approved P10.02 `company.asset.admit-staged-version` operation, exact candidate and P10.01 authority matrix into the RFC-0005 execution context. It does not create a broader reusable/public workflow contract or new delegated authority.

### 3.4 Exact review and handling continuity is fail closed

The executor re-reads the current product-local review evidence immediately before governed admission and requires:

- exact `InReview` state;
- explicit non-canonical review authority marker;
- same current owner actor;
- unchanged deletion/reuse policy;
- exact staged material/version;
- exact current content digest.

The Data Governance and Validation gate bases include the reviewed handling policy and exact review/version/digest evidence. A direct executor call without current review evidence fails before canonical mutation.

### 3.5 Retry intent is explicit and idempotent

Functional review found that a stable retry token combined with freshly generated candidate timestamps could create an idempotency-key conflict for an otherwise identical owner retry.

P10.04 now binds the in-process owner admission intent to the exact Organization/material/version/review-policy digest and preserves one command timestamp for that intent. The retry token and Event identities also include the exact review-policy digest. Once the exact version is admitted, a repeated request resolves the existing immutable result without producing a second canonical admission/Event/effect.

Changed handling/review intent is not silently treated as the same admission request.

### 3.6 Version/currentness and supersession remain immutable

The admitted Document Subject lineage is inspected with the existing canonical-lineage semantic owner. Exactly one head is current. A later admitted staged version must name the exact current canonical predecessor; branching, skipping an unadmitted predecessor or ambiguous current state fails closed.

Historical admitted versions remain visible in `Архив / заменено`; the current version appears in `Принято`.

### 3.7 Provenance projection uses the canonical Event envelope

CI exposed one projection defect where P10.04 attempted to read provenance directly from `CanonicalEvent`. The canonical Event owns provenance through its canonical record envelope. The projection was corrected to read `event.record.provenance_refs` without changing Event/admission semantics.

### 3.8 Product/platform ownership remains intact

Company taxonomy, review labels, `company.asset.*` operation naming, material roles, form fields and owner-facing UX remain inside Workspace/product modules.

The shared P10.03 guarded admission path remains domain-neutral. P10.04 does not add Company taxonomy to the Kernel, CAP-001 or shared admission semantic owner.

### 3.9 No new durable mechanism is selected

P10.03 closed its exact internal reference/runtime scope with bounded in-memory canonical-admission state and explicitly deferred any database, object store, durable transaction manager, durable idempotency/reconciliation ledger, stable serialization/wire contract or separate service topology to the applicable ADR gate.

P10.04 reuses that foundation and does not select one of those mechanisms by product-local shortcut. Therefore this closure proves the owner-facing/reference-runtime lifecycle composition, not restart-durable canonical persistence or M10-alpha live-session evidence.

A later task that selects a materially constraining durable mechanism must evaluate the applicable ADR gate before reliance.

### 3.10 Generated output and Knowledge boundaries remain unchanged

Generation now requires an exact admitted Company Asset DOCX version. The generated file remains `TransientOutput`; download does not promote it. P10.04 creates no RFC-0007 validated Knowledge and does not implement the P10.05 generated-output promotion operation.

## 4. Functional cross-review iterations

Maximum permitted iterations: 7.

### Iteration 1 — lifecycle/authority presentation

**Finding:** owner UX had to expose useful lifecycle actions without collapsing staged review into canonical admission or making technical identifiers primary.

**Revision:** established four truthful views, explicit staged/canonical badges, human-first handling metadata, exact admission review proof and technical provenance drill-down.

**Disposition:** closed.

### Iteration 2 — guarded-entrypoint architecture fitness

**Finding:** the first P10.04 backend composition called the low-level Organizational Asset admission primitive directly, bypassing the P10.03 guarded integration entrypoint.

**Revision:** routed canonical admission exclusively through `admit_governed_organizational_asset`; the existing architecture-fitness guard remains enforced and Reference Python CI passes.

**Disposition:** closed.

### Iteration 3 — frontend contract and reproducible production assets

**Finding:** legacy owner-journey fixtures still modeled the pre-P10.04 Company Materials projection, and the first rebuilt SPA bundle did not match committed production assets.

**Revision:** updated tests to the Company Asset Library contract, retained admitted-only generation semantics, rebuilt exact production assets on the official locked CI runner and restored the ordinary reproducibility gate without leaving temporary CI reconciliation machinery.

**Disposition:** closed.

### Iteration 4 — productive admission wiring

**Finding:** P10.04 routes were implemented but productive `p9_03_workspace.py` still installed them without a current governed admission executor, so the owner path was correctly fail-closed but could never complete admission.

**Revision:** installed `P1004OwnerCompanyAssetAdmissionProvider` + `P1003CompanyAssetAdmissionExecutor` in productive composition. Added a separate exact admission authorization grant and explicit provisioning command; `workspace.open` is not reused. Added executable evidence that productive composition installs the executor but does not auto-grant admission.

**Disposition:** closed.

### Iteration 5 — exact review continuity and idempotency

**Finding:** a caller could reach the executor abstraction without the library's review transition, and retry identity did not yet preserve one stable exact owner intent across freshly generated runtime timestamps.

**Revision:** executor now independently revalidates exact current review evidence and policy, carries review/digest evidence into gate bases, stabilizes one exact in-process command intent and returns an existing admitted result on exact repeated success.

**Disposition:** closed.

### Iteration 6 — canonical Event provenance and accumulated review

**Finding:** productive integration tests exposed an incorrect projection access to Event provenance (`event.provenance_refs` rather than `event.record.provenance_refs`).

**Revision:** corrected projection access. Re-reviewed accumulated backend, productive composition, UI, security/authority separation, Product Contract boundary, provenance, version/currentness, generation, export, tests and non-claims.

**Disposition:** closed. No remaining material functional, authority, security, product/platform, source-of-truth, provenance, versioning, retry or ADR-boundary objection was identified inside the exact P10.04 scope.

This functional review is engineering evidence only. It is not a Constitution/RFC/ADR acceptance, Product Contract lifecycle promotion, Platform Capability promotion, operational-readiness approval or broader conformance decision.

## 5. Executable evidence

P10.04 acceptance coverage includes:

- truthful four-view staged/review/accepted/archive projection;
- staged review remains non-canonical;
- rejection without canonical mutation;
- exact review handling-policy validation;
- explicit separate local admission grant and revocation behavior;
- no ambient/automatic admission grant;
- productive Workspace installs the governed executor;
- all six independent RFC-0005 gate kinds present and `ALLOW` before admission;
- P10.01 owner Organizational Authority basis distinct from authorization;
- exact owner-command Consequential Approval basis distinct from authorization/authority;
- P10.02 Product Contract remains `Provisional`;
- direct executor call without current review evidence fails closed;
- canonical admission only through the P10.03 guard;
- idempotent exact repeated owner admission;
- immutable admitted version history/currentness/linear successor behavior;
- canonical Document/designation/Event provenance projection;
- Organization-scoped bounded export;
- exact admitted-version-only Company DOCX generation;
- generated result remains `TransientOutput`;
- no validated Knowledge promotion;
- production frontend lock/assets reproducibility.

A green implementation baseline was recorded at commit `b48dbb2e0c2c42188bcb1b42095bba3610ba4228` after the productive wiring and Event-provenance correction:

- `Productive Workspace CI` run `33241889059` — `success`;
- `Reference Python CI` run `33241889134` — `success`.

A final evidence-only test then added an explicit assertion that productive `build_workspace_app()` installs the governed executor without auto-granting admission. Merge is permitted only if the final PR-head CI remains green after closure/roadmap synchronization.

## 6. Closure decision

**P10.04 = Complete / PASS** for the exact bounded internal owner-facing/reference-runtime scope described above.

Canonical sequencing advances to:

> **P10.05 — Reviewed generated-output promotion boundary.**

## 7. Explicit non-claims

P10.04 closure does **not** establish:

- `M10-alpha` or a completed live real Company Asset Cycle;
- restart-durable canonical asset persistence or a selected database/object-store/transaction/idempotency architecture;
- P10.05 generated-output promotion implementation;
- automatic document → RFC-0007 Knowledge promotion;
- a Stable Product Contract;
- an Active Platform Capability;
- customer/public Production;
- a public/stable API/SDK/wire/browser contract;
- multi-Organization proof;
- SLA/support/certification expansion;
- broader conformance maturity;
- autonomous AI authority or approval;
- a new approved delegation of Organizational Authority.

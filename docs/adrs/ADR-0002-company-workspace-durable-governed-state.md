# ADR-0002 — Company Workspace Durable Governed State

Status: `Proposed`
Version: `0.1.0`
Date: `2026-08-29`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `product_specific`, `platform-boundary` and `governance`
Related: Constitution `1.2.0`; RFC-0001, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0008 `1.0.0` — `Accepted`; ADR-0001 — `Accepted`; P10.02 Company Workspace Product Contract `0.2.0` — `Provisional`; R34 — `Executed / BLOCKED`
Decision authority: residual owner authority; exact proposal approval pending

## 1. Context

R34 requires the first real owner-operated Arvectum Company asset cycle to prove not only session-local usability but also exact-version/provenance truthfulness, failure/retry behavior and backup/restore/update compatibility.

P10.03, P10.04 and P10.05 intentionally closed without selecting durable canonical persistence. Their reference semantic owners keep admission/promotion state in memory and explicitly leave any database, durable idempotency ledger, transaction manager or serialization mechanism behind the applicable ADR gate.

The current Company staging path already uses an owner-local runtime root with secured directories, content-addressed blobs, immutable staged-version identities and atomic JSON manifests. Staged/review/transient material is product-owned and non-canonical. Canonical Company asset admission and reviewed-output promotion, however, currently lose their committed semantic state when the process restarts.

That gap is acceptable inside the explicit P10.03–P10.05 non-claims, but it blocks R34/M10-alpha because a real governed Company asset must remain reconstructable and safely usable after restart/recovery.

The decision must not:

- select a mandatory platform-wide database or event store;
- make a product-local physical layout a shared Platform Contract;
- move Company taxonomy or business rules into shared platform behavior;
- turn staging/review/transient output into canonical state through persistence alone;
- weaken RFC-0005 Governed Execution or RFC-0006 append-only Event semantics;
- replay historical consequential effects during recovery;
- create an `Active` Platform Capability or a public/stable storage API.

## 2. Decision

If accepted, the bounded Company Workspace runtime SHALL persist the exact committed canonical/evidence state required by the P10.02 `Provisional 0.2.0` asset operations as **owner-local immutable JSON records under the existing Workspace runtime root**.

This is a product-local persistence adapter behind the existing semantic owners. It is not a new Kernel primitive, database requirement, public wire contract or platform capability.

### 2.1 Physical form

Use a dedicated runtime subtree, for example:

```text
<runtime-root>/workspace-company-governed-state/
  admission/
    committed/
    attempts/
  promotion/
    committed/
    attempts/
  manifests/
```

Each consequential committed result or uncertainty/idempotency record is stored as one immutable, schema-versioned JSON record.

The implementation SHALL:

- create records with temporary-file + fsync/close + atomic rename semantics appropriate to the local filesystem;
- use owner-only directory/file permissions consistent with the existing Company materials store;
- refuse symlinks and unsafe paths;
- never overwrite a committed record with materially different content;
- use deterministic identity/retry/event information to detect duplicate/conflicting records;
- keep raw Company document bytes in the existing content-addressed material/output stores rather than duplicating them into governance metadata;
- keep reusable credentials/secrets out of persisted canonical/evidence payloads.

### 2.2 Semantic source of truth

The persisted records represent the durable product-runtime realization of already-governed P10.03/P10.05 semantic results. They do not redefine those semantics.

On startup/recovery the adapter SHALL reconstruct typed `OrganizationalAssetAdmissionState` and `ReviewedGeneratedOutputPromotionState` (or an equivalent exact semantic representation) from immutable records and verify:

- schema/version support;
- Organization scope;
- stable Subject/Version/Event identities;
- exact digests/integrity references;
- predecessor/lineage consistency;
- retry-token/fingerprint consistency;
- no conflicting reuse of one canonical identity;
- required source bytes/references are available when continued use requires them.

A projection/index MAY be cached for performance, but any cache is rebuildable and non-authoritative.

### 2.3 Commit boundary

A state-changing owner command SHALL be reported as successful only after:

1. current RFC-0005 gates and exact-version checks pass;
2. the pure/domain semantic owner produces one logically committed result;
3. the corresponding immutable durable record is established successfully;
4. the runtime read-after-write reconstructs the same exact result from durable state.

If step 3 or 4 fails, the command MUST NOT report successful durable admission/promotion. It must expose a truthful failed/uncertain/reconciliation-required outcome according to what can be proved.

If the durable record exists but the client did not receive the response, retry SHALL resolve the same committed result idempotently rather than repeat the consequential effect.

### 2.4 Recovery and replay

Recovery reconstructs state; it does not re-execute historical side effects.

Historical Events/records MAY be replayed only as pure reconstruction input. No external effect, canonical re-admission or new promotion may be repeated without a new current Governed Execution where required by RFC-0005/RFC-0006.

Uncertain prior attempts SHALL remain fail-closed until reconciled; restart MUST NOT convert uncertainty into success or permission to retry blindly.

### 2.5 Backup / restore / update

The governed-state subtree and the existing Company material/output stores form one declared owner-local recovery set for the bounded Company Workspace asset cycle.

Backup/restore evidence for R34 SHALL prove at least:

- exact staged source bytes/manifests survive or are restored consistently;
- admitted canonical identities, versions, provenance and Event references reconstruct exactly;
- reviewed promotion reconstructs exactly while the original transient source remains transient;
- pre-promotion admitted versions remain immutable/retrievable;
- an update/restart does not silently drop or reinterpret stored schema versions;
- unsupported future/unknown schema versions fail closed rather than being guessed.

This ADR establishes no RTO/RPO, archival guarantee, external-production support promise or customer SLA.

### 2.6 Portability

The JSON representation is an internal, schema-versioned persistence format, not a public/stable API. Nevertheless it SHALL remain inspectable and exportable enough to support the P10.02 portability boundary without dependence on Python pickle, opaque process memory or a proprietary database encoding.

A future storage implementation MAY replace the filesystem representation if it preserves the governed identities, versions, provenance, event history, retry/reconciliation semantics and migration/export behavior. Such replacement requires the applicable subordinate decision if materially constraining.

## 3. Product / platform boundary

Platform-owned semantics remain those already defined by Accepted RFCs and existing capability contracts: identity/versioning, Governed Execution, Event/provenance, Document/Artifact and Organizational Asset semantics.

Company-owned implementation remains responsible for:

- this owner-local persistence adapter;
- Company material/runtime directory composition;
- Company-specific projection and UX;
- Company semantic roles and review vocabulary.

No shared platform consumer may depend on these filesystem paths, JSON filenames or Company-specific schemas as an undocumented platform contract.

Successful R34 use does not promote this mechanism into a Platform Capability. Reuse by another product requires a separate evidence-based promotion/contract decision.

## 4. Security and data handling

The adapter SHALL preserve RFC-0003 and P10.02 requirements:

- exact one-Organization scope for this bounded slice;
- deny/fail closed on unresolved or conflicting scope;
- least-privilege filesystem access;
- classification/purpose/rights/retention/deletion metadata where required for reconstruction;
- no raw governed content, reusable credentials or secrets duplicated into logs;
- no ambient cross-Organization reuse;
- explicit deletion/retention handling without rewriting retained historical meaning.

Persistence is not authority. A recovered record does not grant current Authorization, Organizational Authority, Data Governance permission or Consequential Approval for a new operation.

## 5. Alternatives considered

### A. Keep in-memory state through R34

Rejected. It cannot prove restart-durable reconstructability or backup/restore/update compatibility required by R34 and Phase 10.

### B. Introduce SQLite as the Company/platform canonical store now

Rejected for this stage. RFC-0001/RFC-0005/RFC-0006/RFC-0008 intentionally do not select a mandatory database/event store. Choosing SQLite as shared platform architecture would exceed the minimum R34 requirement and risk hidden product/platform coupling.

### C. Python pickle / process-object snapshots

Rejected. Opaque/runtime-coupled representation conflicts with portability, inspectability and safe migration goals and expands deserialization risk.

### D. One mutable JSON snapshot only

Rejected as the sole canonical representation. It makes historical append-only event/effect evidence and crash/retry reasoning weaker than immutable per-operation records. Rebuildable snapshots/indexes remain allowed as derived acceleration.

### E. External DMS/object store/event database

Deferred. Unnecessary for the bounded Local / Persistent Internal / owner-operated M10-alpha slice and would introduce infrastructure/operational commitments not justified by current evidence.

## 6. Consequences

Positive:

- removes the known R34 restart/recovery blocker without overbuilding a universal storage platform;
- preserves open, inspectable and reversible owner-local state;
- allows exact state reconstruction without consequential replay;
- aligns durable idempotency/retry evidence with RFC-0005/RFC-0006;
- reuses the existing secured owner-local runtime model and content-addressed bytes.

Costs/risks:

- filesystem atomicity and crash behavior need explicit tests;
- schema migration and corrupted/partial-record behavior must fail safely;
- backup must cover governed metadata and referenced bytes coherently;
- the product-local implementation must not become an accidental undocumented platform dependency;
- this does not provide multi-node transactions, distributed consensus, customer-production HA or an external archival guarantee.

## 7. Migration / reversal path

1. Existing staged materials and transient outputs remain unchanged and non-canonical.
2. Existing pre-ADR in-memory canonical sessions are not retroactively invented as durable history. Only evidence that can be exactly reconstructed from retained canonical artifacts may be migrated; otherwise the owner must perform a new governed admission/promotion.
3. New accepted implementation writes immutable schema-versioned records.
4. A future store can import/export these records through an explicit migration that preserves semantic identities/history and verifies read-after-write equivalence.
5. Reversal may disable this Company-local adapter and migrate the same governed state to a replacement store; it must not silently discard canonical history.

## 8. Acceptance criteria

ADR-0002 may become `Accepted` only after:

1. functional cross-review has no unresolved material objection;
2. the exact reviewed proposal blob is identified;
3. residual owner authority explicitly approves that exact proposal;
4. a canonical approval record exists independently of the acceptance publication;
5. ADR index and roadmap are synchronized;
6. read-after-write verification is complete.

Acceptance does not itself close R34 or M10-alpha. Implementation + recovery evidence + the real owner-operated cycle remain required.

## 9. Functional cross-review

Maximum: 7 iterations. This review is not formal approval.

### Iteration 1 — architecture / RFC boundary

Finding: a durable store is required, but selecting a platform-wide DB/event store would exceed RFC scope and the R34 need.

Resolution: make the decision explicitly Company Workspace product-local, behind existing semantic owners, with no shared storage contract.

Result: `PASS after revision`.

### Iteration 2 — event / idempotency / crash boundary

Finding: one mutable snapshot can lose the distinction between append-only historical evidence, successful effect and uncertain retry state.

Resolution: immutable per-operation records are authoritative; snapshots/indexes only derived. Success requires durable record + read-after-write; recovery never replays effects.

Result: `PASS after revision`.

### Iteration 3 — security / privacy / data minimization

Finding: serializing full runtime objects could accidentally persist secrets/raw content and create opaque unsafe snapshots.

Resolution: schema-specific JSON contains only reconstruction/evidence fields; raw bytes stay in existing content-addressed stores; credentials/secrets and unnecessary content are excluded.

Result: `PASS after revision`.

### Iteration 4 — portability / migration

Finding: an internal filesystem format could become hidden coupling or inaccessible state.

Resolution: open schema-versioned JSON, explicit export/migration semantics, no consumer dependence on paths/filenames, no pickle/proprietary encoding.

Result: `PASS`.

### Iteration 5 — product/platform and lifecycle integrity

Finding: a successful local mechanism could be mistaken for a promoted Platform Capability or production-readiness claim.

Resolution: explicitly retain product-local ownership, Provisional Product Contract scope and Local / Persistent Internal environment; promotion/reuse remains a separate governed decision.

Result: `PASS`.

Material objections after iteration 5: **none at proposal level**.

## 10. Current disposition

- proposal: `ADR-0002 v0.1.0`;
- status: `Proposed`;
- functional cross-review: `PASS after 5 iterations`;
- material unresolved review objections: none;
- exact owner approval: **pending**;
- implementation reliance for canonical closure: **not yet admitted**;
- R34: remains `BLOCKED / NOT PASS`;
- M10-alpha: remains unclaimed.

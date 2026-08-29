# P10.05 — Reviewed generated-output promotion boundary — closure review

Status: `Complete / PASS`
Date: `2026-08-29`
Owner: `ООО «Арвектум»`
Task classification: `product_contract`
Constitution: `1.2.0` — `Ratified`, frozen
RFC baseline: RFC-0001 through RFC-0008 `1.0.0` — `Accepted`
Accepted ADR: `ADR-0001 — Productive Workspace Browser Application Topology`
Product Contract: `P10.02 Arvectum Company ↔ Productive Workspace — Provisional 0.2.0`
Roadmap baseline at task start: `ROADMAP 2.97.4`; `PHASE-10 1.0.4`; `P10.05 — Current`
Implementation PR: `#29 — P10.05 implementation`
Reviewed implementation head: `738ceb53afa3d955c8cb36627ba142e069f3bde0`

## 1. Closure statement

P10.05 is `Complete / PASS` for the exact bounded `Local / Persistent Internal / owner-operated` Productive Workspace/reference-runtime scope.

The implementation closes the Product Contract reliance gate that P10.02 `Provisional 0.2.0` deliberately left unavailable until P10.05 implementation and review. It makes the already-admitted operation `company.generated-output.promote-reviewed` available only through an explicit owner review lifecycle and a separate RFC-0005 Governed Execution canonical-mutation command.

A generated output remains `TransientOutput` by default. Review, opening, download, rejection, keeping transient and requesting promotion are not canonical admission. A successful promotion creates a separate immutable governed Company Document/Artifact version, an explicit Organizational Asset designation and canonical RFC-0006 Event evidence. The source transient output is not relabelled or rewritten into canonical history.

P10.05 does not amend Constitution or Accepted RFC/ADR, does not create Product Contract `0.2.1`, does not promote Product Contract `0.2.0` to `Stable`, does not promote a Platform Capability to `Active`, and does not establish M10-alpha.

## 2. Canonical authority checked

The closure review re-checked the canonical authority chain rather than relying on project chat or model memory:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — canonical change and Transient Output / governed asset boundaries;
4. RFC-0004 — Product Contract lifecycle and mandatory contract before governed platform reliance;
5. RFC-0005 — Governed Execution, exact material/version pins, six independent gates, retry/idempotency/uncertainty and AI authority boundary;
6. RFC-0006 — append-only canonical Event/provenance/evidence and replay safety;
7. RFC-0007 — Document/Artifact/Observation do not automatically become validated Knowledge;
8. RFC-0008 — generated Artifacts are Transient Outputs by default and require explicit governed promotion;
9. ADR-0001 — Productive Workspace browser/BFF trust boundary, same-origin/CSRF/server-side revalidation and exact release asset semantics;
10. P10.01 authority matrix — generated-output review dispositions and promotion semantics;
11. lifecycle-current P10.02 Product Contract `Provisional 0.2.0` — exact already-admitted `company.generated-output.promote-reviewed` boundary;
12. canonical master and Phase 10 roadmaps.

Conflict check result: **no material conflict with higher authority**.

Decision Authority Policy remains `Proposed 0.2.1`; no approved exact delegation is inferred. Residual Organizational Authority remains with the owner under Accepted governance.

## 3. Exact implemented lifecycle

The owner-facing lifecycle is:

```text
Generated Artifact
    ↓
TransientOutput
    ↓ explicit owner review
 ┌──┼─────────────────────────────┐
 ↓  ↓                             ↓
Reject   Keep transient      Request promotion
 |          |                       |
 |          |                       ↓ new explicit command
 |          |              current server-side revalidation
 |          |                       ↓
 |          |              RFC-0005 Governed Execution
 |          |                       ↓ six independent ALLOW gates
 |          |                       ↓
 |          |              new governed Document/Artifact Version
 |          |                       + Organizational Asset designation
 |          |                       + canonical promotion Event
 |          |                       |
 └──────────┴──────── source remains TransientOutput
```

Review state is product-local and explicitly non-canonical. `PromotionRequested` is necessary but insufficient for canonical mutation.

The final promotion command re-resolves and revalidates the exact output and exact admitted source before any canonical effect.

## 4. Product Contract boundary

P10.05 uses the lifecycle-current P10.02 Product Contract `Provisional 0.2.0` without changing its normative substance.

The executable projection is pinned to the canonical P10.02 Subject/Version and immutable approved publication evidence. It admits only:

- operation `company.generated-output.promote-reviewed`;
- one exact Native promoted Company Document/Artifact output;
- exact read reliance on the already admitted Company source Document Version;
- explicit Organizational Asset designation write;
- RFC-0005 canonical-mutation semantics.

The projection remains non-authoritative implementation evidence and lifecycle status remains `Provisional`.

No hidden storage table, undocumented private API, private stream or product-specific schema is made into a Product Contract dependency.

## 5. Authority and security boundary

The productive command requires all six independent current RFC-0005 gates:

1. Actor Assurance;
2. Authorization;
3. Organizational Authority;
4. Data Governance;
5. Validation;
6. Consequential Approval.

The exact local promotion grant is least-privilege and covers only:

- operation: `company.generated-output.promote-reviewed`;
- resource: `company-generated-outputs`;
- access path: `local`.

That grant satisfies Authorization only. The implementation rejects a grant representation that claims to satisfy Organizational Authority or Consequential Approval.

The current bounded provider requires exactly one enabled attributable human owner in the current Organization, re-authenticates the P7.04 credential, resolves residual owner Organizational Authority independently, and records the explicit owner promotion command as a separate consequential-approval basis.

Workspace session, button visibility, CSRF success, Product Contract possession and technical access do not create Authorization or Organizational Authority.

No promotion grant is auto-provisioned by Workspace. Provisioning remains an explicit administrative action.

## 6. Exact source, provenance and handling

Promotion resolves the exact transient output bytes and re-computes SHA-256. The command fails closed if the digest differs from the retained transient manifest.

The generating source must resolve to exactly one currently admitted Company Asset version in the current bounded canonical state. The admitted source Artifact digest must equal the retained generation source digest.

Promotion evidence preserves, where retained and available:

- exact transient output identity/version;
- exact transient output Artifact identity and SHA-256;
- exact admitted source Document Subject/Version;
- exact admitted source Artifact identity;
- exact source Organizational Asset designation Subject/Version;
- retained generation/source provenance;
- Product Contract Subject/Version;
- Workflow Subject/Version;
- Execution Subject/Version;
- six gate-decision versions;
- resulting canonical Document/Artifact version;
- resulting Organizational Asset designation;
- resulting canonical promotion Event.

Historic F11/P10.04 generation manifests did not retain a separately versioned generation configuration or generation-input digest. P10.05 records those fields truthfully as `not-retained` rather than inventing evidence. This closure makes no stronger reconstructability claim than the retained evidence supports.

Classification, purpose, rights, retention, deletion and permitted-reuse semantics are inherited from the exact admitted source handling evidence. The bridge verifies source designation handling against the admitted Artifact and does not silently widen derived-output handling.

## 7. Canonical effect and retry semantics

Only the domain-neutral shared promotion semantic owner performs the CAP-001 admission call.

Before effect it validates:

- Governed Execution admission for `CANONICAL_MUTATION`;
- Organization scope continuity;
- exact Product Contract/Workflow/operation continuity;
- all six current gates and their independent evidence;
- exact transient Artifact identity/state/digest;
- exact retained generation/source provenance;
- reviewed Data Governance handling;
- current governed Actor attribution.

Successful effect creates:

1. one immutable governed Document/Artifact Version;
2. one explicit immutable Organizational Asset designation;
3. one canonical `platform.generated-output.promoted` Event;
4. one keyed-idempotent successful consequential-attempt record in the bounded reference state.

The source transient manifest remains `TransientOutput` with `canonical_authority = false`.

An exact retry token is bound to the immutable promotion fingerprint. Rebinding the token to different content fails. An exact successful retry resolves the existing result rather than silently duplicating canonical effect. An uncertain prior outcome requires reconciliation before retry.

## 8. Browser / BFF boundary

P10.05 adds internal same-origin Workspace routes for:

- listing generated outputs and truthful review state;
- recording a non-canonical review disposition;
- issuing the separate promotion command.

Current session/Organization context is revalidated server-side. State-changing requests require CSRF validation. Missing or changed exact admitted-source evidence fails closed.

Owner UX clearly distinguishes:

- `TransientOutput` source state;
- review/disposition state;
- inherited handling;
- promotion request;
- the final Governed Execution command;
- the separate canonical result after success.

No send, sign, publish or external-effect control is introduced by P10.05.

## 9. Functional cross-review

Maximum allowed iterations: 7.

### Iteration 1 — authority / Product Contract boundary

Finding: risk of treating P10.05 implementation as a reason to create Product Contract `0.2.1` or to collapse possession of `0.2.0` into authority.

Resolution: use only the exact already-admitted P10.02 `0.2.0` operation; keep projection non-authoritative and Provisional; retain six independent current gates.

Result: `PASS after bounded confirmation`.

### Iteration 2 — transient / canonical state separation

Finding: risk that owner review or successful promotion could relabel the generated file itself as canonical.

Resolution: review remains non-canonical; the source manifest is never rewritten; promotion creates a separate immutable Document/Artifact Version and asset designation.

Result: `PASS`.

### Iteration 3 — provenance / handling integrity

Finding: risk of silently broadening derived-output handling or fabricating generation evidence absent from historical manifests.

Resolution: inherit and verify source handling exactly; pin exact output/source identities and digests; expose absent historical generation-config/input-digest evidence as `not-retained`.

Result: `PASS after bounded reconciliation`.

### Iteration 4 — fail-closed / retry / exception boundary

Finding: exact admitted-source loss could surface through a lower-layer P10.04 exception rather than the P10.05 BFF unavailable contract.

Resolution: preserve lower-layer fail-closed semantics and normalize the browser boundary to truthful `503` unavailability; tests assert no canonical effect. Keyed idempotency and uncertain-outcome reconciliation remain explicit.

Result: `PASS after revision`.

### Iteration 5 — browser / authority / external-effect boundary

Finding: risk that a visible final button, existing session or exact Product Contract could be mistaken for current authority, or that promotion UX might imply send/sign/publish.

Resolution: explicit separate promotion authorization grant; command-time server-side six-gate revalidation; no auto grant; UI states it does not confer authority; no send/sign/publish surface.

Result: `PASS`.

### Iteration 6 — exact release / frontend reproducibility

Finding: functional source tests passed but the checked-in frontend `dist` initially differed from the reproducible CI build.

Resolution: exact CI-produced frontend build was reconciled into the branch; generated `dist` now contains the reproducible hashed asset `index-Sugv74QQ.js`; the temporary reconciliation workflow was removed before final quality evidence. Both required normal CI workflows then passed on the same exact reviewed implementation head.

Result: `PASS after revision`.

Material objections after iteration 6: **none**.

This functional review is implementation evidence only. It is not Product Contract `Stable` approval, Platform Capability lifecycle promotion, operational-readiness approval, R34 PASS, M10-alpha evidence or delegation of Organizational Authority.

## 10. Verification and CI evidence

Reviewed implementation head:

`738ceb53afa3d955c8cb36627ba142e069f3bde0`

Exact-head quality evidence:

- Productive Workspace CI `#104`, run `33245781308` — `success` on exact head `738ceb53afa3d955c8cb36627ba142e069f3bde0`;
- Reference Python CI `#115`, run `33245781326` — `success` on the same exact head.

Frontend build reconciliation evidence:

- CI-generated artifact `p10-05-workspace-dist` digest `sha256:439a58b307a2fea5d41c8b6e7c1c4b10a764ec8d7bec8ce7e4ca1e24fc476de8`;
- exact committed generated JS blob after reconciliation: `reference/python/workspace_frontend/dist/assets/index-Sugv74QQ.js`, blob `765378f970e8c1d5b7c488b05b6e53c31e643336`;
- temporary reconciliation workflow removed before the exact-head green CI above.

Tests cover, among other cases:

- no ambient promotion grant and explicit revocation;
- Reject / Keep transient / PromotionRequested causing no canonical mutation;
- all six independent current gates;
- Authorization distinct from Organizational Authority;
- exact inherited handling;
- exact admitted source requirement;
- fail-closed missing-source behavior;
- idempotent promotion with one canonical Event/effect;
- source remaining `TransientOutput` after promotion;
- no validated Knowledge creation;
- no send/sign/publish availability;
- BFF CSRF/current-context behavior;
- owner-facing separate final Governed Execution action.

## 11. Explicit non-claims

P10.05 closure does **not** establish or claim:

- `R34` PASS;
- `M10-alpha` achievement;
- a real owner-operated M10-alpha asset-cycle evidence run;
- restart-durable canonical promotion/admission persistence;
- a selected database, object store, durable transaction manager or durable idempotency ledger;
- a public/stable API, SDK, browser contract or independently versioned service;
- Product Contract `Stable` status;
- Platform Capability `Active` status;
- customer/external `Production` readiness;
- SLA, support, compatibility, certification or broader conformance commitments;
- automatic validated Knowledge creation;
- legal approval, legal validity, signing, filing, external send or publication;
- cross-Organization admission/reuse or multi-Organization production proof;
- autonomous AI Organizational Authority, Authorization or final consequential approval;
- an approved authority delegation absent canonical approval evidence.

The current canonical/promotion state implementation remains deliberately bounded/reference/in-memory. Loss of the exact admitted source state after restart therefore fails closed; this closure does not disguise that limitation as durable persistence.

## 12. Exit result and next gate

P10.05 exit outcome is satisfied for its declared scope:

> a generated `TransientOutput` can be explicitly reviewed and either rejected/kept transient or requested for governed promotion; promotion can create a separate governed Company Document/Asset version only through the applicable Product Contract and RFC-0005 Governed Execution path while preserving exact retained input/output/provenance/handling evidence and remaining distinct from RFC-0007 validated Knowledge, legal approval, signing, external send and publication.

Next canonical critical-path gate:

`R34 — M10-alpha Asset Governance / Usability Review`.

R34 still requires **real owner evidence, not synthetic fixtures**, for the first asset cycle. P10.05 closure alone does not satisfy R34 or M10-alpha.

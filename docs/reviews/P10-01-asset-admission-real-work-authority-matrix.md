# P10.01 — Asset/admission + real-work authority matrix

Status: `Complete / PASS`
Date: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform`, `product_specific` and `governance`
Roadmap: `Phase 10 — Operational Work & Organizational Assets`
Constitution basis: `1.2.0` — `Ratified`, frozen
RFC basis: RFC-0001 through RFC-0008 `1.0.0` — `Accepted`
Accepted ADR: `ADR-0001 — Productive Workspace Browser Application Topology`
Current Product Contract: `P9.11-F11 Arvectum Company ↔ Productive Workspace — Provisional 0.1.0`
Predecessor: `P10.00 — Complete / PASS`
Successor: `P10.02 — Product Contract evolution for Company assets + operational work`

## 1. Purpose

P10.01 fixes the minimum authority, asset and real-work semantics required before Arvectum OS is allowed to implement canonical Company asset admission or any broader product operational action through Productive Workspace.

This matrix is deliberately semantic. It does not select a physical database/schema, create a sixth Kernel primitive, promote a Platform Capability, make a generated artifact canonical, create a universal `Task` primitive, or grant authority to browser state, AI output, technical access or Product Contract possession.

The matrix preserves the following binding distinctions:

- receipt/staging is not canonical admission;
- a Governed Organizational Asset is an explicit governed designation, not a persistence side effect;
- generated output is `TransientOutput` by default;
- Authentication, Authorization, Organizational Authority, Data Governance, validation and Consequential Approval are separate decisions;
- product/company action semantics remain product-owned;
- Actionable Work is a non-authoritative projection, not a source of work or authority;
- external sources remain authoritative where `External Reference` applies;
- exact versions materially relied upon by consequential execution are pinned.

## 2. First-slice Company asset classes

The first asset scope is constrained to the real F11 material classes plus reviewed generated output.

| Asset class | Company-owned semantic role | Authority after successful admission | Default purpose / handling | Rights / usage affirmation | Version / supersession | Parsing / extraction | Knowledge status |
|---|---|---|---|---|---|---|---|
| Brandbook | `Брендбук` | `Native` for the exact Company-held governed Document/Artifact version | internal brand governance and exact-version generation; Organization-scoped | owner/operator affirms lawful Company purpose and right to retain/use | immutable admitted versions; later replacement creates a new version; historical version remains addressable subject to lawful retention/deletion | safe PDF/DOCX/text extraction MAY be derived where available; extraction remains non-authoritative | no automatic Knowledge promotion |
| Logo / brand asset | `Логотип` or other Company brand asset | `Native` for admitted bytes/version | internal brand use and exact-version generation | same rights affirmation; provenance required | immutable version; later visual replacement is a new version, not overwrite | image metadata/rendering allowed; SVG only after safe parsing/sanitization; no active content execution | no automatic Knowledge promotion |
| Company document template | `Шаблон документа` | `Native` for admitted template version | exact-version input to Company document generation | rights/purpose affirmation required | immutable template versions; a newer version may supersede for future use without invalidating historical executions | safe DOCX/PPTX/TXT/MD parsing as needed; macros/executable content excluded from first slice | template rules remain Company-owned semantics, not platform Knowledge by default |
| Company source/reference material held by Company | `Организационный источник` or bounded Company source material | `Native` only for the exact Company-held admitted copy/version | internal source/reference use for declared purpose | source/right/provenance declaration required | immutable admitted version; newer source copy creates a new version | bounded safe parsing/extraction allowed | source content is not validated Knowledge by admission alone |
| External source/reference material not copied into Company authority | `Организационный источник` | `External Reference` | governed reference to an externally authoritative source | permitted access/use basis must be explicit | local governed reference versions may change; external authority remains external | retrieval/transformation only within declared rights/purpose | no automatic Knowledge promotion |
| Project-bound generated document considered for internal acceptance | Company product-owned document type | `TransientOutput` until separate reviewed promotion; then `Native` for the admitted exact governed Document/Artifact version | internal project work | exact input provenance plus owner review required | generated candidate is immutable/transient by digest/reference; admitted result receives governed identity/version; revisions produce new candidates/versions | generated content may be rendered/inspected; no execution of embedded active content | no automatic Knowledge promotion |

### 2.1 First-slice exclusions

The first admission slice excludes:

- executable files, scripts, installers and arbitrary packages;
- macro-enabled Office formats and uncontrolled active content;
- archives with uncontrolled nested content;
- automatic external sending, signing, filing or publication;
- automatic conversion to Policy, Standard, Decision or validated Knowledge;
- cross-Organization reuse or admission;
- unbounded local-disk indexing;
- asset admission based only on download, preview, AI confidence, repeated use or storage persistence.

A later expansion requires the minimum sufficient Product Contract/version and applicable governance evidence.

## 3. Authority and canonical-state matrix

| Subject / state | Canonical? | Authority mode / authority | Consequential reliance rule |
|---|---:|---|---|
| F11 staged upload | No — `StagedNonCanonical` | Company-provided source with staging provenance; no canonical asset authority | may be inspected and proposed for admission; must not be relied upon as an admitted organizational asset |
| External governed source reference before admission | No canonical asset yet | external system/source remains authoritative | may be staged as an admission candidate only |
| Admitted Company Document/Artifact version | Yes | `Native` for the exact Company-held governed version; underlying third-party fact rights/source remain separate | exact Version Identity pinned before consequential use |
| Admitted external-reference asset | Yes as governed reference | `External Reference`; external source remains authoritative for declared fact/content scope | exact governed reference version plus external-source/freshness semantics pinned where material |
| Generated preview/draft | No — `TransientOutput` | derived product output, non-authoritative | may be reviewed/downloaded; neither action promotes it |
| Reviewed and successfully promoted generated Company document | Yes | `Native` for admitted governed version | promotion itself is a separate consequential governed operation |
| Asset discovery/search/read model | No | rebuildable derived projection | must retain source/version/freshness provenance; cannot replace canonical state |
| Actionable Work card/view | No | derived projection of an explicit product/company request source | may explain and route; cannot create urgency, assignment, permission, approval or Organizational Authority |
| Product/company request source | Depends on owning product/source | remains under owning product/company authority model | exact source/version and effective Product Contract must be resolved before consequential action |

## 4. First-slice admission operation matrix

### 4.1 `company.asset.admit-staged-version`

Purpose: admit one exact staged Company-held material version into governed canonical Document/Artifact history and explicitly designate it as a Governed Organizational Asset within the declared Company role/scope.

| Decision dimension | Required semantics |
|---|---|
| Actor / Authentication | current attributable owner/operator Principal and session context resolved server-side; stronger assurance may be required by later policy, but session existence alone is insufficient |
| Authorization | explicit permission to request admission for the exact Organization/resource/operation; deny by default |
| Organizational Authority | current residual authority is the owner unless an approved delegation applicable to this exact admission exists |
| Data Governance | Organization, declared purpose, classification/handling, rights/source affirmation, retention/deletion rule and permitted reuse must be resolved |
| Validation / review | exact content class, size, digest, safe-storage status, provenance, Company semantic role and required metadata reviewed; unsupported/ambiguous/unsafe input fails closed |
| Consequential Approval | explicit owner approval for canonical admission under current residual-authority state; UI button/technical access/AI proposal cannot substitute |
| Exact pins | staged item identity/version, bytes/content digest, Product Contract version, workflow/operation definition and materially relied-upon governed control versions |
| Canonical effect | create immutable canonical Document/Artifact version and explicit asset designation under one stable subject lineage; never mutate staged history into canonical by relabeling |
| Event / provenance | preserve Governed Execution identity/version lineage and successful canonical admission/designation evidence; canonical Event where required by the admitted execution/event contract; telemetry alone is insufficient |
| Failure / cancellation | fail closed; no canonical asset/version claim on validation/gate/storage/evidence uncertainty; cancellation/rejection does not fabricate a successful asset version; retry must be idempotent for the same admitted intent |

### 4.2 `company.asset.admit-external-reference`

Purpose: canonically govern a Company asset/reference while preserving an external authoritative source.

| Decision dimension | Required semantics |
|---|---|
| Actor / Authentication | same attributable server-side actor requirements as staged admission |
| Authorization | explicit admission permission for the exact Organization/reference scope |
| Organizational Authority | owner residual authority unless an approved exact delegation exists |
| Data Governance | purpose, rights/access basis, classification, permitted local transformations, retention/deletion of local governed metadata and portability declared |
| Validation / review | external system/object/source identity, authority scope, retrieval/freshness expectations, conflict/failure behavior and provenance are explicit enough to prevent competing truth |
| Consequential Approval | explicit owner approval under the current authority state |
| Exact pins | exact candidate reference/version descriptor, Product Contract version, operation/workflow version and materially relied-upon controls |
| Canonical effect | create/update immutable canonical governed-reference version with `External Reference`; do not claim external bytes/facts as `Native` |
| Event / provenance | preserve admission execution and reference/source provenance; successful consequential effect evidence must be reconstructable |
| Failure / cancellation | fail closed on unresolved authority/source/rights/freshness semantics; no silent fallback to `Native` or stale local truth |

### 4.3 `company.generated-output.promote-reviewed`

Purpose: after explicit owner review, promote one exact generated `TransientOutput` into a governed Company Document/Artifact version. P10.02 may admit the contract boundary; the implementation path is P10.05 and remains unavailable until that work is complete and reviewed.

| Decision dimension | Required semantics |
|---|---|
| Actor / Authentication | current attributable owner/operator context resolved server-side |
| Authorization | explicit permission for the promotion operation and target Company/project scope |
| Organizational Authority | owner residual authority unless a later approved delegation applies |
| Data Governance | output classification, purpose, rights, source/input provenance, retention/deletion and permitted reuse resolved before promotion |
| Validation / review | exact generated artifact digest plus materially relied-upon input versions/configuration; human review decision is explicit |
| Consequential Approval | explicit owner approval to admit this exact reviewed output as governed Company state |
| Exact pins | transient artifact identity/digest, generation provenance, exact input asset versions, applicable Product Contract/workflow/control versions |
| Canonical effect | create a new immutable governed Document/Artifact version/designation; the transient candidate itself is not silently rewritten into canonical history |
| Event / provenance | governed promotion execution and resulting canonical identity/version are reconstructable; rejection remains distinguishable from success |
| Failure / cancellation | reject/keep transient/failed/uncertain remain truthful terminal states; retry cannot duplicate the same canonical effect silently |

## 5. Generated-output lifecycle decision matrix

```text
TransientOutput
      ↓ owner review
 ┌────┼──────────────────────┐
 ↓    ↓                      ↓
Reject  Keep transient       Request governed promotion
 |       |                      |
 no      no canonical          ↓ current authz/authority/data governance
 canonical change              ↓ exact-version revalidation
 change                        ↓ Governed Execution
                               ↓
                         Admitted Company Document/Asset Version
```

Rules:

1. generation, preview, open, download, edit-in-browser intent or repeated reuse does not create canonical status;
2. rejection does not erase the transient provenance required by applicable bounded retention/evidence rules;
3. owner review is necessary but is not by itself a canonical write — the admitted Governed Execution must succeed;
4. the promoted version retains exact derivation/input provenance;
5. promotion does not create validated Knowledge;
6. external sending/signing/publication remains a separate product/governance scope.

## 6. Real Action Request source classes

Phase 10 recognizes real requests only when they originate from an explicit product/company source with a truthful current state. No synthetic request is created to satisfy M10.

| Source class | Source of truth | Workspace role | Product Contract requirement | Consequentiality |
|---|---|---|---|---|
| Company asset admission/review request | Company Workspace staged/generated item plus exact source/provenance | explain pending review and route owner to the governed admission/promotion flow | evolved Company ↔ Workspace contract lineage | canonical mutation when admitted/promoted |
| Tender Operator / Tender Agent result requiring owner disposition | exact product-owned canonical/product source when a genuine item exists | non-authoritative projection plus product entry point | effective Tender/Product Contract must explicitly cover the requested platform/action reliance | depends on the actual tender operation; no ambient authority |
| Discount Parser controlled publication/approval request | exact product-owned current request/source when one naturally exists | projection/entry point only | effective product/platform Product Contract required before any governed platform reliance | likely external/product mutation; exact operation must declare side effects |
| Other product-owned request | explicit canonical/product source with stable identity/version/freshness | projection/entry point only | exact effective Product Contract must exist before consequential execution | determined by the product-owned operation definition |
| Chat/model suggestion without admitted source | none | may be shown only as non-authoritative suggestion if useful | cannot become an actionable governed request by itself | none until a governed product/company source exists |

## 7. First real action journey disposition

No product-specific consequential action is selected or fabricated in P10.01.

The first real action journey is selected only when a genuine request naturally exists. At selection time the record must identify:

- product/company owner;
- exact source of truth and immutable source/version reference where material;
- exact effective Product Contract dependency;
- requested operation and side-effect class;
- current Authorization, Organizational Authority, Data Governance, validation and approval requirements;
- expected completed/blocked/failed/uncertain outcomes;
- reconstruction evidence required by RFC-0005/RFC-0006.

The previously deferred natural F08 recheck remains eligible when a real request actually appears, but its existence is not asserted by this matrix.

## 8. Product/platform ownership boundary

### Platform/domain-neutral responsibility

The platform may own only reusable mechanics such as:

- stable subject/version identities and immutable canonical lineage;
- generic Document/Artifact and asset-designation mechanics;
- Organization/Actor attribution;
- domain-neutral staging/admission envelope;
- authorization/data-governance enforcement points;
- RFC-0005 Governed Execution envelope and exact-version pinning;
- generic provenance/event/reconstruction mechanics;
- non-authoritative projection/application infrastructure;
- portability/export mechanics.

### Company/product responsibility

Arvectum Company and the relevant product retain:

- asset roles/taxonomy and business meaning;
- brand/template/document semantics;
- admission usefulness criteria beyond domain-neutral safety/governance controls;
- product-specific approval/business rules;
- product Action Request semantics and state machine;
- urgency, priority, assignment and business interpretation;
- product operation/side-effect semantics;
- owner-facing product UX composition.

No Company/product taxonomy is promoted to Kernel or shared platform semantics by P10.01.

## 9. Functional cross-review

Maximum iterations: 7.

### Iteration 1 — Kernel / authority boundary

Finding: risk of treating `Organizational Asset` and Actionable Work as new Kernel primitives.

Resolution: asset remains an explicit designation above the five Kernel primitives; Actionable Work remains a non-authoritative projection over product/company requests.

Result: `PASS after revision`.

### Iteration 2 — receipt/admission and authority separation

Finding: risk that owner-operated simplicity could collapse session, authorization, owner authority and approval into one UI action.

Resolution: the operation matrix separately records Actor/Authentication, Authorization, Organizational Authority, Data Governance, validation and Consequential Approval for every first-slice canonical mutation.

Result: `PASS after revision`.

### Iteration 3 — external authority / generated output / Knowledge

Finding: risk of converting source/reference content to `Native`, treating generated files as canonical on download, or treating admitted documents as validated Knowledge.

Resolution: explicit `External Reference` path; generated output remains transient until separate governed promotion; Knowledge promotion remains out of scope.

Result: `PASS after revision`.

### Iteration 4 — product operational work boundary

Finding: an inventory of potential product actions could be mistaken for authority to execute them.

Resolution: P10.01 defines source classes only. Product-specific consequential execution requires a genuine request, an exact effective Product Contract that declares the operation, and current server-side gate revalidation. No first action is fabricated.

Result: `PASS`.

Material objections after iteration 4: **none**.

Functional cross-review is not Product Contract approval, lifecycle promotion, Platform Capability promotion, operational-readiness approval or delegation of Organizational Authority.

## 10. Exit finding

P10.01 satisfies its Phase 10 exit criteria:

- first-slice asset classes and admission semantics are explicit;
- receipt/generation remain distinct from canonical admission;
- Action Request source classes are explicit without a universal Kernel `Task` primitive;
- Authentication, Authorization, Organizational Authority, Data Governance, validation and approval remain distinct;
- no Product Contract expansion has been made by this matrix itself;
- P10.02 has exact sufficient inputs for Product Contract version design;
- R33 review questions can now be evaluated against explicit semantics.

Verdict:

> **`P10.01 = Complete / PASS`.**

Next canonical action:

> **`P10.02 — evolve the existing Arvectum Company ↔ Productive Workspace Product Contract lineage to the minimum sufficient Company-asset + operational-entry boundary, then obtain exact owner approval before Provisional reliance.`**

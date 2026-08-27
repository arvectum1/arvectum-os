# P10.01 — Asset/admission + real-work authority matrix

Status: `Complete / PASS — design and authority baseline only`
Version: `1.0.0`
Date: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`, `product_specific` and `governance`
Roadmap work item: `P10.01 — Asset/admission + real-work authority matrix`
Parent roadmap: [`PHASE-10-OPERATIONAL-WORK-ORGANIZATIONAL-ASSETS.md`](../roadmap/PHASE-10-OPERATIONAL-WORK-ORGANIZATIONAL-ASSETS.md)
Predecessor: [`P10-00-post-M9-outcome-selection-and-phase-10-activation.md`](P10-00-post-M9-outcome-selection-and-phase-10-activation.md)
Current Company Workspace Product Contract: [`P9.11-F11 Provisional 0.1.0`](../contracts/P9-11-F11-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.1.0.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `Accepted 1.0.0`; ADR-0001 `Accepted`
Decision-authority note: `DECISION-AUTHORITY-POLICY 0.2.1` remains `Proposed` and is non-normative; this artifact creates no new delegation. Residual authority remains with the owner under the Accepted baseline.
Next canonical action: `P10.02 — Product Contract evolution for Company assets + operational work`
Blocking review after P10.02: `R33 — Asset / Product Contract / Authority Boundary Review`

## 1. Outcome

P10.01 fixes the semantic and authority baseline required before canonical Company-asset admission or new real product/company action execution is implemented.

The baseline separates four concerns that MUST NOT be collapsed:

1. **subject state** — staged/transient material versus an explicitly admitted canonical asset version;
2. **source authority mode** — whether Arvectum OS is authoritative for the admitted version or references an external authoritative source;
3. **technical access** — Authentication/Actor resolution and Authorization;
4. **organizational decision authority** — Organizational Authority, Data Governance, validation/review and Consequential Approval where applicable.

The same human owner may satisfy more than one decision gate in the current owner-operated environment, but the gates remain semantically distinct and must be revalidated/recorded as applicable. A logged-in session, a visible button, a technical role, a Product Contract or an AI recommendation does not manufacture Organizational Authority.

P10.01 is deliberately a **design/evidence artifact**, not a Product Contract transition, implementation acceptance, Platform Capability promotion or operational-readiness approval.

## 2. Binding boundaries

This artifact applies these existing Accepted constraints rather than creating new foundational architecture:

- an Organizational Asset is a designation over existing RFC-0002/RFC-0008 semantics, not a sixth Kernel primitive;
- `StagedNonCanonical` receipt is not canonical admission;
- generated material remains `TransientOutput` by default;
- canonical asset/version admission is a consequential canonical mutation and therefore uses RFC-0005 Governed Execution;
- canonical Events/provenance remain append-only evidence under RFC-0006 semantics;
- admitted documents/assets do not automatically become RFC-0007 validated Knowledge;
- Authentication, Authorization, Organizational Authority and Data Governance remain distinct RFC-0003 concerns;
- AI may classify, summarize, draft, compare and propose, but is never the source of authority or final consequential approval;
- external authoritative systems remain authoritative when the declared source mode says so;
- historical replay never repeats an external side effect without new authorization;
- product-specific material roles, workflows, approval rules and action semantics remain product-owned;
- the existing F11 Product Contract `Provisional 0.1.0` is **not expanded by this artifact**.

## 3. Semantic axes

### 3.1 Subject/admission state

P10.01 uses the following semantic states/outcomes. They are not prescribed database enums or mandatory class hierarchies.

| State/outcome | Canonical? | Meaning |
|---|---:|---|
| `TransientOutput` | No | Generated/draft output. Useful output is still non-canonical until a separate admitted promotion succeeds. |
| `StagedNonCanonical` | No | Organization-scoped received material with exact version/digest/provenance retained for review/reuse inside the current Provisional F11 boundary. |
| `AdmissionRequested` | No by definition | A review/intent state. Merely requesting admission does not create the asset version. If a future implementation stores the request canonically, that storage is itself governed separately. |
| `AdmittedAssetVersion` | Yes | Explicit immutable canonical Company asset/document version created only by the admitted Governed Execution path. |
| `Rejected` | No admitted version created | Admission decision outcome. Rejection may still have bounded decision/evidence records where the effective contract requires them. |
| `Superseded` | Canonical historical version remains | A newer admitted version becomes effective without overwriting the earlier canonical version. |
| `Dispositioned/withdrawn` | Canonical history remains subject to applicable deletion/privacy rules | The version is no longer current/usable for the declared purpose; history is not silently rewritten. Exact disposal semantics remain subordinate-governance/contract work. |

### 3.2 Source authority mode

Source authority is orthogonal to admission state.

| Mode | Meaning in P10.01 |
|---|---|
| `Native` | Arvectum-controlled admitted record/version is authoritative for the declared Company asset scope. `Native` is a logical authority designation, not a mandated physical storage topology. |
| `External Reference` | An external source remains authoritative. Arvectum OS may canonically hold identity/reference/provenance/handling metadata permitted by contract, but does not become a competing source of truth. |
| `Governed Replica` | Accepted architecture permits this authority mode, but it is **not admitted into the first P10.01 Company-asset slice**. A later real integration need must declare exact sync/freshness/conflict/failure semantics before use. |

An admitted asset may therefore be `AdmittedAssetVersion + External Reference`; canonical admission of the reference metadata does not transfer source-of-truth authority from the external system.

## 4. First-slice Company asset matrix

The first slice is intentionally bounded to material classes already grounded by F11 and the Phase 10 roadmap.

`Classification/handling` below is a product-level handling expectation for the first owner-operated slice. P10.01 does **not** create a company-wide legal/data-classification policy or statutory retention schedule. Where an exact policy value does not yet exist, the admission path must require an explicit governed decision/reference rather than invent one.

| Asset class | Company-owned semantic role | First-slice source authority | Default purpose / handling expectation | Rights / usage gate | Retention / deletion expectation | Version / supersession | Parsing / extraction | Knowledge |
|---|---|---|---|---|---|---|---|---|
| **Brandbook** | Company brand guidance source used by Company work and generation | `Native` when the Company intentionally admits the exact controlled file; `External Reference` only when an explicitly declared external source remains authoritative | Company operational brand use; broader/public reuse is not inferred from admission | Owner must affirm Company ownership/license or another sufficient usage basis for the exact version | Keep current admitted version while operationally applicable; superseded history remains inspectable subject to applicable retention/deletion decisions; no invented automatic expiry | New admitted bytes create a new immutable version; prior versions are never overwritten | Text/structure/metadata extraction allowed only for the admitted Company purpose and current access/handling constraints | No automatic promotion to validated Knowledge/Policy/Standard |
| **Logo / brand asset** | Company visual brand asset | `Native` for the exact Company-controlled admitted file | Company brand/document production; external/public publication remains a separate use/action decision | Owner must affirm ownership/license and allowed use for the exact asset | Keep while used by Company; superseded variants remain historical subject to explicit disposition | New artwork/file is a new immutable version; current/effective designation is separate from identity | Technical metadata and bounded content analysis allowed for admitted purpose; no rights inference from file possession | No automatic Knowledge promotion |
| **Company document template** | Exact reusable template for Company documents and project-bound generation | `Native` for the exact admitted template | Internal Company document generation; external sending/signing/filing is not implied | Owner must affirm the Company may use/modify the exact template and any embedded assets/fonts/content | Keep while template is current; superseded template versions remain available for reconstruction subject to retention/deletion decisions | Every admitted template change is a new immutable version; generation pins the exact admitted version | Structure/placeholders/text extraction allowed for template validation/generation inside admitted purpose | Template contents are not validated Knowledge by admission |
| **Company source/reference material** | Source material used to inform Company work | `External Reference` by default when another source remains authoritative; `Native` only when the Company owns/controls the accepted copy and intentionally makes that exact copy authoritative for the declared Company purpose | Purpose must be explicit at admission/use; broad reuse is not inferred | Exact source/license/permission/custody basis must be captured as applicable. Storing a URL or possessing bytes is not evidence of legal usage rights | Retain reference/provenance only for the declared business purpose and applicable policy; copied bytes are not retained merely for convenience when rights/purpose do not support it | External-reference changes preserve prior source/version/freshness evidence; Native accepted copies are immutable versions | Extraction only when rights, purpose, classification and Product Contract permit it | Observation/content does not become validated Knowledge without a separate RFC-0007 path |
| **Project-bound generated document considered for internal acceptance** | Company document candidate created from exact admitted inputs/templates | Starts as `TransientOutput`; becomes `Native` only after explicit review and admitted promotion | Review/internal Company use before any later send/sign/publish action | Rights/provenance of all material inputs must remain reconstructable; owner review cannot cure missing input rights | Transient handling remains bounded; if admitted, retain according to the accepted Company-document purpose and later disposition rules | Every admitted generated result is a new immutable document/asset version; regeneration does not overwrite an admitted version | Parsing/validation allowed for exact output validation and admitted purpose | Admission as a document/asset is still not validated Knowledge |

### 4.1 First live asset-cycle preference

The preferred first M10-alpha admission candidate is a **real Company document template** already meaningful to ordinary Company work, because it exercises the full evidence chain:

`StagedNonCanonical exact template → owner review → canonical admission → later exact-version retrieval → real generated Company document as TransientOutput`.

This preference is sequencing guidance, not a requirement to fabricate or replace the real owner-selected material. Brandbook/logo admission may proceed in the same admitted Product Contract scope if P10.02 keeps that boundary minimum-sufficient and R33 finds no material objection.

## 5. Admission operations and authority matrix

These names are semantic operation labels for P10.01/P10.02 discussion, not stable API names.

### 5.1 `AdmitStagedNativeAssetVersion`

Purpose: turn one exact `StagedNonCanonical` Company-controlled material version into one immutable canonical `AdmittedAssetVersion` with `Native` source authority.

| Gate / concern | Required P10.01 decision |
|---|---|
| Authentication / Actor | Resolve current authenticated owner-operated Workspace actor/session at command time. |
| Authorization | Revalidate current technical permission for the exact Organization, candidate and requested operation. UI visibility or prior page load is insufficient. |
| Organizational Authority | Current owner residual authority must explicitly authorize the admission in this owner-operated scope unless/until an Accepted delegation says otherwise. Technical Authorization does not satisfy this gate. |
| Data Governance | Exact purpose, Organization scope, handling/classification decision/reference, rights basis and retention/deletion expectation must be present and valid for the version. This remains a distinct decision even when the owner is the same human. |
| Validation / review | Exact staged identity/version/digest/source/provenance and content-type/safety validation proportionate to the asset class must pass. |
| Consequential Approval | Canonical admission requires explicit owner confirmation in the current undelegated scope; future delegation/thresholds require approved governance and cannot be inferred from the Proposed Decision Authority Policy. |
| Product Contract | Effective P10.02 contract version must explicitly admit this operation and asset class before implementation/reliance. F11 `0.1.0` is insufficient. |
| Exact inputs | Organization, candidate/staged version, digest/content identity, semantic role, source authority mode, rights evidence/reference, handling/classification decision/reference, retention expectation/reference, contract version and workflow definition/version are pinned. |
| Canonical effect | Create exactly one immutable admitted asset/document version and current/effective relation/state as defined by the effective contract; never overwrite an admitted version. |
| Evidence | Governed Execution run/attempt, decision/authority evidence, exact input/version pins, resulting canonical state delta and canonical Event/provenance sufficient for reconstruction. |
| Failure | Fail closed on stale/missing/mismatched/revoked inputs or gates. No admitted version is created on failure/cancellation. |
| Retry | Same admitted intent must be idempotent; retry must not create duplicate asset versions. Current gates/preconditions are revalidated as required. |

### 5.2 `AdmitExternalReferenceAssetVersion`

Purpose: canonically admit a Company asset/reference whose external system/source remains authoritative.

All gates from `AdmitStagedNativeAssetVersion` apply, plus:

- authoritative source identity and authority scope must be explicit;
- retrieval/freshness/applicability semantics must be explicit enough for the declared use;
- canonical Arvectum state must not falsely claim the referenced bytes/content as Native authority;
- conflict behavior must prefer truthful source-state/reconciliation over silently forking a competing truth;
- copying/extracting external bytes requires separate rights/purpose support and does not follow automatically from admitting the reference.

`Governed Replica` is not a fallback for inconvenient External Reference behavior in the first slice.

### 5.3 `PromoteTransientOutputToAssetVersion`

Purpose: after human review, admit an exact generated `TransientOutput` as a new governed Company document/asset version.

All canonical-admission gates apply. In addition:

- exact generator/release/workflow identity and all material input versions are pinned;
- the output digest/version being reviewed is exactly the output being admitted;
- owner download/open/view is **not** admission;
- AI generation/recommendation is **not** approval;
- missing rights/provenance on material inputs blocks admission rather than being cured by owner acceptance;
- external send/sign/file/publish remains a separate consequential action unless a later effective Product Contract explicitly admits it.

### 5.4 `RejectAdmission`

Purpose: explicitly decline admission of an exact staged/transient candidate.

- creates no `AdmittedAssetVersion`;
- may preserve bounded review/decision evidence if required by the effective workflow/contract;
- does not imply deletion of the underlying staged/transient material unless a separate retention/disposition rule says so;
- must not rewrite or remove prior admitted canonical history.

### 5.5 `AdmitSupersedingAssetVersion`

Purpose: admit a new immutable version and make it current/effective according to the declared product semantics.

- uses the same admission gates as a new version;
- pins the predecessor/current version as a precondition;
- stale-current conflicts fail/reconcile rather than silently superseding the wrong version;
- predecessor remains historical subject to applicable access/retention/deletion rules;
- the new current/effective designation is a consequential canonical mutation through Governed Execution.

## 6. Generated-output decision matrix

Canonical lifecycle baseline:

```text
exact admitted inputs / allowed staged inputs
                ↓
        generate / transform
                ↓
          TransientOutput
                ↓
            owner review
        ┌───────┼──────────────┐
        ↓       ↓              ↓
      reject  keep transient  request admission
                                ↓
                    current gates revalidated
                                ↓
                       Governed Execution
                         ┌──────┴──────┐
                         ↓             ↓
                      admitted       blocked/
                    asset version    failed/cancelled
```

| Owner choice | Canonical asset created? | Authority meaning |
|---|---:|---|
| Open/download/preview | No | Observation/use only; proves neither acceptance nor authority. |
| Reject | No | Explicit non-admission decision; deletion is separate. |
| Keep transient | No | Output remains useful but non-canonical within bounded handling. |
| Request admission | Not yet | Creates intent/review path only. Current authority/data-governance/contract gates must still pass. |
| Admit | Yes | Explicit consequential canonical mutation through Governed Execution with owner residual authority in current scope. |

## 7. Real-work consequentiality matrix

P10.01 does not create a universal Kernel `Task` or a permanent global action-class enum. Instead, every concrete requested operation is classified by explicit consequences. Multiple consequence flags may apply; requirements accumulate rather than one class hiding another.

| Requested operation shape | Canonical mutation | External side effect | Organizational/legal commitment | Cross-Organization / scope-retention expansion | Governed Execution | Authority baseline | AI role |
|---|---:|---:|---:|---:|---|---|---|
| Read/search/inspect an allowed asset/request | No | No | No | No | Not required merely for observation | Current Authentication/Authorization and Data Governance/access/purpose constraints | May retrieve/explain/summarize |
| Draft/generate/transform into `TransientOutput` | No | No | No | No | Not required solely because transient output is created, unless another consequential effect is bundled | Current access/data-governance constraints on inputs and output handling | May perform generation; no approval implied |
| Propose metadata/admission/action | No by proposal alone | No | No | No | No canonical/external effect may occur from proposal alone | Proposal carries no Organizational Authority | May propose; human/governed checks decide |
| Admit/supersede/reclassify/disposition a canonical Company asset version | Yes | Usually no | Potentially | Potentially | **Required** | Authorization + Organizational Authority + Data Governance + validation/review + approval as applicable; current owner is residual authority in undelegated scope | May prepare evidence/proposal; cannot final-approve |
| Make a consequential product/company canonical state decision | Yes | Maybe | Maybe | Maybe | **Required** when the requested operation is consequential canonical change | Exact product-owned authority/approval semantics must be declared by effective Product Contract/workflow; technical access is insufficient | May analyze/propose; no independent authority |
| Send/publish/submit/sign/file/write to an external system | Maybe | **Yes** | Often | Maybe | **Required for consequential external effect** | Exact current authority + product contract + external-effect policy/preconditions; uncertain outcomes remain uncertain | May prepare payload/proposal; cannot bypass approval/effect gate |
| Expand Organization scope, cross-Organization transfer, broaden retention/reuse or access | Maybe | Maybe | **Yes/high consequence** | **Yes** | Governed path required if admitted at all | **Default deny** in Phase 10 first slice absent explicit approved authority/policy/Product Contract. Current owner action alone does not silently create a reusable cross-org rule | Cannot self-authorize or infer consent |
| Record consequential approval/commitment | Yes when approval is canonical organizational state | Maybe | **Yes** | Maybe | Governed canonical recording required | Recognized Organizational Authority required; proposed delegation policy is not normative | AI may recommend, never be final approver |

### 7.1 Approval and execution remain separate

An approval record does not itself perform an external effect unless the admitted workflow defines and authorizes that subsequent effect. Conversely, an execution endpoint or technically callable route does not manufacture Organizational Authority.

At command time, server-side checks must re-evaluate current applicable access/context/authority/preconditions rather than trusting a stale UI projection or an earlier AI/tool result.

## 8. Real Action Request source classes

A real request must have an explicit product/company source. Rendering something in Workspace, an LLM statement, chat memory or a heuristic does not make it a real Action Request.

| Source class | Truthful source requirement | Typical requested operation | Consequence shape | Product Contract status for Phase 10 |
|---|---|---|---|---|
| **Company asset review/admission request** | Exact staged/transient Company material version plus provenance/digest and explicit review intent | reject / keep transient / request admission / admit through governed path | canonical asset mutation when admitted | P10.02 must evolve F11 before canonical admission reliance |
| **Tender Operator disposition request** | Explicit Tender-owned product record/result with stable identity, freshness and source-of-truth semantics from the Tender product boundary; Workspace must not infer a task from text alone | owner disposition and, where separately admitted, a product action | may be internal canonical decision and/or later external effect | Candidate source class only until exact Tender Product Contract/action dependency is verified/admitted |
| **Discount Parser controlled-publication request** | Explicit Discount Parser-owned request/result whose source state truthfully requires owner disposition | approve/reject controlled publication or another exact product-owned action | likely external publication effect if approved | Candidate source class only; no execution until effective Product Contract expressly admits the operation and authority path |
| **Other product/company-owned explicit request** | Stable explicit source identity, owner, current state/freshness, source of truth and requested operation | product-specific | determined from actual operation, never guessed from UI wording | Must have an effective Product Contract before governed platform reliance |

### 8.1 Excluded sources

The following are insufficient by themselves:

- chat/model memory;
- AI suggestion or extracted “to-do” text;
- dashboard card existence;
- stale cached projection without current source semantics;
- arbitrary notification/telemetry;
- a developer-created synthetic fixture whose only purpose is to satisfy M10.

Such inputs may become evidence for a human to locate a real source, but cannot manufacture the request, urgency, responsibility, permission or approval.

## 9. First real action journey selection rule

**No P10.07 real action is selected by P10.01 because no new genuine product/company action request is evidenced in the current canonical repository state.**

This is the required truthful result, not a blocker for P10.01.

The first real journey is selected only when a genuine request naturally exists. At selection time the evidence record MUST fix:

- owning product/company scope;
- exact request/source identity and source of truth;
- current freshness/state;
- applicable Product Contract/version;
- requested operation;
- canonical-mutation and external-effect flags;
- Organizational Authority and approval requirement;
- Data Governance constraints;
- current preconditions/idempotency/effect identity where applicable;
- success/blocked/failed/uncertain terminal semantics;
- reconstruction/Event/provenance evidence required.

P10.07 remains waiting rather than fabricating evidence. P10.06 design may proceed after this P10.01 baseline.

## 10. Minimum semantic contract requirements for P10.02

P10.01 does not mandate physical tables, class inheritance, database topology or public API names. It requires the Product Contract to carry enough semantics to prevent hidden coupling and authority ambiguity.

### 10.1 Asset candidate / admission intent

The effective contract must be able to identify, directly or by referenced evidence:

- Organization;
- actor/principal/session context at command time;
- candidate kind and product-owned semantic role;
- exact staged/transient/source identity and version;
- exact digest/content identity where bytes are under Company control;
- source authority mode and authoritative source identity when external;
- provenance/source/version/freshness as applicable;
- rights/usage affirmation or evidence reference;
- purpose + handling/classification decision/reference;
- retention/deletion expectation/reference;
- requested admission operation;
- exact Product Contract version and workflow definition/version;
- expected current/predecessor version and other preconditions.

### 10.2 Admission decision / admitted version

Reconstruction must be able to establish:

- outcome: admitted / rejected / cancelled / blocked / failed;
- exact admitted immutable asset/document version when successful;
- source authority mode;
- effective/current relation where applicable;
- exact authority/approval and Data Governance evidence/references;
- exact Governed Execution run/attempt;
- canonical Event/state-delta/provenance evidence;
- failure/retry/reconciliation result when not successful.

### 10.3 Real Action Request envelope

P10.06/P10.02 must preserve at minimum:

- owning product/company source;
- exact request/source identity;
- source of truth and freshness/current-state reference;
- human-readable context without making Workspace authoritative;
- requested operation and consequence flags;
- applicable Product Contract/version;
- required current authority/approval/data-governance gates;
- exact targets/inputs/preconditions;
- idempotency/effect identity and reconciliation semantics when an external effect exists;
- truthful terminal states including `blocked`, `failed` and `uncertain` rather than success-only reporting.

These are semantic requirements only; implementation shape remains subordinate and reversible.

## 11. Default-deny admission and action gates

A consequential admission/action MUST NOT proceed when any applicable required gate is unresolved. At minimum the implementation/contract must be able to block on:

1. unresolved Organization/tenant scope;
2. missing/stale Authentication/Actor context;
3. missing technical Authorization;
4. missing Organizational Authority;
5. missing Data Governance decision/scope;
6. missing required validation/review;
7. missing required Consequential Approval;
8. missing/invalid exact Product Contract version or operation scope;
9. stale/mismatched candidate/request/version/digest/precondition;
10. unresolved source authority / source-of-truth semantics;
11. missing rights/usage basis where material;
12. unresolved handling/classification/purpose or retention decision/reference where required;
13. prohibited cross-Organization transfer/scope expansion;
14. unavailable Governed Execution path for a consequential canonical/external effect;
15. uncertain prior external effect that requires reconciliation rather than retry.

Failing a gate is a truthful blocked/failed decision, not a reason to silently degrade to direct mutation.

## 12. Event, provenance, replay and uncertainty requirements

For successful consequential admission/action, evidence must be sufficient to reconstruct:

- who/what actor initiated and who/what authority approved as applicable;
- exact Organization and scope;
- exact inputs/targets/version/digest/preconditions;
- Product Contract and workflow definition/version;
- authority/Data Governance/approval decisions or evidence references;
- canonical before/after or state delta where applicable;
- external effect identity/result/reconciliation evidence where applicable;
- resulting canonical Event/provenance links.

Canonical Events remain append-only. Correction creates new truth/evidence rather than silently rewriting history.

Historical replay or reconstruction MUST NOT repeat an external effect without a new current authorization and admitted execution attempt. An uncertain external outcome remains `uncertain` until reconciled; it is not guessed into success or blindly retried.

## 13. Security, privacy and Organization boundary

The first P10.01 slice remains the existing `Local / Persistent Internal / owner-operated` environment, but structural controls still apply.

- Organization scope is explicit even with one currently operated Organization;
- cross-Organization transfer/reuse is not admitted by this slice;
- least privilege/default denial applies to technical access;
- material intake does not grant rights to use, disclose or redistribute content;
- retention/minimization/deletion remain structural concerns and cannot be broadened by AI or convenience;
- derived previews/search indexes/caches remain non-authoritative projections unless separately admitted;
- exposing an asset in Workspace does not imply public visibility or external publication rights;
- no browser/BFF/internal route is promoted to a public/stable API by this design.

## 14. Product/platform boundary disposition

### Platform-owned, domain-neutral responsibility

Subject to P10.02/R33 and later implementation evidence, the reusable platform responsibility may cover only mechanics such as:

- exact subject/source/version/provenance identity;
- Organization/Actor/access/context resolution;
- admission/governed-execution envelope;
- immutable canonical version/history mechanics;
- generic source-authority declaration;
- generic handling/rights/retention evidence references;
- canonical Event/provenance/reconstruction mechanics;
- truthful blocked/failed/uncertain outcome representation.

### Company/product-owned responsibility

The following remain Company/product semantics:

- `brandbook`, `logo`, `Company document template`, source/reference-material roles;
- what a Company document means and when it is acceptable for business use;
- brand/template placeholder rules and generated-document semantics;
- Tender/Discount/other product request schemas and business approval rules;
- urgency/priority/business responsibility;
- external publication/send/sign/file semantics;
- exact owner-facing UX labels and workflows beyond the domain-neutral contract.

No Company taxonomy becomes a Kernel primitive or universal platform catalog because P10.01 uses it.

## 15. Product Contract disposition for P10.02

P10.01 supports the roadmap's expected default:

1. evolve the existing Arvectum Company ↔ Productive Workspace Product Contract lineage from F11 for **Company asset canonical admission + generated-output reviewed promotion**;
2. keep the new version `Provisional` unless a separate lifecycle decision says otherwise;
3. do not overload that contract with materially independent Tender/Discount operational action semantics merely to make P10.07 easier;
4. declare any domain-neutral Actionable Work envelope separately from each product-owned action operation;
5. require exact product-specific Product Contract coverage before a Tender/Discount/other action can execute through Arvectum OS.

The exact version number and final scope are P10.02 decisions; this artifact does not pre-approve them.

## 16. R33 input checklist

P10.01 provides complete inputs for R33. The blocking review must verify at least:

1. no Company material taxonomy became shared Kernel semantics;
2. `TransientOutput`, `StagedNonCanonical`, admission request and canonical admission remain visibly distinct;
3. source authority (`Native` / `External Reference`) is explicit and no competing source of truth is created;
4. `Governed Replica` remains outside the first slice unless separately justified;
5. Authentication/Actor, Authorization, Organizational Authority, Data Governance, validation/review and approval are separate gates;
6. same-human owner operation does not collapse the semantic gates;
7. Proposed Decision Authority Policy is not treated as normative delegation;
8. rights/usage evidence is explicit and file possession is not treated as legal right;
9. retention/classification decisions are structural but P10.01 has not invented legal schedules/taxonomy;
10. every consequential canonical mutation uses Governed Execution;
11. consequential external effects have current authority, idempotency/reconciliation and no-effect-on-replay semantics;
12. generated output remains transient until explicit reviewed promotion;
13. admitted asset/document content does not automatically become validated Knowledge;
14. no AI result becomes authority, approval, scope expansion or Knowledge promotion;
15. F11 `Provisional 0.1.0` remains unexpanded until P10.02 publishes an effective boundary;
16. no browser/BFF/internal implementation detail becomes a public/stable commitment;
17. P10.07 still waits for a genuine request rather than synthetic evidence.

## 17. Functional cross-review

Functional cross-review is implementation/design critique only; it is **not** formal approval, RFC/ADR acceptance, Product Contract transition, capability promotion or operational-readiness approval.

### Iteration 1 — architecture / Kernel boundary

Material objection: the initial matrix could be misread as introducing a universal Organizational Asset primitive or permanent global action-class enum.

Revision:

- asset is explicitly a designation over RFC-0002/RFC-0008 semantics;
- source authority is an orthogonal semantic axis;
- real-work classification uses explicit consequence flags instead of a new Kernel Task/action primitive;
- no physical schema/API/class hierarchy is prescribed.

Disposition: resolved.

### Iteration 2 — security / authority

Material objection: owner-operated simplicity could collapse Authentication, Authorization, Organizational Authority, Data Governance and approval into one UI confirmation.

Revision:

- gates are separately enumerated;
- command-time server-side revalidation is required;
- the same owner may satisfy multiple gates only when each applicable gate is independently valid/evidenced;
- the Proposed Decision Authority Policy is explicitly non-normative;
- no AI/UI/technical access can manufacture authority.

Disposition: resolved.

### Iteration 3 — data governance / rights / retention

Material objection: P10.01 could accidentally invent a company-wide classification taxonomy, legal rights conclusion or retention schedule without approved policy evidence.

Revision:

- first-slice handling is framed as product-level purpose/expectation;
- rights are explicit affirmation/evidence requirements, never inferred from possession;
- exact retention/classification policy values are references/decisions where available and are not fabricated;
- External Reference is default for externally authoritative source material;
- cross-Organization transfer/retention expansion defaults to denied in the slice.

Disposition: resolved.

### Iteration 4 — Product Contract / AI / real-work evidence

Material objection: a completed P10.01 matrix could be mistaken for permission to implement canonical admission or execute Tender/Discount actions under F11.

Revision:

- F11 `Provisional 0.1.0` remains explicitly insufficient for canonical admission/action execution;
- P10.02 remains the next mandatory Product Contract step and R33 remains blocking for P10.03;
- Tender/Discount requests are candidate source classes only;
- first P10.07 journey remains unselected until a genuine request exists;
- AI remains proposal-only and cannot provide approval/authority.

Disposition: resolved.

**Cross-review result: 4 iterations completed; no material objections remain for P10.01 design closure and handoff to P10.02.**

## 18. P10.01 exit criteria

| Exit criterion | Result |
|---|---:|
| First-slice asset classes explicit | PASS |
| Admission semantics explicit | PASS |
| Receipt/generation distinct from canonical admission | PASS |
| Generated-output review/promotion lifecycle explicit | PASS |
| Real Action Request source classes explicit without Kernel Task primitive | PASS |
| Authority / Data Governance / validation / approval separated | PASS |
| Consequentiality matrix explicit | PASS |
| Source-of-truth / source-authority modes preserved | PASS |
| Rights / handling / retention expectations explicit without invented policy | PASS |
| No premature Product Contract expansion | PASS |
| No synthetic P10.07 action selected | PASS |
| R33 inputs complete | PASS |

**P10.01 = Complete / PASS in design/evidence scope.**

This does not mean canonical asset admission exists. The next canonical action is P10.02, which must publish the minimum-sufficient effective Product Contract boundary before P10.03 implementation relies on governed Company-asset admission.
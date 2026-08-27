# DECISION-2026-08-27-P10-02-PROVISIONAL-APPROVAL

Status: `Approved`
Date: `2026-08-27`
Owner / Decision Authority: `ООО «Арвектум»`
Task classification: `product_contract` + `governance`
Authority: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0`; ADR-0001 `Accepted`
Decision target: `P10.02 — Arvectum Company ↔ Productive Workspace Product Contract`
Approved lifecycle transition: `Draft → Provisional`
Approved version: `0.2.0`

## 1. Independent owner decision

The owner explicitly approved the exact reviewed P10.02 Product Contract with the instruction:

> `утверждаю P10.02 Product Contract v0.2.0 в Provisional scope; exact Draft blob a92c1d1aac54d565d3d32ce746925620c9d1fd12`

This decision existed in project conversation before the Provisional publication commit and is recorded here as canonical approval evidence.

The owner also stated that the approval was given on trust in the prepared analysis rather than after personally inspecting the full contract text, and objected that the decision had not been presented clearly enough in human-readable form. This provenance note does not alter the explicit approval above, but it is material process feedback: future owner approval gates should present a concise human-readable decision brief before requesting an exact governance statement.

## 2. Exact approved proposal identity

Approved Draft:

`docs/contracts/P10-02-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-DRAFT-v0.2.0.md`

Exact approved Draft content identity:

- blob SHA: `a92c1d1aac54d565d3d32ce746925620c9d1fd12`;
- Draft version: `0.2.0`;
- PR: `#24`;
- Product Contract subject: `product-contract-subject/p9-11-f11-arvectum-company-workspace@organization/arvectum-company`.

The approval applies only to that exact bounded content. A material boundary change requires a new immutable Product Contract version and new applicable approval evidence.

## 3. Human-readable approved scope

The owner approves publication of `Provisional 0.2.0` for bounded internal governed reliance in the current `Local / Persistent Internal / owner-operated` scope.

In practical terms, the approved contract boundary permits Productive Workspace to support:

1. governed canonical admission of one exact reviewed staged Company-held material version through `company.asset.admit-staged-version`;
2. governed admission of an external Company-relevant reference while preserving `External Reference` authority through `company.asset.admit-external-reference`;
3. the contract boundary for later reviewed promotion of one exact generated `TransientOutput` through `company.generated-output.promote-reviewed`, while real reliance on that promotion operation remains unavailable until P10.05 implements and reviews it;
4. read-only/non-canonical projection of an explicit current Company/product request through `workspace.actionable-work.project-request`;
5. a no-side-effect Workspace entry/routing envelope through `workspace.product-operation.enter`, where any actual downstream product effect still requires the owning product's exact effective Product Contract and product-owned governed workflow/operation.

The approved first-slice Company asset classes are bounded to brandbook, logo/brand assets, Company templates, Company-held source/reference materials, governed external references and an exact reviewed generated document only after the separate promotion path is admitted.

## 4. Authority and safety meaning

This approval does not collapse or bypass Authentication, Authorization, Organizational Authority, Data Governance, validation or Consequential Approval. Current gates must be evaluated independently at the consequential operation boundary. Residual Organizational Authority remains with the owner unless a separately approved exact delegation applies.

Generated output remains `TransientOutput` by default. Opening, downloading, editing, commenting on, repeatedly using or trusting a generated draft does not make it canonical.

External sources remain authoritative within their declared `External Reference` scope; local caching, copying, retrieval or generated representation does not silently convert them to `Native` authority.

## 5. What this approval does not approve or prove

This decision does not approve or prove:

- P10.03 implementation;
- R33 PASS;
- a real Company asset admission already having occurred;
- P10.05 generated-output promotion implementation;
- any Tender Agent, Discount Parser or other product consequential side effect;
- Product Contract `Stable` status;
- Platform Capability `Active` status;
- customer/external Production readiness;
- public/stable API, SDK, browser or BFF compatibility;
- remote execution authority;
- automatic external sending, signing, filing or publication;
- electronic-signature/legal-validity semantics;
- automatic Policy, Standard, Decision or validated Knowledge promotion;
- cross-Organization sharing/reuse;
- SLA, support, certification or broader conformance claims;
- legal ownership or expanded reuse rights merely through asset designation.

## 6. Required publication sequence

This approval record must exist in repository history before the Provisional publication commit.

After this independent approval commit exists, the branch may:

1. publish lifecycle-current `Provisional 0.2.0` by immutable reference to the exact approved Draft blob;
2. synchronize P10.02 review/status and Phase 10/master roadmaps;
3. perform read-after-write verification and applicable checks;
4. merge PR #24 only with approval-before-publication history preserved;
5. verify resulting `main` state;
6. advance the critical path to `R33 — Asset / Product Contract / Authority Boundary Review` while keeping P10.03 blocked until R33 passes.

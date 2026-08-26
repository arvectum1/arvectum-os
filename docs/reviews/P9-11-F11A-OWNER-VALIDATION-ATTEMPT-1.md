# P9.11-F11A — Real owner validation attempt 1

Status: `FAIL / bounded remediation in progress`
Date: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `product_specific + product_contract + platform`
Product Contract: `P9.11-F11 Provisional 0.1.0`
Observed live Workspace: `p9.11.9` / app contract `11`

## 1. Real owner journey evidence

The owner performed the first real F11A Company-material/template journey on the governed selected-Mac Workspace.

Observed positive evidence:

- a real Company brandbook was uploaded successfully into the staged material store;
- the owner then uploaded the real test DOCX template prepared for the F11A exact-version template journey;
- normal Company Materials navigation remained available.

The owner then reported two material frictions:

1. material/document type must be entered manually and should instead be a fixed list containing at least `Шаблон документа` plus an explicit `Другое` option that reveals a custom category field;
2. after filling the document-generation fields, the journey ended at the raw response:

```json
{"code":"RELEASE_MISMATCH","reload_required":true}
```

Result: **F11A owner validation attempt 1 = FAIL**. Upload/staging works, but the real standard-document journey is not yet complete and usable.

## 2. Finding F11A-01 — free-text material role is unnecessary owner friction

The current F11A UI exposes `semantic_role` as a required free-text field. This is technically flexible but unnecessarily asks the owner to remember internal vocabulary such as `document-template`, `brandbook`, `logo` or `source`.

Bounded remediation:

- replace the ordinary free-text control with a product-owned fixed first-slice material taxonomy:
  - `Шаблон документа` → `document-template`;
  - `Брендбук` → `brandbook`;
  - `Логотип` → `logo`;
  - `Исходный материал` → `source`;
  - `Другое` → explicit custom text field;
- continue storing the final resolved semantic role as existing F11A metadata;
- do not turn this product-local taxonomy into a shared Platform Capability or RFC-level document taxonomy.

This remains inside RFC-0008 product-owned document/template taxonomy boundaries and the existing F11 Product Contract.

## 3. Finding F11A-02 — generated-output download bypasses the Workspace release guard

Repository inspection establishes a deterministic client defect:

- ordinary F11A JSON API operations use `f11Api.ts`, which adds `X-Arvectum-Workspace-Release` to `/api/app/v1/**` requests;
- the generated-output UI instead rendered `download_href` as a plain browser `<a href>`;
- the browser navigation therefore omitted the mandatory release header;
- the Workspace trust-boundary middleware correctly rejects any `/api/app/v1/**` request whose supplied release does not equal the active release and returns `409 {"code":"RELEASE_MISMATCH","reload_required":true}`.

The release guard itself is correct and MUST NOT be weakened to make downloads work.

Bounded remediation:

- replace the unguarded API anchor with a same-origin release-bound `fetch` download;
- preserve current session/access revalidation on the BFF download route;
- keep arbitrary/external download paths rejected client-side;
- create a temporary browser object URL only after the protected response succeeds;
- keep generated output `TransientOutput`, with exact source-version provenance and no canonical admission.

The owner's report alone does not independently establish whether the generation POST completed before the browser reached the raw mismatch response. Therefore this record does not claim that a generated output definitely existed or definitely did not exist. The acceptance journey is treated as failed until generation plus protected download/open are rechecked end to end.

## 4. Governance / authority check

No Product Contract expansion is required.

- Product Contract remains `Provisional 0.1.0`.
- Brandbook/template receipt remains `StagedNonCanonical`.
- Generated DOCX remains `TransientOutput` by default.
- Upload or generation grants neither Authorization nor Organizational Authority.
- No validated Knowledge is created by receipt/generation.
- Canonical asset/document admission remains unavailable in this F11A slice.
- The server release guard remains fail-closed.
- Product-specific material taxonomy remains product-owned.

## 5. Remediation candidate

Workspace `p9.11.10` candidate scope:

1. fixed owner-facing material type list plus explicit `Другое` custom field;
2. release-bound generated-DOCX download helper;
3. no plain `/api/app/v1/.../download` anchor in the F11A UI;
4. regression coverage for fixed taxonomy, protected download action and exact release header;
5. app API contract remains `11`;
6. no change to F11 lifecycle/authority/canonical-admission semantics.

## 6. Recheck required

After reviewed CI, reproducible production assets, merge and governed deployment, the owner must repeat the same real journey:

1. return to Company Materials through normal navigation;
2. confirm the material type is selected from the fixed list and `Другое` exposes a custom field;
3. use the already staged exact DOCX template version or upload the intended real template version;
4. generate a real project-bound DOCX;
5. download it through the protected UI action;
6. open the DOCX and inspect actual placeholder replacement / usability;
7. report any remaining material friction.

No F11A owner PASS may be claimed before that recheck succeeds.

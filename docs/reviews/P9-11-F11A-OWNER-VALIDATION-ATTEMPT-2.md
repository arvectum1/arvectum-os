# P9.11-F11A — Real owner validation attempt 2

Status: `PASS / bounded real template-to-document journey`
Date: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `product_specific + product_contract + platform`
Product Contract: `P9.11-F11 Provisional 0.1.0`
Observed live Workspace: `p9.11.10` / app contract `11`
Release-bearing canonical source: `470878b8778fbac009d1ae52092879cf50d8f3f1`
Predecessor: [`P9-11-F11A-OWNER-VALIDATION-ATTEMPT-1.md`](P9-11-F11A-OWNER-VALIDATION-ATTEMPT-1.md) — `FAIL`, remediated by PR #19.

## 1. Governed deployment / technical readiness

Selected-Mac governed deployment of p9.11.10 reportedly passed:

- P7.06 transaction `129845fa731fee12f2f9d2ada6894c42bc366b582835f8c299533d78565ad877`;
- backup `/Users/master/Library/Application Support/ArvectumOS/persistent-internal/backups/p7-03-backup-20260826T214943Z-ab680eae2632ec3a.tar.gz`;
- backup SHA-256 `ff9acf7e497bf0e27b7dcbfc7baa1abdee196f9c7e83c3feffc83476d26f1a5a`;
- P7.02/P7.05 healthy;
- `CURRENT_EXACT` / `MANAGED_SPAWN_PROOF`;
- one loopback listener on `127.0.0.1:8769`;
- exact assets and Desktop launcher PASS.

Technical smoke also established fixed material-type UX, retained staged brandbook/template, release-bound protected download, `TransientOutput`, exact source pinning and successful placeholder replacement.

## 2. Real owner recheck

The owner then repeated the real standard-document journey and reported:

> `работает. сказался, открылся, форматирование как и должно быть, тексты подтянулись. единственное, ворд на макбук ругался, что файл сомнительного происхождения и можно ли ему доверять. но после "ОК" все открыл`

Interpreted only to the extent supported by the owner report:

- generation worked;
- the DOCX downloaded;
- the DOCX opened in Word on the MacBook;
- expected formatting was preserved;
- supplied text values were inserted correctly;
- Word displayed a trust/provenance warning before opening, but the owner accepted the prompt and the document opened normally.

## 3. Result

**F11A owner validation attempt 2 = PASS in the bounded real template-to-document scope.**

The Word trust prompt is recorded as `minor / non-blocking owner friction`. Current evidence does not establish that the prompt reflects malformed OOXML, a Workspace integrity failure, or a security-guard defect. No attempt is made to suppress or bypass host-application security warnings merely to remove friction.

A future bounded investigation may determine whether ordinary downloaded-file provenance/quarantine behavior or another host-specific cause explains the prompt. That investigation is not required for F11A bounded owner usefulness because the generated document was usable after the explicit Word confirmation.

## 4. Governance / authority boundary

- staged brandbook/template remain `StagedNonCanonical`;
- generated DOCX remains `TransientOutput` by default;
- exact template version/provenance remains pinned;
- upload/generation grant neither Authorization nor Organizational Authority;
- generated content does not become validated Knowledge;
- canonical asset/document admission remains unavailable in this F11A slice;
- release guard remains enabled and was not weakened by the download repair;
- Product Contract remains `Provisional 0.1.0`.

## 5. Disposition

- F11A — bounded owner PASS;
- F11A-01 fixed material-type UX — resolved/rechecked;
- F11A-02 release-bound DOCX download — resolved/rechecked;
- Word trust prompt — minor/non-blocking observation;
- no Stable Product Contract, Active Platform Capability, canonical admission or operational-readiness promotion is implied.

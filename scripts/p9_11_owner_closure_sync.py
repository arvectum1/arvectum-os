from pathlib import Path


def replace_exact(path: str, old: str, new: str, count: int = 1) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"{path}: expected {count} occurrence(s), found {actual}: {old[:120]!r}")
    p.write_text(text.replace(old, new, count), encoding="utf-8")


def append_once(path: str, marker: str, block: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if marker in text:
        raise SystemExit(f"{path}: closure marker already present")
    p.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


Path("docs/reviews/P9-11-F11B-OWNER-VALIDATION-RECHECK-3.md").write_text(r'''# P9.11-F11B — Real owner validation recheck 3

Status: `PASS / bounded owner usefulness scope`
Date: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `platform + product_contract + product_specific`
Product Contract: `P9.11-F11 Provisional 0.1.0`
Observed live Workspace: `p9.11.9` / app contract `11`
Predecessor: [`P9-11-F11-OWNER-VALIDATION-ATTEMPT-2.md`](P9-11-F11-OWNER-VALIDATION-ATTEMPT-2.md) — `FAIL`, remediated by F11D-03.

## 1. Real owner evidence

After p9.11.9 F11D-03 remediation and repeated navigate-away/return stability checks, the owner reported:

> `пока не нашел особо к чему прикопаться, кроме верстки (но это не критично, еще поменяется 100 раз).`

This follows the earlier real failure where portfolio data disappeared after ordinary navigation and the subsequent cache-backed repair that retained source/cached cards across revisits.

## 2. Result

**F11B owner recheck #3 = PASS in the bounded owner-usefulness scope.**

The owner can use the project portfolio as an acceptable daily read-only orientation surface. The remaining layout concern is explicitly non-critical and is treated as `minor` visual friction rather than a material closure blocker.

This PASS does not assert perfect/final UI design, a public/stable browser contract, remote execution, roadmap write capability, or canonical authority for the dashboard projection.

## 3. Authority / provenance boundary

- canonical roadmap/status authority remains `External Reference`;
- the local last-known-good portfolio cache remains non-canonical and rebuildable;
- source SHA/content hash/fetched-at/freshness remain provenance evidence, not Organizational Authority;
- `reconciliation-required` remains truthful for unresolved sources;
- no chat/model memory substitutes for missing canonical source evidence;
- no Product Contract lifecycle promotion follows from this owner PASS.

## 4. Disposition

- F11B — bounded owner PASS;
- layout polish — minor/non-blocking backlog only;
- Product Contract — `Provisional 0.1.0` unchanged;
- P9.11 closure may consider F11B owner-usefulness criterion satisfied.
''', encoding="utf-8")

Path("docs/reviews/P9-11-F11A-OWNER-VALIDATION-ATTEMPT-2.md").write_text(r'''# P9.11-F11A — Real owner validation attempt 2

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
''', encoding="utf-8")

# F11 aggregate review.
replace_exact("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md",
              "Status: `Deployed / technical smoke PASS / owner validation pending`",
              "Status: `Owner validation PASS in bounded F11A/F11B scope / Product Contract remains Provisional`")
replace_exact("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md", "Version: `0.5.0`", "Version: `0.6.0`")
replace_exact("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md", "Updated: `2026-08-26`", "Updated: `2026-08-27`")
replace_exact("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md", "Workspace release: `p9.11.7`", "Workspace release: `p9.11.10`")
replace_exact("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md", "Merged source: `ff73db4e0ee9917572654287d4dc74b4a0dea1ff`", "Merged source: `470878b8778fbac009d1ae52092879cf50d8f3f1`")
replace_exact("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md",
              "Owner PASS остаётся pending. Он требует на live Workspace минимум:",
              "Этот критерий был pending до p9.11.10 owner recheck; теперь он закрыт bounded owner PASS. Исторически требовалось минимум:")
replace_exact("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md",
              "Owner PASS остаётся pending. Он требует live dashboard, который:",
              "Этот критерий был pending до owner recheck #3; теперь он закрыт bounded owner PASS. Исторически требовался live dashboard, который:")
replace_exact("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md",
              "- F11A — **deployed; technical smoke PASS; owner validation pending; canonical admission unavailable**;\n- F11B — **deployed; technical smoke PASS; owner validation pending**;\n- F09 — ordinary running-Workspace stop/update/restart path now has natural live PASS evidence from the F11 deployment, within its existing bounded scope;\n- Workspace release — `p9.11.7`, app contract `11`;\n- deployed selected-Mac runtime/source — `ff73db4e0ee9917572654287d4dc74b4a0dea1ff` according to owner-supplied local evidence;\n- P9.11 — `Current`;\n- R32 — `Locked`;\n- следующий canonical action — real owner F11A and F11B journeys; any material friction becomes the next P9.11 finding.",
              "- F11A — **bounded owner PASS on live p9.11.10; canonical admission unavailable**;\n- F11B — **bounded owner PASS after p9.11.9 cache-backed stability repair**;\n- F09 — ordinary running-Workspace stop/update/restart path retains natural live PASS evidence from the F11 deployment, within its existing bounded scope;\n- Workspace release — `p9.11.10`, app contract `11`;\n- deployed selected-Mac runtime/source — `470878b8778fbac009d1ae52092879cf50d8f3f1` according to owner-supplied local evidence;\n- Product Contract — `Provisional 0.1.0` unchanged;\n- F11 owner-usefulness acceptance — **PASS in bounded F11A/F11B scope**;\n- P9.11 closure criteria — satisfied with only minor/non-blocking visual and Word trust-prompt friction remaining;\n- next canonical action — `R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate`.")
append_once("docs/reviews/P9-11-F11-company-materials-and-project-portfolio.md", "## 9. Post-remediation owner validation closure", r'''
## 9. Post-remediation owner validation closure

The pending wording in earlier sections is superseded by real owner evidence recorded after the p9.11.9 and p9.11.10 repairs:

- [`P9-11-F11B-OWNER-VALIDATION-RECHECK-3.md`](P9-11-F11B-OWNER-VALIDATION-RECHECK-3.md) — `PASS / bounded owner usefulness scope`;
- [`P9-11-F11A-OWNER-VALIDATION-ATTEMPT-2.md`](P9-11-F11A-OWNER-VALIDATION-ATTEMPT-2.md) — `PASS / bounded real template-to-document journey`.

F11B owner feedback accepts the portfolio as usable with only non-critical layout polish remaining. F11A owner feedback confirms real generation, download, open, formatting preservation and text substitution on p9.11.10. The Word trust/provenance prompt is retained as minor non-blocking friction and is not bypassed or misrepresented as a Workspace security failure without evidence.

F11 therefore achieves **bounded owner-usefulness PASS** while the Product Contract remains `Provisional 0.1.0`. This does not establish Stable Product Contract status, Active Platform Capability, canonical asset admission, customer Production/readiness, SLA/support or public/stable API/browser compatibility.
''')

# P9.11 closure review.
replace_exact("docs/reviews/P9-11-real-daily-use-dogfooding-friction-backlog-closure.md",
              "Status: `Implementation Ready / Owner-session evidence pending`",
              "Status: `Complete / PASS — real owner sessions and material friction disposition evidenced`")
replace_exact("docs/reviews/P9-11-real-daily-use-dogfooding-friction-backlog-closure.md",
              "Current canonical action: `P9.11 — Real daily-use dogfooding + friction/backlog closure`",
              "Current canonical action: `R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate`")
replace_exact("docs/reviews/P9-11-real-daily-use-dogfooding-friction-backlog-closure.md",
              "## Why P9.11 is not Complete / PASS yet",
              "## Historical implementation-readiness state: why P9.11 was not Complete / PASS yet")
replace_exact("docs/reviews/P9-11-real-daily-use-dogfooding-friction-backlog-closure.md",
              "## P9.11 closure conditions still pending",
              "## Historical closure conditions that remained pending at implementation-readiness time")
replace_exact("docs/reviews/P9-11-real-daily-use-dogfooding-friction-backlog-closure.md",
              "Until those facts are evidenced, P9.11 remains the canonical current action.",
              "Those conditions were intentionally not asserted at implementation-readiness time. They are superseded by the real-owner closure evidence below.")
append_once("docs/reviews/P9-11-real-daily-use-dogfooding-friction-backlog-closure.md", "## P9.11 closure evidence — 2026-08-27", r'''
## P9.11 closure evidence — 2026-08-27

P9.11 now has sufficient real owner evidence for bounded closure:

1. multiple real owner sessions occurred primarily through the live Productive Workspace rather than synthetic scenarios;
2. material usability findings F07–F11 were repaired and rechecked on ordinary owner journeys;
3. F11B project-portfolio stability/usefulness reached bounded owner PASS after the p9.11.9 cache-backed repair;
4. F11A real Company-material/template → generated DOCX → protected download → Word-open journey reached bounded owner PASS on p9.11.10;
5. remaining owner observations are minor/non-closure-blocking: future layout polish and the Word downloaded-file trust/provenance prompt;
6. no unresolved blocker/material finding remains in the evidenced P9.11 closure path;
7. the deferred F08 real task-detail → governed-action journey remains eligible for natural recheck when a genuine actionable task exists, without manufacturing a synthetic task and without reopening the resolved false-task defect;
8. security, authority, provenance and Product Contract boundaries remain fail-closed and unchanged.

Therefore **P9.11 = Complete / PASS** in its exact `Local / Persistent Internal / owner-operated` scope. The next canonical action is **R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate**.

This closure does not establish M9/P9.12 closure, customer Production/readiness, Stable Product Contracts, Active Platform Capabilities, public/stable APIs/browser support, SLA/support or any Organizational Authority delegation.
''')

# Master roadmap.
replace_exact("docs/roadmap/ROADMAP.md", "Version: `2.95.25`", "Version: `2.95.26`")
replace_exact("docs/roadmap/ROADMAP.md", "Updated: `2026-08-26`", "Updated: `2026-08-27`")
replace_exact("docs/roadmap/ROADMAP.md",
              "Version `2.95.25` records F11 owner validation attempt #2 as `FAIL`: the portfolio was initially visible, but after ordinary navigation return every project card became unavailable. F11D-03 root cause was a live GitHub fetch on every page revisit with no last-known-good read-model cache. PR #17 merged the bounded repair at `ef46d23ffe0c724a86f7f49afd4c71345d42265c`, advancing Workspace to `p9.11.9` / app contract `11`. Exact reviewed head `52ab60a332000fff70dc9c9d8d8dc43dccc9b4c5` passed Productive Workspace CI `33005196234` and Reference Python CI `33005196245`. Selected-Mac P7.06 transaction `1bedb028b38c239f2bb2f3632277444d4e56e9a442efd996180e3b300370054e` passed with exact cache-backed navigation smoke. F11B is remediation deployed / owner recheck #3 pending; F11A owner validation remains pending. Neither is owner PASS. Product Contract remains `Provisional 0.1.0`; canonical asset admission remains unavailable; P9.11 remains Current; R32 remains Locked.",
              "Version `2.95.26` records bounded real-owner closure of F11 and P9.11. F11B owner recheck #3 accepted the stable cache-backed project portfolio as usable, with only non-critical layout polish remaining. F11A owner attempt #2 on live `p9.11.10` completed the real staged material/template → generated `TransientOutput` → protected download → Word-open journey with expected formatting and substituted text. The Word trust/provenance prompt is retained as minor non-blocking friction and is not bypassed. F11A/F11B therefore have bounded owner PASS; Product Contract remains `Provisional 0.1.0`, canonical asset admission remains unavailable, and no capability/lifecycle/authority promotion is implied. Real P9.11 sessions and material-friction disposition are now sufficient for `P9.11 = Complete / PASS`; `R32` becomes the current canonical action.")
replace_exact("docs/roadmap/ROADMAP.md",
              "| **P9.11** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current — F10A bounded owner PASS; F11 attempt #2 FAIL; p9.11.9 F11D-03 remediation deployed / F11B owner recheck #3 pending** |",
              "| P9.11 | Real daily-use dogfooding + friction/backlog closure | 🟩 Complete / PASS — F11A/F11B bounded owner PASS; material friction disposition complete |")
replace_exact("docs/roadmap/ROADMAP.md",
              "| R32 | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ Locked |",
              "| **R32** | **M9 Productive Workspace Hardening + Milestone Code Health Gate** | **🟨 Current** |")
replace_exact("docs/roadmap/ROADMAP.md",
              "- **F11 disposition:** F11B remediation deployed / **OWNER RECHECK #3 PENDING**; F11A owner validation pending; no owner PASS;",
              "- **F11 owner validation closure:** F11B owner recheck #3 = bounded PASS with only minor layout polish; F11A owner attempt #2 on p9.11.10 = bounded PASS for real template → generated DOCX → protected download → Word-open journey; Word trust/provenance prompt retained as minor non-blocking friction; Product Contract remains Provisional 0.1.0 and canonical asset admission unavailable;")
replace_exact("docs/roadmap/ROADMAP.md",
              "`P9.11` remains Current and `R32` remains Locked. The next canonical action is real owner recheck #3 of F11B portfolio navigation stability and F11 usefulness on live p9.11.9, alongside the still-pending F11A owner journey. No synthetic owner-session evidence or canonical asset-admission claim is admitted. The first naturally occurring genuine actionable task still rechecks the deferred F08 task-detail → governed-action journey when it appears.",
              "`P9.11` is Complete / PASS and `R32` is Current. F11A/F11B real owner journeys have bounded owner PASS with no unresolved material closure blocker; only minor layout polish and a Word trust/provenance prompt remain. No synthetic owner-session evidence or canonical asset-admission claim is admitted. The first naturally occurring genuine actionable task still rechecks the deferred F08 task-detail → governed-action journey when it appears, without reopening P9.11 unless new material friction is found.")
replace_exact("docs/roadmap/ROADMAP.md",
              "real owner F11A materials/template/transient-document journey + F11B project-portfolio journey\n        ↓\ndisposition any material owner friction; retain deferred natural F08 task journey\n        ↓\nR32\n        ↓\nP9.12 / M9",
              "R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate\n        ↓\nP9.12 / M9 closure")

# Phase 9 roadmap.
replace_exact("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md", "Version: `1.13.22`", "Version: `1.13.23`")
replace_exact("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md", "Updated: `2026-08-26`", "Updated: `2026-08-27`")
replace_exact("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md",
              "Current disposition: F10A has bounded owner PASS for guide understandability. F11 owner validation attempt #2 is `FAIL`: project cards were initially visible, but ordinary navigation return made them all unavailable. F11D-03 root cause was a live GitHub fetch on every revisit without a last-known-good read-model cache. PR #17 merged bounded remediation at `ef46d23ffe0c724a86f7f49afd4c71345d42265c`; Workspace `p9.11.9` / app contract `11` was governed-deployed by P7.06 transaction `1bedb028b38c239f2bb2f3632277444d4e56e9a442efd996180e3b300370054e`. P7.02/P7.05 are healthy, Workspace is `CURRENT_EXACT` / `MANAGED_SPAWN_PROOF`, loopback-only exact assets and launcher checks pass. First source load wrote non-canonical cache; three ordinary revisits were `cached-within-window`, retained identical exact provenance and showed no unavailable cards; explicit refresh succeeded. Reviewed head `52ab60a332000fff70dc9c9d8d8dc43dccc9b4c5` passed Productive Workspace CI `33005196234` and Reference Python CI `33005196245`. F11B is remediation deployed / owner recheck #3 pending; F11A owner validation remains pending; neither is owner PASS. Product Contract remains `Provisional 0.1.0`, canonical asset admission unavailable, P9.11 Current and R32 Locked.",
              "Current disposition: F11A and F11B now have bounded real-owner PASS. F11B recheck #3 accepted the p9.11.9 cache-backed portfolio as usable; remaining layout polish is minor/non-blocking. F11A attempt #2 on governed-deployed `p9.11.10` completed the real staged template → generated `TransientOutput` → release-bound download → Word-open journey with expected formatting and substituted text. A Word trust/provenance prompt remains minor/non-blocking and is not bypassed. Product Contract remains `Provisional 0.1.0`; canonical asset admission remains unavailable. P9.11 real-session/material-friction closure criteria are satisfied, so P9.11 is Complete / PASS and R32 is Current.")
replace_exact("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md",
              "| **P9.11** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current — F10A bounded owner PASS; F11 attempt #2 FAIL; p9.11.9 F11D-03 remediation deployed / F11B owner recheck #3 pending** | real owner sessions + material friction closure |",
              "| P9.11 | Real daily-use dogfooding + friction/backlog closure | 🟩 Complete / PASS — F11A/F11B bounded owner PASS | real owner sessions + material friction closure |")
replace_exact("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md",
              "| R32 | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ Locked | pre-closure hardening PASS |",
              "| **R32** | **M9 Productive Workspace Hardening + Milestone Code Health Gate** | **🟨 Current** | pre-closure hardening PASS |")
replace_exact("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md",
              "Repository and technical smoke evidence are sufficient for deployed technical readiness, not owner usefulness PASS. F11B remains remediation deployed / **OWNER RECHECK #3 PENDING**; F11A owner validation remains pending. Next evidence must come from real owner journeys.",
              "Subsequent real owner evidence closes both journeys in bounded scope. F11B owner recheck #3 accepts the stable project portfolio as usable with only minor layout polish. F11A owner attempt #2 on p9.11.10 confirms real generation, release-bound download, Word open, expected formatting and text replacement; the Word trust/provenance prompt is minor/non-blocking. F11A/F11B therefore have bounded owner PASS while Product Contract remains Provisional 0.1.0 and canonical asset admission remains unavailable.")
replace_exact("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md",
              "real owner F11A materials/template/transient-document journey + F11B project-portfolio journey\n        ↓\ndisposition material friction; retain deferred natural F08 task journey\n        ↓\nR32 hardening + M9 Code Health Gate\n        ↓\nP9.12 / M9 closure",
              "R32 hardening + M9 Code Health Gate\n        ↓\nP9.12 / M9 closure")
replace_exact("docs/roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md",
              "> **P9.11 — perform real owner recheck #3 of F11B portfolio navigation stability and F11 usefulness on live p9.11.9. Attempt #2 remains FAIL and deployed remediation is not owner PASS. F11A owner validation remains pending and must retain staged provenance, `StagedNonCanonical`, `TransientOutput`, and unavailable canonical admission. F11B must be inspected across ordinary navigation and truthfully retain source-backed/cached/reconciliation state, current/next work, execution location and exact provenance. Any material friction becomes the next P9.11 finding. P9.11 remains Current and R32 remains Locked.**\n\nR32 remains locked until the F11 real owner journeys and any resulting material friction are dispositioned together with the existing P9.11 closure criteria.",
              "> **R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate. P9.11 is Complete / PASS from real owner sessions and material-friction disposition. Preserve all existing security, authority, provenance, Product Contract and no-canonical-admission boundaries while performing the pre-closure hardening/code-health review.**\n\nThe deferred F08 real task-detail → governed-action journey remains a natural future recheck when a genuine actionable task appears; it is not a blocker for R32 and must not be satisfied with synthetic owner work.")

# The helper and workflow are temporary branch-only materialization tools.
Path(".github/workflows/p9-11-owner-closure-sync.yml").unlink(missing_ok=True)
Path("scripts/p9_11_owner_closure_sync.py").unlink(missing_ok=True)

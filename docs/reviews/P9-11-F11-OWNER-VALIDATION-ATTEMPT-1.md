# P9.11-F11 — Real owner validation attempt 1

Status: `FAIL / remediation deployed / owner recheck pending`
Date: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `platform + product_contract + product_specific`
Product Contract: `P9.11-F11 Provisional 0.1.0`
Observed live Workspace: `p9.11.7` / app contract `11`; remediation deployed to `p9.11.8` / app contract `11`
Related review: [`P9-11-F11-company-materials-and-project-portfolio.md`](P9-11-F11-company-materials-and-project-portfolio.md)

## 1. Evidence classification

This record captures real owner-use evidence from the live selected-Mac Workspace after the successful F11 governed deployment. It is not synthetic acceptance evidence and it does not grant Authorization, Organizational Authority, canonical admission or Product Contract promotion.

The owner supplied a live screenshot of `/projects` and the following feedback:

> `по проектам - вообще не наглядно. нет единой структуры, подтягивается не все, не юзабельно вообще.`

> `по документам - на старте открылась эта страница (добавить документ, создать документ), я ушел в навигацию, покликал по меню, а теперь не могу вернуться на страницу с документами. ссылки на нее в меню нигде нет`

Result: **F11 owner validation attempt 1 = FAIL**.

## 2. Material finding F11D-01 — project portfolio is not owner-usable

Observed live behavior:

- project cards are arranged as multiple narrow vertical columns;
- different projects expose materially different amounts and shapes of information;
- raw roadmap text and repository/SHA/provenance details dominate the visible card;
- the page does not present one stable owner-facing structure for comparison;
- normalized `done`, `branches` and `execution_targets` already available in the F11 projection are not rendered;
- some registered sources are incomplete: Tender Agent is left in reconciliation despite a repository-owned `STATUS.md`; Creative Test Agent points at top-level `ROADMAP.md`, which is only a pointer to the actual canonical current roadmap;
- the resulting page does not answer the intended owner questions reliably enough: where the project is now, what is complete, what can be done next, which branches/blockers exist and where the action belongs.

This is a material F11B usability failure. Technical source/provenance correctness alone is insufficient for F11B owner PASS.

## 3. Material finding F11D-02 — Company Materials is not discoverable in normal navigation

Observed live behavior:

- `/company-materials` opens and the upload/generation surface exists;
- after navigating away, the owner cannot find a normal primary-menu path back to it;
- the F11 links are visually relegated to the low-priority sidebar control/footer area rather than integrated into the normal task/navigation hierarchy.

This blocks completion of the real F11A owner journey even though the underlying technical surface is deployed.

## 4. Bounded remediation admitted under existing Provisional scope

No Product Contract expansion is required. The repair stays inside the approved F11 `Provisional 0.1.0` behavior:

1. promote `Проекты` and `Материалы компании` into primary Workspace navigation;
2. make every project card expose the same six owner-facing sections:
   - `Где сейчас`;
   - `Что уже сделано`;
   - `Что можно делать сейчас`;
   - `Ветки развития`;
   - `Что заблокировано / ждёт`;
   - `Где выполнять`;
3. move repository/path/exact SHA/content hash/fetch provenance into collapsed technical details;
4. use explicitly registered repository-owned canonical roadmap/status sources rather than pointer files when a more direct canonical current source is already evidenced;
5. derive execution-target labels only from explicit source text or explicit Company coordination metadata; otherwise display `Не указано`;
6. preserve `reconciliation-required` where no truthful registered source exists;
7. preserve read-only semantics: no roadmap write, no remote execution, no chat/model-memory authority.

## 5. Source reconciliation discovered during remediation

Repository inspection confirms:

- Arvectum Company — `docs/roadmap/ROADMAP.md`;
- Arvectum OS — `docs/roadmap/ROADMAP.md`;
- Tender Agent — repository-owned `STATUS.md` provides current product snapshot and next milestone and is admitted as the registered F11 status source; no roadmap write or lifecycle claim is created;
- Discount Parser — `docs/ROADMAP.md`;
- Arvectum Proxy Launcher — `docs/ROADMAP.md`;
- Creative Test Agent — `docs/roadmap/CURRENT.md` is the actual current canonical roadmap; top-level `ROADMAP.md` is only an index/pointer;
- PORT-005 remains unresolved and is not silently merged with Tender Agent;
- Doors Parser and Data Platform remain `reconciliation-required` until an applicable canonical roadmap/status source is explicitly admitted.

## 6. Governance disposition

- F11 Product Contract — `Provisional 0.1.0` unchanged;
- F11A — remediation deployed / **OWNER RECHECK PENDING**; attempt #1 remains FAIL;
- F11B — remediation deployed / **OWNER RECHECK PENDING**; attempt #1 remains FAIL;
- P9.11 — `Current`;
- R32 — `Locked`;
- canonical asset admission — unavailable;
- no Stable Product Contract or Active Platform Capability claim.

The earlier F11 functional cross-review already reached the maximum 7 iterations. This owner-evidence remediation is not labeled an eighth functional cross-review iteration; it is a bounded defect repair inside the already approved Product Contract scope.

## 7. Recheck criterion

After the remediation is merged and governed-deployed, the owner must recheck the real live Workspace. PASS requires, at minimum:

- `Материалы компании` is directly discoverable from primary navigation after arbitrary navigation;
- `/projects` is visually readable without horizontal card scanning;
- every project uses the same owner-facing structure;
- technical provenance is available on demand but does not dominate first glance;
- truthful source-backed data is pulled where an admitted canonical roadmap/status source exists;
- unresolved sources remain explicitly unresolved;
- the owner can answer from one screen where each project stands, what is available next and where the action belongs.

Until that real recheck, F11A/F11B remain owner FAIL / remediation deployed / owner recheck pending and R32 stays locked.

## 8. Post-deploy remediation evidence

- PR #15 release-bearing merge SHA: `3b8044db42c2d029458434c8bd90761d2e720a9d`;
- Workspace: `p9.11.8` / app contract `11`;
- exact reviewed head: `d069abba5a7fb175ad16265abeb3d7d3bd968c90`;
- Productive Workspace CI `32995660581`: `PASS`;
- Reference Python CI `32995661043`: `PASS`;
- P7.06 governed deployment: `PASS`, transaction `d8588f7c7da5e75e4c64f6a25d512c4311c1dc9554eab8558d3bd83266a998ce`;
- P7.06 backup: `p7-03-backup-20260826T175516Z-a78ca28c0053fdbe.tar.gz`, SHA-256 `c7ad0c2c75c4db20184f79aad7a03ba4ca40d0bb12ca41a2eb222ab98bee0c92`;
- technical smoke: P7.02/P7.05 healthy; `CURRENT_EXACT`; `MANAGED_SPAWN_PROOF`; one loopback `127.0.0.1:8769` listener; exact frontend/BFF assets and Desktop launcher verified;
- F11B smoke: readable vertical/uniform cards, all six owner-facing sections, collapsed `Источник и технические доказательства`, Tender Agent `STATUS.md`, Creative Test Agent `docs/roadmap/CURRENT.md`, PORT-005 unresolved, Doors Parser/Data Platform reconciliation-required, and execution targets only from source evidence;
- F11A smoke: `Проекты` and `Материалы компании` are normal visible primary-sidebar entries; navigation away and return to Company Materials works through that menu; staged upload remains `StagedNonCanonical`, output remains `TransientOutput`, canonical asset admission is unavailable, and no Authorization, Organizational Authority or validated Knowledge is granted.

This is remediation deployment and technical smoke evidence only. It does not alter the `FAIL` result of owner validation attempt #1 and does not establish F11A or F11B owner PASS.

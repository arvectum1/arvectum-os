# P9.11-F11 — Real owner validation attempt 1

Status: `FAIL / remediation in progress`
Date: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `platform + product_contract + product_specific`
Product Contract: `P9.11-F11 Provisional 0.1.0`
Observed live Workspace: `p9.11.7` / app contract `11`
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
- F11A — deployed technical surface, owner validation **FAIL / remediation required**;
- F11B — deployed technical surface, owner validation **FAIL / remediation required**;
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

Until that real recheck, F11A/F11B remain owner FAIL/pending remediation and R32 stays locked.

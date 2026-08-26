# P9.11-F11 — Материалы компании и единый портфель проектов

Status: `Owner-approved / Product Contract Provisional 0.1.0 / implementation pending`
Version: `0.2.0`
Created: `2026-08-26`
Updated: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `platform` + `product_contract` with `product_specific` consumers
Roadmap work item: `P9.11 — Real daily-use dogfooding + friction/backlog closure`
Authority baseline: Constitution `1.2.0`; RFC-0001, RFC-0004, RFC-0005, RFC-0006, RFC-0007, RFC-0008 `Accepted 1.0.0`; ADR-0001 `Accepted`
Predecessor: [`P9.11-F10`](P9-11-F10-workspace-guidance-and-organizational-asset-intake-gap.md)
Product Contract: [`Provisional 0.1.0`](../contracts/P9-11-F11-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.1.0.md)
Owner approval: [`DECISION-2026-08-26-P9-11-F11-PROVISIONAL-APPROVAL`](../governance/decisions/DECISION-2026-08-26-P9-11-F11-PROVISIONAL-APPROVAL.md)
Transition review: [`P9-11-F11-provisional-transition`](P9-11-F11-provisional-transition.md)

## 1. Реальный owner feedback и диспозиция F10A

После governed deployment Workspace `p9.11.6` владелец выполнил реальный визуальный recheck встроенного `/guide` и сообщил:

> `руководство есть, оно понятное. но пока система пустая, работать не с чем.`

Это даёт **bounded owner PASS для F10A** только в scope понятности встроенного руководства: руководство существует, доступно владельцу и понятно объясняет текущие возможности/ограничения Workspace.

Тот же реальный owner session выявил два следующих material findings:

1. Workspace не принимает организационные исходники и шаблоны, поэтому из него нельзя собрать стандартный документ ООО «Арвектум» по выбранному проекту;
2. Workspace не показывает единый актуальный статус дорожных карт текущих проектов и не помогает увидеть завершённое, текущую точку, ветви, разблокированные действия и место их выполнения.

F10A не переоткрывается. F10B/F10C не объявляются завершёнными: их предмет конкретизирован в F11A.

## 2. Разделение F11

F11 выполняется двумя параллельными, но явно разделёнными потоками:

- **F11A — «Материалы компании + стандартный документ»**;
- **F11B — «Портфель проектов + синхронизация дорожных карт»**.

Оба потока являются Company-specific использованием Productive Workspace. Arvectum OS предоставляет только domain-neutral механизмы и не становится владельцем брендовых правил, шаблонов ООО «Арвектум», project portfolio semantics или product roadmap truth.

## 3. F11A — целевой owner journey

### 3.1 Материалы компании

В Workspace появляется owner-facing раздел `Материалы компании`, где владелец может:

1. добавить файл;
2. выбрать Company-owned роль материала, например `Логотип`, `Брендбук`, `Шаблон документа`, `Шаблон презентации`, `Шаблон письма`, `Организационный источник`, `Другое`;
3. указать понятное название и при необходимости назначение/описание;
4. увидеть uploader/Actor, дату приёма, Organization scope, classification, provenance, subject identity и immutable version identity;
5. открыть конкретную версию, увидеть историю версий и выбрать точную версию для использования;
6. найти материал через owner-facing discovery;
7. заменить материал только созданием новой версии, не переписывая историческую версию молча.

Receipt файла не означает автоматического признания его валидированным Knowledge, утверждённым Standard, Policy, решением или authority grant.

### 3.2 Создание стандартного документа

Из `Материалов компании` и/или проекта владелец получает действие `Создать стандартный документ`:

1. выбрать конкретный проект по стабильному Company-owned project identity;
2. выбрать тип результата;
3. выбрать точную версию шаблона;
4. выбрать точные версии логотипа/брендбука/дополнительных источников;
5. создать preview/draft;
6. увидеть, какие exact input versions использованы;
7. получить generated Artifact как **Transient Output по умолчанию**;
8. после человеческой проверки отдельно сохранить/экспортировать/продвинуть результат допустимым governed путём, если это требуется.

`Одна кнопка` означает простой owner journey, а не обход provenance, version pinning, authorization, Organizational Authority, Data Governance или Governed Execution.

### 3.3 Platform / Company boundary

**Platform-owned, domain-neutral:** приём bytes/governed external reference; Organization/Actor attribution; stable subject identity; immutable version identity; digest; provenance/received-at; classification/retention/rights metadata where applicable; version listing/resolution; exact-version selection; discovery; portability/export; RFC-0008 Document/Artifact semantics; RFC-0005 governed canonical admission where consequential canonical state is created.

**Company-owned:** роли материалов; правила фирменного стиля; конкретные шаблоны; типы стандартных документов; project binding; правила выбора шаблонов; инструкции генерации и UX; критерии внутреннего утверждения результата.

## 4. F11B — единый портфель проектов

### 4.1 Owner-facing dashboard

В Workspace появляется раздел `Проекты` с единообразной карточкой каждого явно зарегистрированного текущего проекта.

Карточка показывает:

- stable project identity и display name;
- canonical repository/source locator;
- exact source commit SHA;
- время последней успешной синхронизации и freshness;
- phase/milestone, если источник это определяет;
- что завершено;
- где проект находится сейчас;
- текущие/следующие ветви развития;
- какие действия разблокированы;
- какие действия заблокированы и чем;
- где действие должно выполняться, только если это явно определено;
- provenance на исходный roadmap/status source.

### 4.2 Execution target vocabulary

Company-owned presentation vocabulary:

- `web`;
- `mac-mini`;
- `macbook`;
- `windows-laptop`;
- `windows-test-laptop`;
- `linux-test-laptop`;
- `unspecified`.

Одно действие может иметь несколько execution targets. Workspace не угадывает target по чату, модели, имени репозитория или названию задачи. При отсутствии явного evidence показывает `Не указано`.

### 4.3 Source-of-truth rule

Dashboard является **derived read-only projection**, а не новой дорожной картой.

- `arvectum-os` roadmap остаётся authoritative для Arvectum OS sequencing/status;
- `arvectum-company` roadmap/approved portfolio governance остаются authoritative для Company-level sequencing и PORT identity;
- product repositories остаются authoritative для product-specific roadmap/status/domain semantics;
- project chat/model memory не являются roadmap authority;
- GitHub repository paths are locators, not stable Company project identities.

При конфликте dashboard показывает conflict/stale/unknown и provenance; он не выбирает удобную правду молча.

### 4.4 Registry и неодинаковые roadmap formats

Первый slice не требует переписывать все project roadmaps в один Markdown layout. Company-owned project registry для каждого admitted project задаёт stable project identity, display name, canonical repository, canonical roadmap/status source descriptor, adapter/export version и optional technical execution constraints source.

Если canonical roadmap/status source недостаточно определён, карточка показывает `Требуется reconciliation`, а не строится из чатов.

### 4.5 Sync model первого slice

Минимальный режим: `External Reference` для canonical GitHub sources + rebuildable non-canonical cache/projection.

Sync получает exact repository/ref/SHA; читает только зарегистрированные canonical source paths; сохраняет SHA/fetched-at/freshness/provenance; не имеет write access; не создаёт задачи и не меняет статусы; fail-visible на source/network/schema/adapter conflict; credentials остаются server-side; cache не становится authority.

## 5. Начальный project registry scope

Источником portfolio identity является approved Company governance, а не автоматический список GitHub repositories.

Для первого reconciliation рассматриваются Arvectum Company, Arvectum OS и approved Company portfolio nodes PORT-001…PORT-007 из AC-301. Дополнительные repositories включаются только после Company-owned решения, что это current project.

Реальный inventory уже показывает неодинаковую структуру: Arvectum OS и Arvectum Company используют `docs/roadmap/ROADMAP.md`, Proxy Launcher — `docs/ROADMAP.md`; поэтому adapter/source-descriptor layer обязателен.

## 6. Product Contract gate — RESOLVED FOR PROVISIONAL IMPLEMENTATION

На этапе F10B applicable Arvectum Company Product Contract отсутствовал. В F11 exact Draft `0.1.0` был подготовлен и прошёл functional cross-review.

Владелец затем явно утвердил exact boundary формулировкой:

> `утверждаю Product Contract F11 v0.1.0 в Provisional scope`

Approval Record: [`DECISION-2026-08-26-P9-11-F11-PROVISIONAL-APPROVAL`](../governance/decisions/DECISION-2026-08-26-P9-11-F11-PROVISIONAL-APPROVAL.md).

Lifecycle-current publication: [`Provisional 0.1.0`](../contracts/P9-11-F11-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.1.0.md).

The gate is therefore resolved **only for bounded implementation and real validation within the exact approved scope**. It does not create Stable status, implementation PASS, authority grants, operational readiness or Platform Capability promotion.

## 7. Acceptance criteria

### F11A acceptance

PASS требует real owner journey на live Workspace:

1. загрузить минимум один real Company asset и один real template;
2. inspect exact version/provenance;
3. выбрать project + exact template + exact supporting versions;
4. создать реальный standard document;
5. inspect exact input provenance; output remains Transient Output by default;
6. owner confirms practical usefulness.

### F11B acceptance

PASS требует live owner dashboard с real canonical sources:

1. admitted projects показывают canonical status либо explicit reconciliation/error state;
2. source repo/path/SHA/freshness inspectable;
3. done/current/branches/unlocked/blocked normalize without replacing source truth;
4. execution target only from explicit evidence, otherwise `Не указано`;
5. минимум два heterogeneous roadmap layouts normalize correctly;
6. source update после sync отражается с новым SHA;
7. owner confirms dashboard answers where projects are and what can be done next.

Repo tests/synthetic fixtures/screenshots alone do not provide owner PASS.

## 8. Security / failure baseline

F11A first slice uses a conservative allowlist. PNG/JPEG/WebP/PDF/DOCX/PPTX/TXT/MD may be admitted only after actual content/type validation. SVG requires safe sanitization/active-content rejection. Generic archives with uncontrolled nested content, executables/scripts/installers and macro-enabled Office formats (`DOCM`, `PPTM`, `XLSM`) are excluded.

DOCX/PPTX being OOXML ZIP containers does not classify them as generic arbitrary archives; they require structural validation as allowed OOXML classes and must fail closed on macro/active/external-content conditions defined by implementation.

F11B must never present stale data as current, infer missing status from chat/model memory, expose GitHub credentials to browser code, or obtain write access to canonical roadmaps.

## 9. Cross-review

Iteration 1 resolved design risks around platform leakage, admission vs receipt, transient outputs, active upload content, roadmap authority, stale data, browser credentials, hidden CAP-002/CAP-003 reliance, execution-target authority and exit/portability.

Post-approval iteration 2 rechecked the exact approved boundary against Constitution 1.2.0, RFC-0001/0004/0005/0006/0007/0008 and ADR-0001. The OOXML/archive wording was clarified without expanding approved behavior.

Material objections after iteration 2: **none**.

Functional review is not implementation acceptance, owner-usefulness PASS, Product Contract Stable promotion or operational-readiness approval.

## 10. Current disposition

- F10A — bounded owner PASS for guide understandability;
- F11 Product Contract — `Provisional 0.1.0`;
- F11A — implementation admitted, not yet PASS;
- F11B — implementation admitted, not yet PASS;
- P9.11 — `Current`;
- R32 — `Locked`;
- next canonical implementation sequence: `F11A1 → F11A2` and `F11B1 → F11B2`, then governed deploy and real owner validation.

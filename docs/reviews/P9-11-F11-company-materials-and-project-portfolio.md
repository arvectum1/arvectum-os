# P9.11-F11 — Материалы компании и единый портфель проектов

Status: `Draft / owner-approved problem statement / Product Contract gate pending`
Version: `0.1.0`
Created: `2026-08-26`
Updated: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `platform` + `product_contract` with `product_specific` consumers
Roadmap work item: `P9.11 — Real daily-use dogfooding + friction/backlog closure`
Authority baseline: Constitution `1.2.0`; RFC-0001, RFC-0004, RFC-0005, RFC-0006, RFC-0007, RFC-0008 `Accepted 1.0.0`; ADR-0001 `Accepted`
Predecessor: [`P9.11-F10`](P9-11-F10-workspace-guidance-and-organizational-asset-intake-gap.md)

## 1. Реальный owner feedback и диспозиция F10A

После governed deployment Workspace `p9.11.6` владелец выполнил реальный визуальный recheck встроенного `/guide` и сообщил:

> `руководство есть, оно понятное. но пока система пустая, работать не с чем.`

Это даёт **bounded owner PASS для F10A** только в scope понятности встроенного руководства: руководство существует, доступно владельцу и понятно объясняет текущие возможности/ограничения Workspace.

Тот же реальный owner session выявил два следующих material findings:

1. Workspace не принимает организационные исходники и шаблоны, поэтому из него нельзя собрать стандартный документ ООО «Арвектум» по выбранному проекту;
2. Workspace не показывает единый актуальный статус дорожных карт текущих проектов и не помогает увидеть завершённое, текущую точку, ветви, разблокированные действия и место их выполнения.

F10A не переоткрывается. F10B/F10C не объявляются завершёнными: их предмет включается в более конкретный F11A ниже.

## 2. Разделение F11

F11 выполняется двумя параллельными, но явно разделёнными потоками:

- **F11A — «Материалы компании + стандартный документ»**;
- **F11B — «Портфель проектов + синхронизация дорожных карт»**.

Оба потока являются Company-specific использованием Productive Workspace. Arvectum OS предоставляет только domain-neutral механизмы и не становится владельцем брендовых правил, шаблонов ООО «Арвектум», project portfolio semantics или product roadmap truth.

## 3. F11A — целевой owner journey

### 3.1 Материалы компании

В Workspace появляется owner-facing раздел `Материалы компании`, где владелец может:

1. добавить файл;
2. выбрать Company-owned роль материала, например:
   - `Логотип`;
   - `Брендбук`;
   - `Шаблон документа`;
   - `Шаблон презентации`;
   - `Шаблон письма`;
   - `Организационный источник`;
   - `Другое`;
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

**Platform-owned, domain-neutral:**

- приём bytes или governed external reference;
- Organization/Actor attribution;
- stable subject identity;
- immutable version identity;
- content digest;
- provenance/received-at;
- classification/retention/rights metadata, когда применимо;
- version listing/resolution;
- exact-version selection;
- discovery;
- portability/export mechanics;
- RFC-0008 Document/Artifact semantics;
- RFC-0005 governed canonical admission where consequential canonical state is created.

**Company-owned:**

- роли `логотип`, `брендбук`, `шаблон письма`, `шаблон презентации` и т.п.;
- правила фирменного стиля;
- конкретные шаблоны и их содержимое;
- типы стандартных документов ООО «Арвектум»;
- product/project binding semantics;
- правила выбора шаблонов;
- инструкции генерации и UX;
- критерии, когда результат можно считать внутренне утверждённым/готовым.

## 4. F11B — единый портфель проектов

### 4.1 Owner-facing dashboard

В Workspace появляется раздел `Проекты` с единообразной карточкой каждого явно зарегистрированного текущего проекта.

Карточка показывает:

- стабильный project identity и понятное название;
- canonical repository/source locator;
- точный source commit SHA;
- время последней успешной синхронизации и freshness state;
- phase/milestone, если источник это определяет;
- что завершено;
- где проект находится сейчас;
- текущие/следующие ветви развития;
- какие действия разблокированы;
- какие действия заблокированы и чем;
- для каждого действия — где оно должно выполняться, если это канонически/явно определено;
- ссылки/provenance на исходный roadmap/status source.

### 4.2 Execution target vocabulary

Company-owned presentation vocabulary для физического места выполнения:

- `web` — веб/подключённые сервисы;
- `mac-mini` — основной Mac mini;
- `macbook` — MacBook;
- `windows-laptop` — рабочий ноутбук Windows;
- `windows-test-laptop` — стендовый ноутбук Windows;
- `linux-test-laptop` — стендовый ноутбук Linux/Astra;
- `unspecified` — источник не определяет место выполнения.

Одно действие может иметь несколько `execution_targets`.

Workspace **не угадывает** execution target по названию задачи, чату, модели или имени репозитория. Если authoritative/project-owned source не задаёт требование, интерфейс показывает `Не указано`. Company-owned coordination может назначить конкретный host только в пределах product-owned технических ограничений и с явной provenance.

### 4.3 Source-of-truth rule

Dashboard является **derived read-only projection**, а не новой дорожной картой.

- `arvectum-os` roadmap остаётся authoritative для Arvectum OS sequencing/status;
- `arvectum-company` roadmap/approved portfolio governance остаются authoritative для Company-level sequencing и PORT identity;
- product repositories остаются authoritative для product-specific roadmap/status/domain semantics;
- project chat/model memory не являются roadmap authority;
- GitHub repository paths are locators, not stable Company project identities.

При конфликте dashboard показывает conflict/stale/unknown и ссылки на источники; он не выбирает «удобную» правду молча.

### 4.4 Registry и неодинаковые roadmap formats

Первый slice не требует переписывать все project roadmaps в один Markdown layout.

Company-owned project registry должен для каждого admitted project задавать:

- stable project identity;
- display name;
- canonical repository;
- canonical roadmap/status source descriptor;
- adapter/export version;
- optional product-owned technical execution constraints source.

Если проект не имеет достаточно определённого canonical roadmap/status source, его карточка остаётся видимой как `Требуется reconciliation`, а не строится из чатов.

Долгосрочно допускается machine-readable `project status export`, но он должен быть либо:

1. derived/validated projection из canonical roadmap, либо
2. явно назначенной authoritative частью самого project governance.

Нельзя создавать второй несинхронизированный planning source только ради удобства Workspace.

### 4.5 Sync model первого slice

Предпочтительный минимальный режим: `External Reference` для canonical GitHub sources + rebuildable non-canonical cache/projection.

Sync должен:

- получать exact repository/ref/commit identity;
- читать только зарегистрированные canonical source paths;
- сохранять source SHA/fetched-at/freshness/provenance в projection;
- не иметь write access к product roadmaps;
- не создавать задачи и не менять статус проектов;
- fail closed/visible на network/source/schema/parse conflict;
- не использовать GitHub credentials в browser;
- выполняться server-side через BFF/provider boundary;
- не превращать cached projection в canonical authority.

Если позднее потребуется Governed Replica/offline-first authority behavior, это отдельное изменение Product Contract с freshness/conflict/failure semantics.

## 5. Начальный project registry scope

Источником portfolio identity является approved Company governance, а не автоматический список всех GitHub repositories.

Для первого reconciliation должны быть рассмотрены:

- `Arvectum Company`;
- `Arvectum OS`;
- approved Company portfolio nodes PORT-001…PORT-007 из AC-301;
- дополнительные репозитории (например company landing/site) только после явного Company-owned решения, что это текущий project, а не просто repository/asset.

Реальный inventory уже показывает неодинаковую структуру: например Arvectum OS и Arvectum Company имеют `docs/roadmap/ROADMAP.md`, Proxy Launcher имеет `docs/ROADMAP.md`, а не каждый product repository использует единый roadmap path. Поэтому adapter/source-descriptor layer обязателен.

## 6. Product Contract gate

На момент F10B applicable Arvectum Company Product Contract для governed organizational asset/template history отсутствовал. F11 расширяет потребность ещё и на Company portfolio projection.

До real governed reliance должен существовать явный Arvectum Company ↔ Productive Workspace Product Contract по RFC-0004.

Draft подготовлен рядом: [`P9-11-F11-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT`](../contracts/P9-11-F11-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT.md).

До explicit owner approval и допустимого lifecycle transition этот Draft:

- не разрешает real governed asset admission;
- не разрешает считать dashboard production-supported/current truth;
- не создаёт Platform Capability;
- не создаёт Stable/public API;
- не даёт authority/authorization.

Implementation может готовиться параллельно только как bounded/reversible gated work без real governed Company reliance.

## 7. Acceptance criteria

### F11A acceptance

PASS требует реального owner journey на live Workspace:

1. владелец загружает минимум один реальный Company asset и один реальный template;
2. обе сущности имеют inspectable exact version/provenance;
3. из UI выбирается конкретный project + exact template version + exact supporting asset/source versions;
4. по owner action создаётся реальный стандартный документ;
5. generated result показывает exact input provenance и остаётся Transient Output до отдельного допустимого сохранения/продвижения;
6. владелец подтверждает, что flow понятен и результат практически полезен.

Repo test/synthetic fixture/screenshots alone не дают owner PASS.

### F11B acceptance

PASS требует live owner dashboard с real canonical sources:

1. все admitted current projects либо показывают canonical status, либо явно показывают reconciliation/error state;
2. source repo/path/SHA/freshness доступны для проверки;
3. завершённое/current/branches/unlocked/blocked отображаются единообразно без подмены source truth;
4. execution target показывается только при explicit source/Company coordination evidence, иначе `Не указано`;
5. минимум два реально различающихся roadmap layouts успешно проходят adapters;
6. source update после sync отражается в dashboard с новым SHA;
7. owner подтверждает, что по одному экрану понятно «где мы сейчас и что можно делать дальше».

## 8. Explicit exclusions первого F11 slice

Не входят:

- автоматический final approval generated documents;
- автоматическая отправка писем/документов наружу;
- электронная подпись;
- customer/cross-Organization asset sharing;
- скрытая индексация всех файлов машины;
- превращение любых загруженных файлов в validated Knowledge;
- автоматическая запись/изменение roadmaps через dashboard;
- выполнение local/web actions прямо из dashboard;
- remote control Mac/Windows/Linux hosts;
- создание задач из ChatGPT chats без canonical promotion;
- public API/SDK;
- Stable Product Contract;
- Active Platform Capability promotion.

Action execution/dispatch из dashboard, если понадобится, будет отдельным RFC-0005 governed scope после доказанной пользы read-only projection.

## 9. Cross-review — iteration 1

Functional review ролей platform architecture / product boundary / security-data governance / UX / operational truthfulness выявил и устранил следующие material risks ещё в design:

- второй competing source of truth для project roadmaps → запрещён; dashboard только derived projection;
- browser-side GitHub credentials/network authority → запрещены; sync server-side;
- скрытое превращение uploaded bytes в Knowledge/Standard → запрещено;
- Company-specific brand semantics в Kernel/platform → оставлены product-owned;
- generated document как автоматически canonical/approved → Transient Output by default;
- execution target inference из чата/модели → запрещён;
- попытка сделать dashboard action dispatcher в первом slice → исключена;
- требование немедленно унифицировать все roadmap Markdown → заменено registry + adapters + честным reconciliation state.

Material objections after iteration 1: **none at design level**. Formal Product Contract owner approval, implementation review, CI, governed deployment and real owner acceptance остаются отдельными gates.

## 10. Disposition

- F10A: **bounded owner PASS — guide understandability**;
- F11A: **admitted as real owner finding; Product Contract gate pending**;
- F11B: **admitted as real owner finding; Product Contract gate pending**;
- P9.11: должен оставаться `Current`;
- R32: должен оставаться `Locked`;
- next canonical action after this draft: **owner review/approval of the exact F11 Product Contract boundary**, затем bounded implementation F11A/F11B и real acceptance.

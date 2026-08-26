# P9.11-F10 — Пробел в руководстве Workspace и приёме организационных материалов

Статус: `Исправление выполняется — F10A реализован в рабочей ветке; проверка границы F10B завершена; F10B/F10C не заявлены готовыми`
Дата: `2026-08-26`
Владелец: `ООО «Арвектум»`
Классификация задачи: `platform` с границей `product_contract` / product-owned content
Родительская задача: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## 1. Каноническая основа

Проверены и применены:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001…RFC-0008 — `Accepted 1.0.0`;
- RFC-0004 — до управляемой зависимости продукта от общих platform capabilities, shared history или canonical state требуется явный Product Contract;
- RFC-0005 — consequential canonical change выполняется через Governed Execution;
- RFC-0006 — provenance/event semantics не позволяют превращать прикладную телеметрию или локальную запись в каноническое событие по умолчанию;
- RFC-0007 — Observation, transient output и AI-вывод не становятся validated Knowledge автоматически;
- RFC-0008 — получение/обработка документа отделены от его канонического допуска; product-specific templates, taxonomies и workflows по умолчанию остаются product-owned; generated Artifact по умолчанию является Transient Output;
- ADR-0001 — Productive Workspace использует React/TypeScript SPA + same-origin Python BFF; browser/BFF не являются authority/canonical state; Organization scope, Authorization и Data Governance проверяются server-side;
- P9.11 остаётся `Current`; R32 остаётся закрыт до завершения реального dogfooding.

Конфликтов с источниками более высокого уровня не обнаружено.

## 2. Реальная обратная связь владельца

После F08/F09 владелец смог открыть чистый Workspace, но не смог понять, какую полезную работу в нём можно выполнять и где находятся соответствующие функции.

Зафиксированный вопрос владельца:

> ну а как пользоваться-то? я могу как-то загрузить туда шаблон презентации, например, или источников для презентации (логотип, брендбук) или шаблоны документов, писем, чтобы они потом делались по одному стандарту? или что я могу там делать и где? может быть стоит прикрутить руководство пользователя?

Это реальный finding P9.11, а не синтетический сценарий.

## 3. Что Workspace фактически умеет до F10

Проверка `reference/python/workspace_app/main.py` и текущего frontend подтверждает:

- Главная ведёт к задачам, поиску информации и Arvectum AI;
- `Задачи` показывают реальную owner-attention и доступные продуктовые контексты;
- `Документы` / `Информация` / `Знания` дают read-only discovery по уже существующему разрешённому управляемому контексту;
- открытие найденного объекта остаётся inspect-only и само по себе не создаёт consequential action;
- Arvectum AI принимает ограниченный вопрос и возвращает source-grounded transient answer по текущему разрешённому контексту;
- `Настройки` дают доступ к организации, активности, техническим проверкам, тестовым сценариям и обратной связи;
- browser-facing writes ограничены session/bootstrap/logout, dogfooding feedback/disposition, Copilot questions и bounded governed preflight;
- endpoint/UI для общего file upload/import, создания документов, шаблонов или произвольного organizational asset intake отсутствует.

Следовательно, до F10 через Productive Workspace нельзя:

- загрузить брендбук PDF;
- добавить логотип как организационный бренд-материал;
- загрузить шаблон презентации `.pptx`;
- загрузить шаблон документа `.docx`;
- создать и переиспользовать шаблон письма;
- добавить произвольные source files для будущей grounded generation;
- создать презентацию/документ из выбранных точных версий source/template/brand inputs.

Это не скрытая функция: её действительно нет в текущем контракте Workspace.

## 4. Finding A — пользователю непонятны возможности Workspace

Проблема состоит не только в отсутствии новых функций. Уже реализованные возможности не были собраны в понятный owner workflow, поэтому для ответа на вопрос «что здесь делать?» требовалось знание репозитория и архитектуры.

### Требуемое исправление F10A

Workspace должен содержать встроенное русскоязычное руководство, которое:

1. доступно без GitHub, терминала и README;
2. объясняет назначение основных разделов человеческим языком;
3. различает `работает сейчас` и `ещё не реализовано`;
4. показывает, что делать при нормальном пустом состоянии, когда задач нет;
5. не приписывает AI, поиску или UI организационные полномочия;
6. показывает точную Workspace release identity, чтобы текст руководства не выглядел обещанием возможностей другой версии;
7. прямо сообщает об отсутствии общего file/material intake, а не маскирует этот пробел.

### Реализация F10A

В рабочей ветке F10 добавлено:

- `reference/python/workspace_frontend/src/Guide.tsx` — встроенная поверхность `Руководство / Что здесь можно делать`;
- маршрут `/guide` в Productive Workspace;
- постоянная ссылка `Руководство` в sidebar;
- действие `Открыть руководство` на Главной;
- пояснение на Главной, что отсутствие задач является нормальным состоянием и не означает, что Workspace «не работает»;
- список текущих функций: Главная, Задачи, Документы, Arvectum AI, Настройки;
- явный раздел `Чего пока нет` с перечислением отсутствующих logo/brandbook/PPTX/DOCX/email/source-file intake возможностей;
- явное пояснение authority boundary: поиск, экран, кнопка и AI-ответ сами по себе не утверждают решения и не дают новых прав;
- release-aware вывод `context.release.id`;
- `Guide.test.tsx` с русскоязычными regression guards;
- Workspace release повышен с `p9.11.5` до `p9.11.6`; `app_api_contract` остаётся `11`, поскольку новый BFF/API контракт не вводится.

Английский режим существующего Workspace не удаляется: это было бы регрессией принятого RU/EN интерфейса. Русский остаётся production-default, а весь канонический F10 review и owner-facing первичный текст этой задачи ведутся на русском.

## 5. Finding B — отсутствует управляемый приём организационных материалов

Примеры владельца являются валидным организационным use case, но их нельзя исправить одной кнопкой `Загрузить`.

Domain-neutral intake-механизм должен как минимум сохранять, пропорционально типу материала:

- Organization scope;
- attributable uploader;
- content bytes либо управляемую external reference;
- тип/семантическую роль материала;
- применимые classification/purpose/rights/retention metadata;
- provenance и received-at;
- стабильную logical subject identity для значимого Document/Asset;
- immutable version/checkpoint identity для версии, на которую реально опираются;
- явную замену/версионирование вместо silent overwrite;
- поиск/повторное обнаружение;
- выбор точной source/template version для downstream use;
- экспорт/portability в соответствии с RFC-0008.

Owner-facing название может быть `Материалы компании` или `Библиотека`; Kernel terminology пользователю не требуется.

## 6. Результат архитектурной и Product Contract проверки F10B

### 6.1 Что может принадлежать платформе

Платформенно допустима только domain-neutral механика, например:

- принять материал в определённой Organization scope;
- сохранить provenance/version metadata;
- обеспечить контролируемое обнаружение и точный выбор версии;
- поддержать governed/external-reference semantics;
- обеспечить portability и policy enforcement.

Это не даёт платформе права интерпретировать конкретный файл как «правильный логотип Арвектум», «утверждённый коммерческий шаблон» или «обязательный стиль письма».

### 6.2 Что остаётся company/product-owned

Нельзя hard-code как platform-global semantics:

- логотип ООО «Арвектум»;
- брендбук и брендовые правила;
- шаблоны презентаций;
- шаблоны коммерческих писем;
- шаблоны документов;
- email templates;
- правила согласования этих материалов;
- брендовые инструкции для генерации.

### 6.3 Product Contract gate

В текущем каноническом `arvectum1/arvectum-os` не найден действующий Product Contract, который давал бы Arvectum Company управляемую зависимость от общего organizational asset/document/template history Arvectum OS для перечисленных company-owned материалов.

Поэтому F10 **не создаёт молча** такой контракт и **не объявляет** company-specific brand/template semantics платформенной возможностью.

До соответствующего Product Contract нельзя честно заявить F10B `PASS` в формулировке «загрузить реальный материал компании и использовать его через governed/product boundary».

Это архитектурный gate, а не техническая причина откладывать F10A.

## 7. Целевой owner journey после отдельного допуска F10B

```text
Материалы компании
    ↓
Добавить материал
    ↓
выбрать файл / external reference
    ↓
выбрать понятную роль:
Источник | Шаблон | Бренд-материал | Стандарт/руководство
    ↓
проверить metadata + scope + version
    ↓
сохранить через разрешённую границу
    ↓
найти / открыть / использовать точную версию
```

Сам факт поступления файла не должен автоматически означать:

- validated Knowledge;
- утверждённый стандарт;
- каноническое решение;
- Organizational Authority;
- разрешение на consequential action.

## 8. F10C — template-aware generation

F10C допускается только после реального intake точных source/template versions и соответствующей product/company boundary.

Пример будущего company-owned workflow:

```text
Создать презентацию
    ↓
выбрать точную версию шаблона
выбрать точные версии логотипа/брендбука
выбрать source documents / governed context
    ↓
AI/tooling создаёт Artifact
    ↓
Artifact остаётся Transient Output по умолчанию
    ↓
владелец проверяет результат
    ↓
явный save/promote/export при наличии соответствующего разрешённого пути
```

F10 не превращает это в speculative universal office automation внутри shared Kernel.

## 9. Критерии приёмки

### F10A

F10A считается технически готовым к owner recheck, когда:

- `/guide` доступен из обычного Workspace;
- Главная и sidebar дают очевидный путь к руководству;
- руководство на русском объясняет текущие возможности, местонахождение функций и ограничения;
- руководство показывает exact release identity;
- отсутствие загрузки материалов указано явно;
- authority-safe semantics не искажены;
- frontend build/tests/CI проходят.

Финальный UX PASS требует короткого реального owner recheck на развёрнутом `p9.11.6`.

### F10B

F10B может получить PASS только когда владелец через Workspace без GitHub/терминала:

1. добавит хотя бы один реальный организационный материал;
2. найдёт его снова;
3. увидит provenance/version information;
4. использует его через явную разрешённую governed/product boundary.

До прохождения Product Contract gate и реального owner proof этот критерий не считается выполненным.

### F10C

Нужен реальный end-to-end generated artifact из точных versioned inputs. Repository-only tests и synthetic screenshots не являются owner acceptance.

## 10. Functional cross-review

### Итерация 1

Проверены:

- соответствие Constitution/RFC-0001…0008/ADR-0001;
- отсутствие нового browser-side authority;
- отсутствие ложного утверждения о наличии upload/intake;
- отсутствие hard-coded company brand semantics в platform code;
- сохранение existing RU/EN behavior при русском production-default;
- отсутствие нового BFF/API compatibility promise;
- exact-release semantics.

Найдено одно техническое замечание: первоначальный frontend test использовал matcher `toHaveAttribute`, хотя `@testing-library/jest-dom` не входит в зависимости проекта. Тест исправлен на стандартный `getAttribute`, новая зависимость не добавлялась.

После исправления иных material objections на уровне статического functional review не обнаружено.

## 11. Диспозиция

F10 остаётся material finding P9.11, но теперь разделён честно:

- **F10A — реализован в рабочей ветке и готов к CI + deployed owner recheck**;
- **F10B — архитектурная/Product Contract проверка завершена; реализация общего intake и owner acceptance ещё не выполнены**;
- **F10C — не начат и не должен опережать admitted intake + Product Contract boundary**.

F07/F08/F09 не переоткрываются. P9.11 остаётся `Current`, R32 остаётся locked.

Следующее каноническое действие после merge/CI F10A: развернуть точный `p9.11.6`, провести короткий owner recheck руководства, затем отдельно решить Product Contract/bounded implementation path для F10B без переноса company-specific semantics в платформу.

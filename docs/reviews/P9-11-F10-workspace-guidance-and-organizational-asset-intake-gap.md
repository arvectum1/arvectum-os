# P9.11-F10 — Workspace Guidance and Organizational Asset Intake Gap

Status: `Observed / remediation required`
Date: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` / product-owned content boundary
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical basis

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- RFC-0004 requires an explicit Product Contract before governed product reliance on shared platform capabilities/history/state;
- RFC-0007 keeps Memory/Knowledge promotion explicit and prevents AI output from silently becoming validated Knowledge;
- RFC-0008 defines Document/Artifact architecture, keeps product-specific templates/taxonomies/workflows product-owned by default, and treats generated Artifacts as Transient Outputs by default until explicit governed promotion;
- ADR-0001 defines the Productive Workspace browser/BFF trust boundary and keeps product-specific browser semantics behind explicit registered/product-contract boundaries;
- P9.11 remains `Current`; R32 remains locked.

## Real owner feedback

After F08/F09 restoration and bounded owner recheck, the owner can open a clean Workspace but cannot determine what productive work can actually be done there. The owner asked:

> ну а как пользоваться-то? я могу как-то загрузить туда шаблон презентации, например, или источников для презентации (логотип, брендбук) или шаблоны документов, писем, чтобы они потом делались по одному стандарту? или что я могу там делать и где? может быть стоит прикрутить руководство пользователя?

This is a real P9.11 usability/productivity finding, not a synthetic scenario.

## Current implemented Workspace capability map

Repository inspection of `reference/python/workspace_app/main.py` and the current frontend establishes the following shipped behavior:

- Home routes to Tasks, Information search and Arvectum AI;
- Work shows current owner attention plus available product contexts;
- Information / Documents / Knowledge are read-only discovery over already-existing authorized governed source snapshots;
- Discovery result interaction is `inspect-only` and exposes no consequential action;
- Arvectum AI accepts a bounded question and produces a source-grounded transient answer over the current authorized Workspace context;
- System exposes Organization, Activity, Technical checks, Test scenarios and Feedback;
- current browser-facing writes are limited to session/bootstrap/logout, dogfooding feedback/disposition, Copilot questions and the bounded governed preflight;
- there is no file upload/import endpoint, multipart handler, document creation endpoint, template creation endpoint or browser UI for adding organizational materials.

Therefore the owner currently cannot, through Productive Workspace:

- upload a brandbook PDF;
- upload/store a logo as an organizational brand asset;
- upload a `.pptx` presentation template;
- upload a `.docx` document template;
- define/reuse an email template;
- add arbitrary source files for future grounded generation;
- create a presentation/document from selected governed sources and exact template/brand versions.

This is not a hidden or undocumented feature; it is not implemented in the current Workspace contract.

## Finding A — capability discoverability / user guidance

Even the implemented read/search/ask/diagnostic capabilities are not explained as a coherent user workflow. The owner should not need repository knowledge to discover what each Workspace section is for.

Required direction:

1. add a built-in Russian-first `Руководство` / `Что здесь можно делать` surface;
2. expose it from Home and/or persistent navigation without competing with primary work;
3. explain each current section in owner language with concrete examples;
4. clearly distinguish `работает сейчас` from `ещё не реализовано`;
5. provide contextual help from major routes;
6. keep the guide release-aware so it does not promise features absent from the exact deployed Workspace release;
7. do not use README/repository documentation as the ordinary owner's user manual.

A useful first version should cover at least:

- Главная — current attention and primary actions;
- Задачи — real actionable owner work only;
- Документы / Информация — search and inspect existing governed context;
- Arvectum AI — ask grounded questions about available context; answers are transient and not authority;
- Настройки — organization/activity/diagnostics/test scenarios/feedback;
- current limitations, including absence of file upload, document/template creation and general-purpose asset intake.

## Finding B — governed organizational asset intake

The owner's examples are a valid organizational-intelligence use case and fit the accepted architecture, but require a real intake workflow rather than merely more documentation.

The platform-level mechanism should remain domain-neutral and support bounded local intake of files/materials with, proportionate to the item:

- Organization scope and attributable uploader;
- content bytes or governed external reference;
- type/semantic role;
- classification/purpose/rights/retention metadata where applicable;
- provenance and received-at metadata;
- stable logical subject identity where the material becomes a significant Document/Asset;
- immutable version identity/checkpoint for relied-upon versions;
- explicit versioning/replacement rather than silent overwrite;
- search/discovery integration;
- exact source version selection for downstream generation;
- export/portability consistent with RFC-0008.

A minimal owner-facing entry point may be called `Библиотека` or `Материалы компании` rather than exposing Kernel terminology.

## Company/product-owned semantics

The following content must not become hard-coded platform-global business semantics:

- `логотип ООО «Арвектум»`;
- brandbook and brand rules;
- presentation templates;
- commercial-letter templates;
- document templates;
- email templates;
- approval rules for those templates;
- brand-specific generation instructions.

These are company/product-owned organizational materials. If Arvectum Company relies on shared Arvectum OS document/artifact/knowledge capabilities or shared canonical history for them, the applicable Product Contract must cover that reliance before governed use under RFC-0004. F10 does not itself create or promote such a Product Contract.

## Desired future owner journey

A truthful target journey is:

```text
Материалы компании
    ↓
Добавить материал
    ↓
choose file / external reference
    ↓
classify owner-facing role:
Источник | Шаблон | Бренд-материал | Стандарт/руководство
    ↓
review metadata + scope + version
    ↓
Save as governed organizational material
    ↓
search / inspect / use in Arvectum AI or a product workflow
```

For generation, a later product-owned workflow may support for example:

```text
Создать презентацию
    ↓
select exact presentation template version
select exact logo/brandbook versions
select source documents / governed context
    ↓
AI/tooling generates Artifact
    ↓
Artifact remains Transient Output by default
    ↓
owner reviews
    ↓
explicit save/promote/export as applicable
```

The same pattern can support documents and email drafts. Generation does not automatically create validated Knowledge, approval, Organizational Authority or a canonical final document.

## Remediation decomposition

### F10A — Built-in user guide / capability map

Small immediate Workspace UX task.

Goal: the owner can answer `what can I do here?` and `where do I do it?` without repository/terminal knowledge.

No backend upload capability is implied by the guide.

### F10B — Organizational Asset Intake boundary and minimal slice

Design and implement the smallest governed local intake slice compatible with RFC-0003/0004/0007/0008 and ADR-0001.

First useful file classes should be selected from real owner need, preferably:

- brand asset (SVG/PNG);
- brandbook/reference PDF;
- presentation template (`.pptx`);
- document template (`.docx`).

Do not claim universal format support before exact validation.

### F10C — Template-aware generation

Only after admitted source/template intake exists.

A product/company-owned workflow should select exact source and template versions, generate a transient Artifact, preserve derivation provenance and allow explicit owner review/export/promotion.

Do not implement speculative universal office automation inside the shared Kernel.

## Acceptance direction

F10A is acceptable when a real owner can open Workspace and independently identify the useful current capabilities, their locations and their limitations.

F10B is acceptable only when the owner can add at least one admitted real organizational material through Workspace, find it again, inspect provenance/version information, and use it through an explicit governed/product boundary without repository or terminal work.

F10C requires a real end-to-end generated artifact from exact versioned inputs; synthetic screenshots or repository-only tests are not owner acceptance.

## Disposition

F10 is a material P9.11 finding. It does not reopen F07/F08/F09. P9.11 remains Current and R32 remains locked.

Next action: implement F10A as the smallest immediate usability repair while performing the bounded F10B architecture/Product Contract check in parallel. Do not treat the guide as a substitute for the missing asset-intake capability.
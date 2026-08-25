# P9.11-F07 — Owner-first Workspace UX repair

Status: `Owner recheck failed / remediation under review`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical basis

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted` Productive Workspace browser topology;
- roadmap `2.95.9` — P9.11 remains `Current`, R32 remains locked;
- prior P9.11 Russian-first and branding repair remains the presentation baseline.

This is a bounded, reversible Workspace presentation repair. It changes no BFF route, session, security control, product contract, governed action, external-product logic, or owner authority.

## Finding and repair

The real owner recheck reviewed a screenshot of the deployed Workspace on canonical runtime `470d4e310973ed873eb71d1bec3cf0985288be6b`. It failed: the owner could not immediately identify what to do; the large welcome hero displaced work; scenario fixtures appeared as ordinary attention; raw English evidence appeared on Home; actions looked secondary; and deployed branding was unacceptable. The screenshot is not evidence of PR `#6`, which has not been deployed.

Implemented behavior:

- Home begins with compact Arvectum identity and `Что делать сейчас`, followed immediately by primary task, document-search, and Arvectum AI actions;
- ordinary Home and Tasks show only `live` attention items; scenario items appear only through explicit `Настройки → Тестовые сценарии` diagnostics;
- Home uses Russian presentation summaries and urgency labels without raw source/evidence/next-step strings; raw values remain in the detail screen under `Исходные данные`;
- primary navigation uses `Главная`, `Задачи`, `Документы`, `Arvectum AI`, and `Настройки` without changing stable route/backend IDs;
- the exact owner-provided `BRAND__Ok----Block.svg` asset remains unchanged and is displayed prominently in the sidebar;
- Workspace release advances to `p9.11.3`; application contract remains `11`.

## Intentional English

- `Arvectum`, `Arvectum OS`, and `Arvectum AI` are product names;
- `RU` and `EN` identify the explicit language selector;
- release IDs, hashes, API contracts, status codes, provider/source data, and other exact technical or evidence-bearing values remain truthful rather than being translated.

Source-provided evidence and product-owned content may remain in their original language. This repair does not translate those values or alter their semantics.

## Verification

- frontend tests assert Russian-default navigation, compact action-first Home, scenario separation, no-live-work state, Russian urgency, the exact Block SVG marker, and release identity;
- frontend typecheck, production build, and the no-Web-Storage guard pass;
- no runtime mutation, selected-Mac start, launcher action, or synthetic owner evidence was performed.

## Status and next step

F07 is real owner evidence and remains failed. The revised PR must receive final review, then be merged and governed-deployed before another real owner recheck. P9.11 remains `Current`; R32 remains locked; P9.12 has not started; M9 remains open.

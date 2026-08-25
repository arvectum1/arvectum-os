# P9.11-F07 — Owner-first Workspace UX repair

Status: `Implementation repair / owner recheck pending`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical basis

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted` Productive Workspace browser topology;
- roadmap `2.95.8` — P9.11 remains `Current`, R32 remains locked;
- prior P9.11 Russian-first and branding repair remains the presentation baseline.

This is a bounded, reversible Workspace presentation repair. It changes no BFF route, session, security control, product contract, governed action, external-product logic, or owner authority.

## Finding and repair

The unresolved owner feedback is that the default Workspace screen did not make the owner’s location, current priorities, and useful next actions clear enough at first glance. The repair makes Russian the default owner-facing flow and reduces internal wording in the main flow.

Implemented behavior:

- the default screen names `Arvectum OS · Рабочее пространство`, welcomes the owner, and explains the Workspace purpose in one short sentence;
- `Требует внимания` follows as the current-priority block with a concise owner-facing description;
- `Что сделать дальше` provides clear routes to work, search, and Arvectum AI;
- primary navigation uses `Главная`, `Работа`, `Источники`, `Arvectum AI`, and `Система`;
- product, activity, organization, governed-action, and search helper copy uses plainer Russian owner-facing wording;
- the canonical Arvectum SVG replaces the placeholder `AV` letter mark while retaining a single, compact `OS` product label.

## Intentional English

- `Arvectum`, `Arvectum OS`, and `Arvectum AI` are product names;
- `RU` and `EN` identify the explicit language selector;
- release IDs, hashes, API contracts, status codes, provider/source data, and other exact technical or evidence-bearing values remain truthful rather than being translated.

Source-provided evidence and product-owned content may remain in their original language. This repair does not translate those values or alter their semantics.

## Verification

- frontend tests assert Russian-default primary navigation, product identity, priority block, actionable next steps, and absence of the placeholder letter mark;
- frontend typecheck, production build, and the no-Web-Storage guard pass;
- no runtime mutation, selected-Mac start, launcher action, or synthetic owner evidence was performed.

## Status and next step

F07 is real implementation work, not a completed dogfooding finding disposition. P9.11 remains `Current`; R32 remains locked. The owner must recheck the exact Workspace through the admissible selected-Mac path after the F06 operational prerequisite is satisfied. No owner recheck PASS is claimed here.

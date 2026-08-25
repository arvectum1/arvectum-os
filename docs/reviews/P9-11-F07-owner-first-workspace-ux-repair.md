# P9.11-F07 — Owner-first Workspace UX repair

Status: `Repair merged / deployment + owner recheck pending`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical basis

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted` Productive Workspace browser topology;
- roadmap `2.95.10` — P9.11 remains `Current`, R32 remains locked;
- prior P9.11 Russian-first and branding repair remains the presentation baseline.

This is a bounded, reversible Workspace presentation repair. It changes no BFF route, session, security control, product contract, governed action, external-product logic, or owner authority.

## Finding and repair

The real owner recheck reviewed a screenshot of the deployed Workspace on canonical runtime `470d4e310973ed873eb71d1bec3cf0985288be6b`. It failed: the owner could not immediately identify what to do; the large welcome hero displaced work; scenario fixtures appeared as ordinary attention; raw English evidence appeared on Home; actions looked secondary; and deployed branding was unacceptable. The screenshot is evidence of the deployed pre-F07 UI and is not visual acceptance of the merged remediation.

Implemented canonical behavior through PR `#6`, merged as `3e0b472a015bde7a44ac8202f364fbf5ea568ebb`:

- Home begins with compact Arvectum identity and `Что делать сейчас`, followed immediately by primary task, document-search, and Arvectum AI actions;
- ordinary Home and Tasks show only `live` attention items; scenario items appear only through explicit `Настройки → Тестовые сценарии` diagnostics and are excluded from ordinary Activity attention;
- Home uses Russian presentation summaries and urgency labels without raw source/evidence/next-step strings; raw values remain in the detail screen under `Исходные данные`;
- primary navigation uses `Главная`, `Задачи`, `Документы`, `Arvectum AI`, and `Настройки` without changing stable route/backend IDs;
- the exact owner-provided `BRAND__Ok----Block.svg` asset is shipped as the local exact-release brand asset and displayed prominently in the sidebar;
- Workspace release advances to `p9.11.3`; application contract remains `11`.

## Intentional English

- `Arvectum`, `Arvectum OS`, and `Arvectum AI` are product names;
- `RU` and `EN` identify the explicit language selector;
- release IDs, hashes, API contracts, status codes, provider/source data, and other exact technical or evidence-bearing values remain truthful rather than being translated.

Source-provided evidence and product-owned content may remain in their original language. This repair does not translate those values or alter their semantics.

## Verification

Final reviewed head `5e5db4b0dbf84774cc5915baccce5a21e109d267` established:

- frontend tests: `27 passed`;
- frontend typecheck: PASS;
- no-Web-Storage guard: PASS;
- production build and committed exact assets: PASS;
- Productive Workspace CI run `32850241215`: PASS;
- Reference Python CI run `32850241199`: PASS;
- targeted local backend/reference run: `41 passed` plus one macOS `/var` symlink-policy baseline failure reproduced on canonical `main`, not introduced by F07;
- no selected-Mac runtime mutation occurred before merge;
- no synthetic owner evidence or browser-runner substitute was used.

## Status and next step

The implementation repair is now canonical, but F07 is not resolved by merge. The selected Mac must be governed-updated to the exact current canonical runtime carrying Workspace `p9.11.3` / app contract `11`; P7.02/P7.05, `CURRENT_EXACT`, admissible process proof and exact live assets must be verified; the exact-release Desktop launcher must be refreshed/opened; then the owner must perform another real visual/usability recheck.

Until that real recheck passes or the remaining friction is otherwise truthfully dispositioned, F07 remains open, P9.11 remains `Current`, R32 remains locked, P9.12 has not started and M9 remains open.

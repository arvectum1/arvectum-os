# P9.11-F07 — Owner-first Workspace UX repair

Status: `Owner recheck PASS in bounded Home/navigation/branding scope`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical basis

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted` Productive Workspace browser topology;
- P9.11 remains `Current`, R32 remains locked;
- prior P9.11 Russian-first and branding repair remains the presentation baseline.

This is a bounded, reversible Workspace presentation repair. It changes no BFF route, session, security control, product contract, governed action, external-product logic, or owner authority.

## Finding and repair

The first real owner recheck of the pre-F07 deployed Workspace failed: the owner could not immediately identify what to do; the large welcome hero displaced work; scenario fixtures appeared as ordinary attention; raw English evidence appeared on Home; actions looked secondary; and deployed branding was unacceptable.

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
- release IDs, hashes, API contracts, status codes, provider/source data, and other exact technical or evidence-bearing values remain truthful rather than being silently rewritten.

Source-provided evidence and product-owned content may remain in their original language where exposed on technical/detail surfaces. This does not make raw source text appropriate as the primary owner-facing explanation.

## Repository verification

Final reviewed head `5e5db4b0dbf84774cc5915baccce5a21e109d267` established:

- frontend tests: `27 passed`;
- frontend typecheck: PASS;
- no-Web-Storage guard: PASS;
- production build and committed exact assets: PASS;
- Productive Workspace CI run `32850241215`: PASS;
- Reference Python CI run `32850241199`: PASS;
- targeted local backend/reference run: `41 passed` plus one macOS `/var` symlink-policy baseline failure reproduced on canonical `main`, not introduced by F07;
- no synthetic owner evidence or browser-runner substitute was used.

## Real owner recheck after deployment

The owner subsequently reviewed the live `p9.11.3` Workspace.

Bounded F07 result:

- **Home first-glance orientation:** PASS — the owner reports that the Home page is now understandable;
- **Home visual quality:** PASS — the owner describes it as visually acceptable / pleasant;
- **primary actions:** PASS — the next-action area is visible and understandable;
- **navigation labels:** PASS in the bounded top-level sense;
- **branding:** PASS — the deployed Arvectum Block logo is acceptable.

The same session exposed a separate material downstream usability failure after entering the urgent task and the governed-action surface. That failure is not hidden inside F07 and is tracked canonically as [`P9.11-F08 — Task-to-Governed Action Comprehension and Actionability`](P9-11-F08-task-to-governed-action-comprehension.md).

## Status and next step

F07 is closed only in its bounded Home/navigation/branding scope. It does **not** close P9.11 or establish that the whole Workspace is owner-usable. F08 now carries the material blocker for task-detail and governed-action comprehension/actionability.

P9.11 remains `Current`; R32 remains locked; P9.12 has not started; M9 remains open.
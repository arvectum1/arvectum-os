# P9.11-F08 — Task-to-Governed Action Comprehension and Actionability

Status: `Observed / repair required`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical basis

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- RFC-0005 preserves the separation of Authentication, Authorization, Organizational Authority, Data Governance, validation and consequential approval, and requires Governed Execution for consequential canonical mutation;
- ADR-0001 — `Accepted` Productive Workspace browser topology; browser-visible controls are not authority and consequential commands must revalidate server-side;
- Workspace source/release under owner recheck: `p9.11.3` / app contract `11`;
- P9.11 remains `Current`; R32 remains locked.

## Real owner recheck

The real owner recheck after the F07 repair established a bounded positive result for the new Home/navigation/branding presentation: the Home page is understandable and visually acceptable, the next-action area is clear, and the owner-provided Arvectum Block logo is satisfactory.

The same recheck found a new material usability failure in the task-detail → governed-action path.

Observed owner feedback:

1. after opening the single urgent task, the task-detail page still contains substantial untranslated/raw English content and does not explain the situation in owner language;
2. the task detail is rendered together with the same queue item below it, so the list-level `Открыть` action can target the already-open focused route and appear non-functional;
3. `Открыть` and `Открыть выполнение` are visually crowded and their semantic difference is not understandable;
4. `Открыть выполнение` leads to a governed page dominated by internal terminology and English source/proof text rather than a plain-language explanation of what is blocked and what the owner can do;
5. the visually primary `Run governed preflight` button looks consequential, but the interface does not explain in plain Russian what it does or whether it is safe;
6. the governed route is classified by the shell as the fallback `system` group, so `Настройки` becomes the active top-level navigation item during a task journey, which further breaks orientation;
7. on long governed pages the desktop sidebar scrolls out with the document rather than acting as a stable orientation anchor;
8. the owner therefore cannot confidently progress from the apparently urgent task despite the Home page itself being understandable.

## Repository evidence

The current task projection creates the live preflight item as `WAITING_INPUT` / high urgency with source text:

- title: `Governed preflight is waiting for decision evidence`;
- reason: four governed gates remain `Waiting`;
- next step: inspect blockers and supply independently governed decision evidence through a governed-action flow `when available`.

The current My Work detail presents those raw values directly. When a focused item is open, the ordinary queue is also rendered below it; the list-level `Открыть` link can therefore navigate to the same focused URL and produce no visible transition.

The current shell groups `/governed` into the fallback `system` navigation bucket, so a route entered from an urgent task highlights `Настройки` rather than preserving task context.

The current governed projection hard-codes English presentation copy and exact RFC-0005 gate names/bases. Its preflight action is explicitly bounded:

- `consequential = false`;
- `canonical_mutation_requested = false`;
- `external_effect_requested = false`;
- `authority_provided = false`.

The underlying P7.06-UI4 proof bridge additionally states that it supplies none of the four action-specific decisions and exposes no consequential action request. Running the preflight only re-evaluates current retained evidence and records minimized owner-local non-canonical proof evidence; it cannot grant authority or approval and performs no canonical mutation or external effect.

Therefore the current `Run governed preflight` operation is non-consequential within this exact implementation, but the UI fails to communicate that truthfully and prominently.

More importantly, the current Workspace does **not** provide an admitted path to satisfy the four missing decisions. Presenting the item to the owner as if a confirmation can simply be supplied in the current screen is therefore misleading. The truthful state is a blocked governed execution with no in-Workspace resolution path yet, plus a safe optional re-check operation.

## Required repair direction

The bounded F08 repair must improve presentation without manufacturing authority or an approval workflow that does not exist.

1. **Task list vs detail**
   - ordinary list card has one clear CTA: `Посмотреть задачу`;
   - opening a task produces a dedicated detail state instead of rendering the same actionable list item immediately below it;
   - a distinct secondary `Назад к задачам` action is visually separated;
   - no same-route `Открыть` control that appears broken.

2. **Truthful task semantics**
   - do not say `Ожидается ваше подтверждение` when the current Workspace has no admitted decision-input path;
   - classify this exact live item in owner-facing presentation as blocked / awaiting governed decisions;
   - explain plainly that the system will not continue until the required decisions exist and that they cannot currently be supplied from this screen;
   - retain exact source/provenance under `Исходные данные` rather than presenting raw English as the primary explanation.

3. **Governed screen**
   - Russian-first owner summary at the top: what is stopped, why it is stopped, and whether anything is happening externally now;
   - translate the four fixed domain-neutral RFC-0005 gate concepts into plain Russian presentation while preserving the exact canonical gate names/bases on demand;
   - raw status codes, validation strings, provenance and English source evidence move under expandable technical/source details;
   - do not alter gate semantics or infer approval from UI state;
   - preserve task orientation: governed inspection reached from a task must remain in the `Задачи` owner context rather than unexpectedly highlighting `Настройки`;
   - on desktop, keep primary navigation available while scrolling long detail/governed pages.

4. **Preflight action**
   - rename owner-facing action to a truthful plain-language label such as `Перепроверить состояние`;
   - directly beside/before it state: this only re-checks the four conditions and records local non-canonical evidence; it does **not** change the document, does not call an external effect, does not grant authority and does not approve anything;
   - visually distinguish this safe diagnostic re-check from a real consequential action;
   - render the positive `безопасная проверка` explanation only when the live projection explicitly proves `consequential=false`, `canonical_mutation_requested=false`, `external_effect_requested=false` and `authority_provided=false`; if those characteristics drift, fail closed and do not present the action as safe;
   - after execution, present the result in plain Russian, including that nothing was changed and which decisions remain unresolved.

5. **No fake resolution path**
   - do not add `Approve`, `Authorize`, delegation, Data Governance approval or consequential approval controls merely to make the task resolvable;
   - a real decision-supply/action workflow, if required, is a separate governed capability and must be designed against RFC-0003/RFC-0005 and applicable product/platform boundaries before implementation.

## Acceptance for F08 repair

A real owner should be able to answer, without reading internal English text:

- what is blocked;
- why it is blocked;
- whether anything external is happening now;
- whether the available re-check button is safe;
- what the button will and will not do;
- whether the task can actually be resolved inside Workspace today;
- where to return after inspection;
- why the top-level navigation still indicates that they are working with a task rather than editing Settings.

No repository test or simulated click substitutes for that real owner recheck.

## Status

F07 is successful only in its bounded Home/navigation/branding scope. F08 now carries the material downstream usability blocker. P9.11 remains `Current`; R32 remains locked; P9.12 has not started; M9 remains open.
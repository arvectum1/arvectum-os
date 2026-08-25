# P9.11-F08 — Task-to-Governed Action Comprehension and Actionability

Status: `p9.11.5 deployed / real owner recheck pending`
Date: `2026-08-25`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## Canonical basis

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- RFC-0005 preserves the separation of Authentication, Authorization, Organizational Authority, Data Governance, validation and consequential approval, and requires Governed Execution for consequential canonical mutation;
- ADR-0001 — `Accepted` Productive Workspace browser topology; browser-visible controls are not authority and consequential commands must revalidate server-side;
- p9.11.4 deployment runtime: `dc0e0cff83a9031a3686191b5cf304ee03c2d1eb` / app contract `11`;
- PR `#7` merged as `2f1bf8f341c1a779805586e9f239c4442a65d96b` after exact-head Productive Workspace CI and Reference Python CI PASS;
- p9.11.4 governed deployment, exact assets, `CURRENT_EXACT`, and `MANAGED_SPAWN_PROOF` passed; the real owner recheck failed;
- PR `#8` merged as `037cd59d7917d52b3ff6aa2dea20dcad22ed484d`; exact reviewed head `dde1102d0892a6c71e7a47de9c3a93fba98c84de` passed Productive Workspace CI and Reference Python CI;
- canonical Workspace source/release is `p9.11.5` / app contract `11`;
- p9.11.5 is now deployed on selected-Mac canonical runtime `03ba2c72fb9460e97b628c4b3dac36ac496cb942`, with exact managed Workspace readiness verified;
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

The pre-repair task projection creates the live preflight item as `WAITING_INPUT` / high urgency with source text:

- title: `Governed preflight is waiting for decision evidence`;
- reason: four governed gates remain `Waiting`;
- next step: inspect blockers and supply independently governed decision evidence through a governed-action flow `when available`.

The pre-repair My Work detail presents those raw values directly. When a focused item is open, the ordinary queue is also rendered below it; the list-level `Открыть` link can therefore navigate to the same focused URL and produce no visible transition.

The pre-repair shell groups `/governed` into the fallback `system` navigation bucket, so a route entered from an urgent task highlights `Настройки` rather than preserving task context.

The governed projection exposes a bounded preflight action with these exact semantics:

- `consequential = false`;
- `canonical_mutation_requested = false`;
- `external_effect_requested = false`;
- `authority_provided = false`.

The underlying P7.06-UI4 proof bridge additionally states that it supplies none of the four action-specific decisions and exposes no consequential action request. Running the preflight only re-evaluates current retained evidence and records minimized owner-local non-canonical proof evidence; it cannot grant authority or approval and performs no canonical mutation or external effect.

Therefore the Workspace must not manufacture owner work from these Waiting gates when no concrete requested action exists. Governance gates may qualify or block a concrete product-owned action; they do not themselves define the owner task.

## Required repair direction

The bounded F08 repair improves presentation without manufacturing authority or an approval workflow that does not exist.

1. **Task list vs detail**
   - ordinary list card has one clear CTA: `Посмотреть задачу`;
   - opening a task produces a dedicated detail state instead of rendering the same actionable list item immediately below it;
   - a distinct secondary `Назад к задачам` action is visually separated;
   - no same-route `Открыть` control that appears broken.

2. **Truthful task semantics**
   - do not say `Ожидается ваше подтверждение` when the current Workspace has no admitted decision-input path;
   - do not project a preflight/proof as owner work when no concrete requested outcome exists;
   - retain exact source/provenance on demand rather than presenting raw implementation evidence as ordinary work.

3. **Governed diagnostics**
   - UI4 remains available as Settings diagnostics rather than an ordinary owner task;
   - the diagnostic surface states that no concrete action is requested;
   - the four fixed domain-neutral RFC-0005 gate concepts remain inspectable with exact canonical gate names/bases on demand;
   - raw status codes, validation strings, provenance and English source evidence remain technical/source detail rather than task semantics.

4. **Preflight action**
   - owner-facing action is `Перепроверить состояние`;
   - directly beside/before it state that this only re-checks the four conditions and records local non-canonical evidence; it does **not** change the document, perform an external effect, grant authority or approve anything;
   - render the positive `Безопасная проверка` explanation only when the live projection explicitly proves the exact waiting/non-consequential boundary; otherwise fail closed and withhold the safe action;
   - after execution, present the result without inventing a blocked owner task.

5. **No fake resolution path**
   - do not add `Approve`, `Authorize`, delegation, Data Governance approval or consequential approval controls merely to make the surface resolvable;
   - a real decision-supply/action workflow, if required, is a separate governed capability and must be designed against RFC-0003/RFC-0005 and applicable product/platform boundaries before implementation.

## Acceptance for F08 repair

A real owner should be able to establish, without reading internal English text:

- whether there is a real task requiring action now;
- that UI4 is a technical readiness check rather than an owner task when no concrete action request exists;
- whether anything external is happening now;
- whether the available re-check button is safe;
- what the button will and will not do;
- where the diagnostics live and how to return to Settings;
- that no urgency or required decision has been manufactured solely from Waiting governance gates.

No repository test or simulated click substitutes for that real owner recheck.

## Merged presentation repair

PR `#7`, merged as `2f1bf8f341c1a779805586e9f239c4442a65d96b`, made the focused task a dedicated Russian-first detail state, reduced the ordinary task card to `Посмотреть задачу`, moved raw evidence behind `Исходные данные`, and made the safe re-check understandable. Exact reviewed head `d2949821347fc3078757303d5858a67dfdd7e23b` passed Productive Workspace CI and Reference Python full CI before merge.

## Post-deploy owner recheck

The selected Mac was governed-updated to `dc0e0cff83a9031a3686191b5cf304ee03c2d1eb` / Workspace `p9.11.4`. P7.02/P7.05, exact release manifest and live assets passed; Workspace reached `CURRENT_EXACT` with `MANAGED_SPAWN_PROOF`. The owner found the mechanics clearer but the F08 result remained **FAIL**:

> Интерфейс понятнее стал. Но не понятна суть задачи. Что-то остановлено, требуется 4 каких-то действия. А каких и что конкретно делать — непонятно.

Root cause is semantic, not merely wording: P7.06-UI4 is a preflight-only proof bridge with no concrete action request, owner resolution path, authority, approval, canonical mutation, or external effect. `RuntimeAttentionProvider` nonetheless projected its Waiting gates as a high-urgency `WAITING_INPUT` owner task. Governance gates can qualify a concrete product-owned action; they cannot manufacture one.

## Merged owner-task eligibility repair

PR `#8`, merged as `037cd59d7917d52b3ff6aa2dea20dcad22ed484d`, advances Workspace to `p9.11.5` / app contract `11` and removes UI4 from ordinary attention, Home/Tasks and Activity alerts. UI4 remains available through `Настройки → Технические проверки` and its four canonical gates and fail-closed safe re-check are preserved. The diagnostic surface explicitly states that no concrete action is requested, ignores stale task-focus query parameters, returns to Settings, and does not describe an unchanged re-check result as a blocked task.

Exact reviewed head `dde1102d0892a6c71e7a47de9c3a93fba98c84de` passed:

- Productive Workspace CI, including SPA interaction/storage gates and BFF security/context tests;
- Reference Python CI full reference test suite;
- frontend `34 passed`, typecheck, Web Storage guard, production build and `git diff --check` as reported by the implementation task.

This merge creates no product business action, Authorization, Organizational Authority, Data Governance permission, consequential approval, canonical mutation or external effect. It is not owner usability acceptance.

## p9.11.5 selected-Mac deployment readiness

After the F09 lifecycle repair was merged and canonically synchronized, the selected Mac successfully governed-deployed canonical target `03ba2c72fb9460e97b628c4b3dac36ac496cb942` from runtime `dc0e0cff83a9031a3686191b5cf304ee03c2d1eb` with Workspace pre-state `NOT_RUNNING`.

- P7.06 preflight: `PASS`;
- P7.06 update: `PASS`;
- transaction: `8d8893f5207cbd52eb67e99abad593f6ce069add3314c95373f081abdcd74ae0`;
- backup SHA-256: `ee93ae8fd9d4d4f5b8729e8309e3459ef3fbbfbf7995516d15c9ce5f836ce836`;
- Workspace stop invoked / SIGTERM during deployment: `NO / NO`;
- runtime after equals canonical target: `YES`;
- P7.02/P7.05: `HEALTHY`;
- Workspace before explicit target start: `NOT_RUNNING`;
- exact managed target start attempts: `1`;
- Workspace `p9.11.5` / app contract `11`: `CURRENT_EXACT` with `MANAGED_SPAWN_PROOF`;
- loopback only: `YES`;
- exact index/assets: `PASS`;
- UI4 ordinary Home attention: `ABSENT`;
- UI4 ordinary Tasks attention: `ABSENT`;
- false HIGH urgency: `ABSENT`;
- Activity false alert: `ABSENT`;
- technical diagnostics: `AVAILABLE`;
- concrete-action diagnostic copy: `PASS`;
- Desktop launcher: `PASS`.

These are structural/runtime readiness checks, not real owner usability acceptance. F08 is now ready for the required real owner recheck on the deployed p9.11.5 Workspace.

## Adjacent-route audit

The read-only F08 audit found no additional task-journey change required outside this repair:

1. `/work` embeds the repaired task projection alongside product contexts; no independent owner-flow regression was changed in this repair.
2. `/information` still presents raw result kind, semantic role, authority mode, health state, and source state in its existing discovery/evidence surface. This is outside the focused task-to-governed repair and should be assessed as separate discovery UX work if owner evidence identifies it as friction.
3. `/copilot` keeps source roles, freshness, model details, and authority boundaries visible to preserve the existing grounded-answer/evidence boundary. No F08 change is admitted there.
4. `/system` remains an explicitly diagnostic and technical surface. UI4 is explicitly available there as `Технические проверки`, not as a Task.

F07 is successful only in its bounded Home/navigation/branding scope. F08 remains open pending the real p9.11.5 owner recheck. P9.11 remains `Current`; R32 remains locked; P9.12 has not started; M9 remains open.

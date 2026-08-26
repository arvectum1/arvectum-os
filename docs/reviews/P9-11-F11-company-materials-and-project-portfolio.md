# P9.11-F11 — Материалы компании и единый портфель проектов

Status: `Owner validation PASS in bounded F11A/F11B scope / Product Contract remains Provisional`
Version: `0.6.0`
Created: `2026-08-26`
Updated: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `platform` + `product_contract` + `product_specific`
Roadmap work item: `P9.11 — Real daily-use dogfooding + friction/backlog closure`
Authority baseline: Constitution `1.2.0`; RFC-0001, RFC-0004, RFC-0005, RFC-0006, RFC-0007, RFC-0008 `Accepted 1.0.0`; ADR-0001 `Accepted`
Predecessor: [`P9.11-F10`](P9-11-F10-workspace-guidance-and-organizational-asset-intake-gap.md)
Product Contract: [`Provisional 0.1.0`](../contracts/P9-11-F11-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.1.0.md)
Owner approval: [`DECISION-2026-08-26-P9-11-F11-PROVISIONAL-APPROVAL`](../governance/decisions/DECISION-2026-08-26-P9-11-F11-PROVISIONAL-APPROVAL.md)
Transition review: [`P9-11-F11-provisional-transition`](P9-11-F11-provisional-transition.md)
Deployment evidence: [`P9-11-F11-LOCAL-DEPLOY-2026-08-26`](P9-11-F11-LOCAL-DEPLOY-2026-08-26.md)
Workspace release: `p9.11.10`
App API contract: `11`
Merged source: `470878b8778fbac009d1ae52092879cf50d8f3f1`

## 1. Исходный реальный finding

После governed deployment Workspace `p9.11.6` владелец выполнил реальный визуальный recheck `/guide` и сообщил:

> `руководство есть, оно понятное. но пока система пустая, работать не с чем.`

Это зафиксировало bounded owner PASS для F10A и два следующих material findings:

1. Workspace не принимал организационные исходники/шаблоны и не позволял получить стандартный документ из точной версии шаблона;
2. Workspace не показывал единый актуальный read-only статус текущих проектов из их канонических roadmap sources.

F11 разделён на:

- **F11A — «Материалы компании + стандартный документ»**;
- **F11B — «Портфель проектов + синхронизация дорожных карт»**.

Product Contract `0.1.0` утверждён владельцем только в lifecycle `Provisional`. Это разрешает bounded implementation и real validation, но не создаёт Stable status, Organizational Authority, operational-readiness approval или Platform Capability promotion.

## 2. Реализованный F11A slice

Workspace release `p9.11.7` содержит owner-facing `/company-materials` в существующем React SPA и same-origin Python BFF.

Текущий bounded flow позволяет:

1. принять owner-selected Company material как **`StagedNonCanonical`**;
2. привязать его к текущему server-resolved Organization и Actor;
3. зафиксировать stable `MAT-*` subject identity и immutable `MV-*` version identity;
4. сохранить exact SHA-256 bytes, uploader, received-at, semantic role, classification, purpose, rights, retention rule, project binding и predecessor version;
5. добавить новую версию без silent rewrite старой;
6. получить список точных staged versions в текущем Organization scope;
7. выбрать exact DOCX version и сгенерировать DOCX по bounded placeholders `{{TITLE}}`, `{{BODY}}`, `{{DATE}}`;
8. получить generated file как **`TransientOutput`** с exact source material/version/hash provenance;
9. скачать exact transient DOCX только после текущей server-side access revalidation.

Это **не** является canonical admission. Upload/generation не создают Authorization, Organizational Authority, Consequential Approval, validated Knowledge, Standard, Policy или canonical Document/Artifact.

### 2.1 Security / Data Governance first slice

Server не доверяет filename extension или browser MIME как доказательству типа. Фактические bytes проверяются до staged receipt.

Первый allowlist:

- DOCX;
- PPTX;
- PDF;
- PNG;
- JPEG;
- WebP;
- UTF-8 TXT/MD.

Fail-closed:

- generic `application/octet-stream`;
- SVG без отдельного sanitizer;
- macro-bearing OOXML content (`vbaProject.bin`);
- encrypted/unsafe OOXML archive paths;
- oversized material/expanded OOXML;
- declared type, не соответствующий фактическим bytes;
- cross-Organization manifest/version/output use;
- symlinked staged metadata/output targets;
- invalid project/material/version/output identities.

Owner-local staged directories получают `0700`, staged blobs/manifests/transient outputs — `0600` на POSIX runtime.

## 3. Реализованный F11B slice

Workspace release `p9.11.7` содержит owner-facing `/projects`.

Источник identity/ownership registry — approved Company governance AC-301 плюс Approved Git migration closure, а не автоматическое перечисление GitHub repositories.

Для source-backed карточки BFF server-side:

1. использует только packaged allowlisted repository/path descriptor;
2. получает exact canonical `main` SHA;
3. читает roadmap на exact SHA;
4. нормализует bounded status/current/branches/unlocked/blocked fields adapter-ом;
5. фиксирует repository, path, exact commit SHA, fetched-at, freshness, adapter;
6. дополнительно фиксирует **SHA-256 точных UTF-8 roadmap bytes**, использованных для нормализации;
7. не имеет roadmap write/remote execution path;
8. не использует chat/model memory как authority.

Если repository locator или roadmap source не reconciled, карточка показывает `reconciliation-required`. Если зарегистрированный canonical source недоступен или exact content identity не подтверждён, карточка показывает `unavailable`; статус не подменяется кэшем или памятью модели.

### 3.1 Registry reconciliation

Approved AC-301 сохраняет PORT-001…PORT-007 identities. Approved Git migration closure устанавливает `arvectum1/*` как canonical PRIMARY и содержит девять текущих canonical repositories.

PORT-005 (`Tender Small-Volume Calculator`) присутствует как Company identity, но `arvectum1/tender-app` фактически отсутствует (`404`) и не входит в approved список девяти canonical repositories. Поэтому F11 registry **не изобретает новый locator и не объединяет PORT-005 с Tender Agent**: repository/roadmap остаются unresolved, карточка — `reconciliation-required`.

## 4. Topology / deployment boundary

F11 не создаёт второй service/process/listener.

`p9_03_workspace.py` собирает существующий Workspace BFF и устанавливает F11 routes **до** существующего SPA catch-all. P7.06 продолжает разворачивать exact immutable `reference/python` release и перезапускает тот же Workspace process через существующий P9.11 process lifecycle.

Сохраняются:

- loopback-only owner-local Workspace profile;
- server-side session/access/context;
- exact release header guard;
- same-origin BFF;
- CSRF + Origin protection state-changing F11 routes;
- no browser credentials;
- no browser canonical state/Web Storage;
- exact release-pinned frontend assets.

## 5. Functional cross-review

### Iteration 1 — F11B exact source identity

Найдено: первоначальный `company_portfolio_verified.py` дублировал provider, но runtime продолжал использовать обычный provider, поэтому content SHA-256 фактически не попадал в live projection.

Исправлено: hashing boundary сделан композиционным; runtime использует `VerifiedRuntimeCompanyPortfolioProvider`; source-backed карточка без exact content SHA-256 fail-closed в `unavailable`.

### Iteration 2 — F11A content safety / Organization scope

Найдено: первоначальный intake доверял declared `media_type`, разрешал `application/octet-stream` и unsanitized SVG; manifest/output не были достаточно жёстко bound к Organization.

Исправлено: actual-byte validation, conservative allowlist, macro/unsafe OOXML rejection, explicit Organization binding/filtering/revalidation, scoped download и owner-only filesystem permissions.

### Iteration 3 — Company registry authority

Найдено: PORT-005 содержал stale/nonexistent current locator `arvectum1/tender-app`.

Исправлено: approved PORT identity сохранена, locator удалён как unresolved; silent merge с Tender Agent не выполняется.

### Iteration 4 — CI/runtime integration

Первый Productive Workspace CI обнаружил две implementation errors:

- `test_company_materials.py` случайно зависел от отсутствующего `pytest` в locked Workspace test environment;
- F11 route installer искал `/ {full_path:path}` вместо фактического `/{path:path}` catch-all.

Исправлено: F11 tests переведены на native `unittest`; route order repaired; BFF regression подтверждает, что F11 API не поглощается SPA.

### Iteration 5 — release/dist reproducibility

Source frontend проходил typecheck/tests/Web Storage guard/build, но committed `dist` был от `p9.11.6`.

Исправлено: release поднят до `p9.11.7`, exact production assets материализованы тем же Node 24 / `npm ci` CI build, затем временный branch-only CI write step удалён. Canonical workflow снова `permissions: contents: read`.

Final technical evidence на normal read-only workflow:

- Productive Workspace CI run `32981091559` on exact final reviewed head `d8211e903559cecea7331042023de89e4a90cbcc` — **PASS**:
  - BFF security/context tests — PASS;
  - frontend typecheck — PASS;
  - frontend tests — PASS;
  - Web Storage guard — PASS;
  - production build — PASS;
  - committed `dist` reproducibility — PASS;
  - release-pinned asset boundary — PASS.
- Reference Python CI run `32981091552` on the same exact reviewed head — **PASS**.

### Iteration 6 — final project-binding UX reconciliation

Найдено: F11 portfolio intentionally includes platform identity `OS`, while the first Company material-binding backend accepts only Company/product identities `COMPANY | PORT-*`. The material form initially reused every portfolio card and therefore offered `OS`, producing a visible option that the server correctly rejected.

Исправлено минимально: backend scope не расширялся на platform identity; F11A project selector filters to `COMPANY | PORT-*`. Exact final frontend bundle was rebuilt reproducibly and normal read-only CI passed.

### Iteration 7 — post-deploy evidence and authority-boundary reconciliation

Проверено owner-supplied selected-Mac deployment evidence against merged repository state, RFC-0005/RFC-0006/RFC-0008 and ADR-0001.

Результат:

- exact merged source/release identity agrees with canonical repository state;
- local P7.06/process/backup evidence is recorded explicitly as owner-supplied operational evidence rather than repository-observed fact;
- deployment/smoke PASS does not promote staged materials into canonical Documents/Artifacts, does not create Authorization/Organizational Authority and does not establish owner-usefulness PASS;
- F09's repaired ordinary stop/update/restart branch gained natural live PASS evidence from this running-Workspace update without broadening its bounded lifecycle scope;
- next evidence remains real owner F11A/F11B interaction.

Material objections after iteration 7 of maximum 7: **none**.

Functional review не является owner-usefulness PASS, Stable Product Contract promotion, canonical asset admission, authority grant или operational-readiness approval.

## 6. Governed deployment evidence

PR #12 squash-merged the implementation to canonical `main` at:

`ff73db4e0ee9917572654287d4dc74b4a0dea1ff`.

The selected Mac then reportedly completed one-pass P7.06 governed update from runtime/source `d5b4fdc3b81a82767473ed1da62f623773d4112a` / Workspace `p9.11.6` to exact merged runtime/source `ff73db4e0ee9917572654287d4dc74b4a0dea1ff` / Workspace `p9.11.7`.

Canonical deployment evidence record: [`P9-11-F11-LOCAL-DEPLOY-2026-08-26`](P9-11-F11-LOCAL-DEPLOY-2026-08-26.md).

Reported technical state:

- P7.06 transaction `edb403383cf719deb48c76040927bad19f50182d4d8a8a9524d217dafdc4a3a7` — PASS;
- P7.02/P7.05 — healthy;
- Workspace — `CURRENT_EXACT` / `MANAGED_SPAWN_PROOF`;
- listener — loopback-only `127.0.0.1:8769`;
- exact release manifest/assets — PASS;
- `/company-materials` technical smoke — PASS;
- `/projects` technical smoke — PASS;
- Desktop launcher — PASS;
- deployment friction — none;
- no rollback, canonical mutation, product external effect or historical-effect replay reported.

## 7. Acceptance state

### F11A

**Technical implementation: deployed and technical smoke PASS.**

Этот критерий был pending до p9.11.10 owner recheck; теперь он закрыт bounded owner PASS. Исторически требовалось минимум:

1. загрузить реальный Company asset;
2. загрузить реальный DOCX template;
3. inspect exact staged version/provenance;
4. выбрать project + exact template version;
5. создать реальный standard document;
6. скачать/inspect Transient Output и exact source provenance;
7. подтвердить практическую полезность либо дать реальный friction feedback.

Canonical asset admission **не реализован и не требуется для bounded staged owner journey**. Если понадобится canonical promotion, она должна идти отдельно через RFC-0005 decisions/gates.

### F11B

**Technical implementation: deployed and technical smoke PASS.**

Этот критерий был pending до owner recheck #3; теперь он закрыт bounded owner PASS. Исторически требовался live dashboard, который:

1. показывает source-backed либо explicit reconciliation/unavailable state;
2. даёт inspect repository/path/exact SHA/content hash/freshness;
3. корректно нормализует минимум два heterogeneous roadmap layout;
4. отражает новый source SHA после refresh;
5. практически отвечает владельцу, где находятся проекты и что доступно дальше.

## 8. Current disposition

- F10A — bounded owner PASS;
- F11 Product Contract — `Provisional 0.1.0`;
- F11A — **bounded owner PASS on live p9.11.10; canonical admission unavailable**;
- F11B — **bounded owner PASS after p9.11.9 cache-backed stability repair**;
- F09 — ordinary running-Workspace stop/update/restart path retains natural live PASS evidence from the F11 deployment, within its existing bounded scope;
- Workspace release — `p9.11.10`, app contract `11`;
- deployed selected-Mac runtime/source — `470878b8778fbac009d1ae52092879cf50d8f3f1` according to owner-supplied local evidence;
- Product Contract — `Provisional 0.1.0` unchanged;
- F11 owner-usefulness acceptance — **PASS in bounded F11A/F11B scope**;
- P9.11 closure criteria — satisfied with only minor/non-blocking visual and Word trust-prompt friction remaining;
- next canonical action — `R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate`.

## 9. Post-remediation owner validation closure

The pending wording in earlier sections is superseded by real owner evidence recorded after the p9.11.9 and p9.11.10 repairs:

- [`P9-11-F11B-OWNER-VALIDATION-RECHECK-3.md`](P9-11-F11B-OWNER-VALIDATION-RECHECK-3.md) — `PASS / bounded owner usefulness scope`;
- [`P9-11-F11A-OWNER-VALIDATION-ATTEMPT-2.md`](P9-11-F11A-OWNER-VALIDATION-ATTEMPT-2.md) — `PASS / bounded real template-to-document journey`.

F11B owner feedback accepts the portfolio as usable with only non-critical layout polish remaining. F11A owner feedback confirms real generation, download, open, formatting preservation and text substitution on p9.11.10. The Word trust/provenance prompt is retained as minor non-blocking friction and is not bypassed or misrepresented as a Workspace security failure without evidence.

F11 therefore achieves **bounded owner-usefulness PASS** while the Product Contract remains `Provisional 0.1.0`. This does not establish Stable Product Contract status, Active Platform Capability, canonical asset admission, customer Production/readiness, SLA/support or public/stable API/browser compatibility.

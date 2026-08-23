# P9.11 — RU-first + Arvectum brand UI dogfooding repair

Status: `Implementation Repair / Owner recheck pending`
Date: `2026-08-23`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` boundary preservation
Canonical action: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## 1. Real owner-session finding

The first real owner launch of Productive Workspace `p9.11.0` was completed on the selected Mac owner-operated runtime. The owner reported a successful exact runtime/Workspace launch and then immediately identified two real usability findings:

1. the interface must be fully Russian by default, with an optional `RU / EN` language switch;
2. the visual system must follow the Arvectum Brand Guide and the established Arvectum product-interface language rather than the generic pre-dogfooding shell styling.

These findings originate from real owner use. No synthetic dogfooding observation, fake session, fabricated endpoint or generated owner feedback was created for this repair.

## 2. Authority and architecture check

Checked before implementation:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 `Accepted 1.0.0`;
- RFC-0001 architecture boundary;
- ADR-0001 Productive Workspace browser/application topology — `Accepted`;
- canonical roadmap `2.95.0` — P9.11 remains the critical-path current action.

Disposition: this is a bounded and reversible P9.11 usability repair inside the already-Accepted SPA/BFF topology. It does not require a Constitution amendment, new/superseding RFC/ADR, Product Contract lifecycle transition or Platform Capability promotion.

## 3. Implemented repair

Workspace release is advanced from `p9.11.0` to `p9.11.1`; internal application contract remains `10`, classification remains `bounded-internal-provisional`, and `public_api` remains `false`.

### 3.1 Russian-first language behavior

- source `index.html` declares `lang=ru` before React boot;
- production `LanguageProvider` starts in `ru`;
- sidebar provides explicit `RU / EN` switching;
- the switch changes only browser presentation state and `document.documentElement.lang`;
- no `localStorage` or `sessionStorage` is used for the language preference;
- backend navigation/API identifiers and semantics are not forked by locale;
- frontend navigation labels are localized by stable existing navigation IDs;
- the main Workspace chrome and platform-owned surfaces provide RU/EN copy;
- product-owned composed surfaces retain their business data/semantics while their Workspace chrome is localized.

Source/evidence content returned by governed providers is not silently machine-translated. A source-owned title, reason, status, summary or evidence string may remain in its source language because changing that content would alter evidence/presentation semantics rather than merely localize UI chrome.

### 3.2 Arvectum visual system

Implementation was checked against Arvectum Brand Guide 1.1 and the existing Arvectum Proxy Launcher product UI as visual reference.

The new Workspace brand layer uses:

- Deep Navy `#041A33`;
- Graphite `#243446`;
- Mint `#43E5C5`;
- Mint Light `#7AF1DD`;
- Soft Gray `#F3F5F7`;
- White `#FFFFFF`;
- Manrope-preferred headings and Inter-preferred body text with system fallbacks only;
- mint as accent/action/focus color rather than a large text background;
- dark technological navigation, clean light content cards, restrained data-flow/dot motifs and consistent focus states.

No font files or remote branding dependencies are introduced. The browser remains compatible with ADR-0001 self-contained exact-release assets and current CSP.

## 4. Boundary preservation

The repair does not change:

- server-side session semantics;
- CSRF, Origin or Host enforcement;
- Organization/Actor resolution;
- Authorization, Data Governance or Organizational Authority;
- Governed Execution semantics;
- Product Contract lifecycle;
- Platform Capability lifecycle;
- product business schemas/workflows/rules;
- canonical Events/Knowledge semantics;
- public/stable API or browser compatibility promises.

A language selector and branded visual presentation therefore remain presentation behavior, not authority or canonical state.

## 5. Functional cross-review

### Iteration 1 — localization / authority / product boundary

Findings and disposition:

- locale must not fork backend API/navigation semantics — resolved by ID-based frontend localization;
- language preference must not introduce unnecessary browser persistence — resolved with in-memory state only;
- source/evidence text must not be silently translated as if the translation were source truth — preserved as source-provided content;
- product UI chrome may be localized but product business semantics remain product-owned.

Result: no remaining material localization/authority objection.

### Iteration 2 — brand / accessibility / build boundary

Brand repair was constrained to the approved visual language and existing SPA asset boundary. Mint remains an accent, accessible focus-visible states are explicit, and no remote font/assets or new runtime service are introduced.

PR CI run `32628011635` established before asset reconciliation:

- BFF security/context tests — `SUCCESS`;
- frontend typecheck — `SUCCESS`;
- frontend tests, including RU-default / RU-EN switch — `SUCCESS`;
- browser Web Storage rejection — `SUCCESS`;
- production build — `SUCCESS`;
- only committed production-asset reproducibility failed because `dist` still represented the previous source revision.

The exact deterministic production assets were then rebuilt by a bounded branch-only helper that itself re-ran typecheck/tests/Web-Storage guard before build. The helper committed the resulting `dist` and removed itself; no temporary helper remains in the final PR diff.

Result: source/build material objections resolved.

### Iteration 3 — integrated repository regression

Post-rebuild Productive Workspace CI was fully green, but Reference Python CI run `32628120353` found one material repository-regression issue in the historical P3.12 closure guard:

- generated Python artifact rejection — `SUCCESS`;
- `1301` reference tests executed;
- exactly one failure: `test_canonical_roadmap_preserves_m3_scope_as_later_phases_progress`;
- the failing assertion required the exact obsolete master-roadmap sentence `no Platform Capability is Active`.

The current canonical roadmap `2.95.0` still preserves the actual Phase 3 invariant — `CAP-001` through `CAP-004` remain `Incubating / Provisional` — and separately states that roadmap status cannot itself change lifecycle. The historical test class explicitly exists to preserve bounded M3 closure *without freezing later phases*. A permanent assertion that no future separately governed Platform Capability may ever become `Active` therefore exceeded the bounded P3.12 scope.

Remediation was narrow:

- removed only the stale global wording assertion;
- retained the master-roadmap assertion that `CAP-001` through `CAP-004` remain `Incubating / Provisional`;
- retained the lifecycle non-promotion assertion;
- retained the independent capability-catalog test that checks each exact CAP-001…CAP-004 row is `Incubating / Provisional` and not `Active`.

No runtime, governance, lifecycle or Productive Workspace gate was weakened.

Result: stale historical wording dependency reconciled; exact M3 capability disposition remains guarded.

### Iteration 4 — final clean implementation / CI

Final code/test head `2ca3b3c469ee9446659f02047cfc02d6a9626348` passed both independent PR CI contours:

- Productive Workspace CI `#151` / run `32628528106` — `SUCCESS`;
  - BFF security/context tests — `SUCCESS`;
  - frontend typecheck — `SUCCESS`;
  - frontend interaction tests, including RU-default and RU/EN switch — `SUCCESS`;
  - browser Web Storage rejection — `SUCCESS`;
  - production build — `SUCCESS`;
  - committed production-asset reproducibility — `SUCCESS`;
  - release-pinned production-asset boundary — `SUCCESS`;
- Reference Python CI `#382` / run `32628528165` — `SUCCESS`;
  - tracked generated-Python-artifact rejection — `SUCCESS`;
  - full architecture fitness suite — `SUCCESS` (`1301` tests).

No material implementation, architecture, authority, product-boundary, localization, accessibility, deterministic-build or repository-fitness objection remains after iteration 4. Functional cross-review stops below the maximum of 7.

Functional cross-review does not constitute RFC/ADR acceptance, lifecycle promotion, operational-readiness approval or P9.11 closure.

## 6. Closure disposition

The RU-first + Arvectum-brand repair is implementation-ready within the exact private owner-operated Workspace contour. It must not be treated as proof that the two real-use findings are resolved until the owner deploys `p9.11.1` and visually/operationally rechecks the interface.

P9.11 therefore remains `Current`. R32 remains locked until the wider real-session evidence and friction backlog satisfy the existing P9.11 exit criteria.

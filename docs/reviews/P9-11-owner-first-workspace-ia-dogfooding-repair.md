# P9.11 — Owner-first Productive Workspace IA dogfooding repair

Status: `Implementation Repair / Owner recheck pending`
Date: `2026-08-24`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` boundary preservation
Canonical action: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## 1. Real owner finding

`P9.11-F03 — Owner-first information architecture / obvious daily workflow`

The current Workspace was technically functional, Russian-first and branded, but the owner opening the real application could not determine where ordinary work starts, which section fits each job, where actionable work or product work lives, or the practical value of Workspace. Platform and governance taxonomy had too much first-level prominence and required the operator to learn architecture before receiving value.

This is real owner feedback. No synthetic acceptance evidence, owner session, product state or task was created.

## 2. Disposition and implementation

The repair is a bounded presentation and navigation change within the Accepted ADR-0001 SPA/BFF boundary:

- first-level navigation is `Сегодня / Работа / Информация / Arvectum AI / Система` with RU default and EN equivalents;
- Today opens with current attention and ordinary next steps;
- Work composes the existing My Work and Product Composition projections;
- Information reuses the existing Discovery BFF and security-scoped query boundary;
- System groups detailed organization, activity, governed-action and dogfooding surfaces;
- product pages lead with the available read-only context and move contract, dependency, provenance and release references into native collapsed technical details;
- legacy deep routes remain available and highlight their human-oriented group;
- Workspace release advances to `p9.11.2`; internal app contract advances from `10` to `11` because BFF-delivered navigation semantics changed materially.

## 3. Boundary preservation

No product workflow, product operation, product state or product deep link was invented. Tender Operator and Discount Parser remain read-only composed contexts with product-specific work retained by their products under P6.02/P6.06.

The repair does not change loopback scope, session handling, Host/Origin/CSRF validation, Organization/Actor resolution, Authorization, Data Governance, Organizational Authority, Governed Execution, external authority modes, Product Contract lifecycle, capability lifecycle, Event/Knowledge/Artifact semantics or the internal-only/public-API boundary.

## 4. Functional cross-review

1. Owner JTBD: Today makes the first decision and next destinations explicit; no architecture education leads the page.
2. Product and authority boundary: product contexts describe only verified read-only availability; no action or authority is implied.
3. Navigation, accessibility and localization: legacy routes retain their components and map to a visible group; semantic links/headings and RU/EN remain in use.
4. Release and verification: navigation contract, deterministic assets, focused frontend and BFF/security tests are updated and checked.

No functional cross-review is formal lifecycle promotion or owner acceptance.

## 5. Owner recheck

P9.11 remains `Current`; R32 remains locked and M9 remains open. The owner must reopen the deployed Workspace without instruction and independently identify where to start, attention, product work, information, Arvectum AI and technical administration.

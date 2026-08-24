# Arvectum OS — Parallel Workstreams after M9-alpha

Status: `Active planning / bounded parallel execution`
Version: `1.1.0`
Created: `2026-08-22`
Updated: `2026-08-24`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform`, `product_contract`, and `product_specific`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Current critical-path action: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## 1. Purpose

M9-alpha is achieved and P9.11 depends materially on real owner dogfooding. This permits bounded parallel work that does not falsify P9.11 evidence or silently alter shared authority/security/contracts.

Parallel work MUST NOT:

- bypass P9.11/R32/P9.12 closure criteria;
- infer Stable Product Contracts, Active Platform Capabilities, public/stable APIs, customer Production or SLA/support;
- move product business semantics into Arvectum OS without evidence and governance;
- create competing sources of truth for externally authoritative systems;
- conflate Authentication, Authorization, Organizational Authority, Data Governance and legal/contractual rights.

## 2. Lane A — Productive Workspace / real dogfooding

Status: `ACTIVE / critical path`.

Canonical sequence:

`P9.11 → R32 → P9.12 → M9`.

Current live blocker is `P9.11-F05`: exact runtime `fdde2cde...` with Workspace `p9.11.2` is installed, but the live loopback listener remains historical `p9.11.1`. PR #3 repair is under review and must not be merged until its material process-identity/evidence/test findings are closed.

Next sequence:

1. revise PR #3;
2. merge only after required regression/review evidence;
3. governed selected-Mac listener reconciliation/update;
4. verify `CURRENT_EXACT` p9.11.2;
5. owner recheck;
6. continue real daily-use friction capture and closure.

This lane alone controls the M9 closure clock.

## 3. Lane B — Russian-market integrations

Status: `INTERNALLY COMPLETE / operational continuation externally blocked`.

The internal design/admission block is complete through INT-B7:

| Item | Status |
|---|---:|
| INT-B1 — Integration portfolio baseline | Complete / PASS |
| INT-B2 — Domain-neutral connector boundary pattern | Complete / PASS |
| INT-B3 — 1С first-candidate design | Complete / PASS |
| INT-B4 — CRM designs | Complete / PASS |
| INT-B5 — СЭД/ECM/ЭДО design | Complete / PASS |
| INT-B6 — Integration security/reliability review | Complete / scoped PASS |
| INT-B7 — First real connector pilot admission package | Prepared / pilot NOT ADMITTED |

### INT-B7 prepared candidate

Preferred first candidate: bounded read-only `1С:ERP 2.5` procurement projection.

The package already defines:

- exact bounded outcome;
- read-only operation allowlist;
- endpoint/deployment intake;
- external authority and Organization binding;
- least-privilege integration principal/credential requirements without storing reusable secrets in canonical state;
- data purpose/classification/minimization/retention/deletion/portability intake;
- compatibility discovery;
- freshness/completeness/stale-state handling;
- authentication/authorization/network/source/pagination/schema/credential failure matrix;
- duplicate/reconciliation semantics;
- connector disable/termination proof;
- Product Contract gate;
- ADR/stable-boundary trigger disposition.

### Resume condition

Lane B has no further internally executable item until one exact real binding exists for a designed candidate:

- actual deployment/account/portal identity;
- actual reachable integration endpoint;
- real deployment/API/configuration metadata;
- dedicated least-privilege integration principal/credential binding;
- bounded real data scope and organizational purpose.

When available, populate and execute the existing INT-B7 package. Do not invent INT-B8 merely to keep the lane moving and do not synthesize endpoint/credential/pilot evidence.

All business writes/effects remain closed until separately governed: 1С posting/writes/payments, CRM writes/stage transitions, СЭД approval/workflow mutations, ЭДО signing/sending/annulment and arbitrary vendor API passthrough.

## 4. Lane C — Product ↔ Workspace operational composition

Status: `AVAILABLE / bounded on evidence`.

Permitted directions include:

- Tender Operator improvements driven by real owner friction;
- Discount Parser status/attention/product surfaces;
- Creative Test Agent product surfaces;
- Proxy Launcher only where Product Contract or product-local rules justify reliance.

Work must remain product-owned unless a shared domain-neutral responsibility is evidenced. New governed platform reliance requires the applicable Product Contract before use.

## 5. Lane D — Reliability / DX / technical debt

Status: `CONTINUOUS`.

Available work:

- CI stability/speed and deterministic builds;
- dependency/license/security updates with regression proof;
- selected-Mac update/rollback/recovery regression fixes;
- internal observability/operator diagnostics;
- documentation drift guards;
- removal of obsolete proof harnesses only when canonical evidence/recovery does not depend on them;
- performance work when real Workspace use provides evidence.

P9.11-F05 is currently also a Lane-D reliability concern, but because it blocks real dogfooding it remains owned by Lane A critical path until resolved.

## 6. Lane E — future external/customer readiness

Status: `DISCOVERY ONLY`.

May investigate:

- genuine second Organization candidate;
- customer deployment/hosting models;
- customer-controlled identity/authority/data governance;
- update/backup/support responsibility splits;
- Russian regulatory/commercial/certification/signing constraints.

No customer Production, multi-tenant implementation, SLA/support or general availability is admitted here.

## 7. Parallelism / merge rule

Parallel branches are permitted when they modify truly independent surfaces.

Before merge each branch must revalidate against current canonical `main`:

- Constitution and Accepted RFC/ADR;
- Product Contract boundaries;
- current roadmap/lane status;
- current tests/quality gates;
- active P9.11 findings and repairs.

Shared Workspace/BFF/session/security or connector-contract changes are not independent merely because they use a different Git branch; they require the applicable review/gate.

## 8. Current concurrency map

```text
                         ┌─ Lane A: P9.11 / F05 ─→ owner dogfooding ─→ R32 ─→ P9.12/M9
                         │
current canonical main ──┼─ Lane B: INT-B7 prepared ──[wait exact real endpoint]
                         │
                         ├─ Lane C: product ↔ Workspace composition on evidence
                         ├─ Lane D: reliability / DX / technical debt
                         └─ Lane E: future external/customer discovery only
```

## 9. Immediate actions

- **Lane A:** close PR #3 material findings, merge bounded repair, reconcile live Workspace to exact p9.11.2, owner recheck, continue real sessions.
- **Lane B:** no internal action until exact real endpoint/deployment/account exists; then resume INT-B7.
- **Lane C:** take only real dogfooding-driven or explicitly contracted product work.
- **Lane D:** continue evidence-backed reliability/quality work that does not conflict with F05 repair.
- **Lane E:** discovery only.

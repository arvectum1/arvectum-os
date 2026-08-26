# R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate

Status: `In Progress / exact-head gate pending`
Date: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `platform + governance`
Canonical roadmap action: `R32`
Base canonical main at review start: `6c057d34f330f78140de6e5816344b847ed45ca8`
Working branch: `work/r32-m9-code-health-gate`

## 1. Authority checked

- Constitution `1.2.0` — `Ratified`, frozen.
- RFC-0001 through RFC-0008 — `Accepted 1.0.0` in the canonical RFC index.
- ADR-0001 — `Productive Workspace Browser Application Topology`, `Accepted 2026-08-21`.
- Arvectum Engineering Standard AES-001 `0.1.0` — bootstrap engineering-process baseline currently referenced by the canonical roadmap.
- Phase 9 roadmap `1.13.23` and canonical ROADMAP `2.95.26` — `R32 = Current`; `P9.12` remains pending.

No lower-authority source is used to weaken Constitution/RFC/ADR requirements.

## 2. Gate interpretation

R32 is the pre-M9-closure L4/code-health hardening gate. Applicable closure evidence includes repository/CI/release-candidate consistency, mandatory tests, dependency consistency, reproducible build/artifact evidence, security/authority fail-closed behavior, ADR compliance, and explicit disposition of material review findings.

The Engineering Standard does not establish a numeric cyclomatic-complexity hard fail. Complexity findings produced by the R32 audit are review signals: material hotspots must be simplified when the change is bounded and risk-reducing, or explicitly dispositioned when further refactoring would add churn without demonstrated value. The no-bureaucracy rule prohibits architecture or mass refactoring solely for uniformity or metric cosmetics.

## 3. Baseline audit evidence

R32 introduced a deterministic Workspace Python code-health inventory and a permanent read-only CI gate:

- `reference/python/tools/workspace_code_health.py`;
- `.github/workflows/r32-code-health-audit.yml`.

Initial inventory found:

- zero Workspace Python modules above the audit's module-size review threshold;
- nine functions above the audit's complexity review threshold.

The branch then performed bounded behavior-preserving decomposition in:

- `workspace_app/config.py` — separated configuration validation concerns;
- `workspace_app/assets.py` — separated frontend asset verification concerns;
- `workspace_app/company_materials.py` — separated actual-content validation helpers while preserving fail-closed media/OOXML validation.

No public/stable API, Product Contract lifecycle, Platform Capability lifecycle, authority model, canonical admission rule, deployment topology, or browser trust-boundary expansion is introduced.

## 4. Prior full gate evidence

R32 M9 Code Health Audit run `33019225480` on branch head `150cdf46177d786d711b418bd5419c707c8baf09` completed `SUCCESS` before the final `company_materials.py` decomposition.

That run included:

- Python 3.12 locked dependency installation;
- Workspace compile and full Workspace test suite;
- `pip check`;
- `pip-audit --strict`;
- deterministic Workspace code-health inventory;
- Node 24 exact frontend dependency install;
- TypeScript typecheck;
- frontend tests;
- Web Storage guard;
- `npm audit --audit-level=high`;
- production frontend build and committed-dist reproducibility;
- full Reference Python suite.

Supply-chain checks were PASS at that reviewed state.

The subsequent bounded material-validation refactor was separately regression-tested and committed as `fa2fc070b338bab214ceea8f5701e50a6d03f61a`. Because that final commit was authored by GitHub Actions, the ordinary push-triggered R32 gate did not run on that exact SHA. Therefore R32 is not yet PASS at publication of this review revision.

## 5. Exact-head acceptance gate

Before R32 can close, the final review head must demonstrate:

1. permanent R32 workflow remains read-only and contains no temporary write-enabled materialization/refactor helper;
2. full Workspace backend tests PASS;
3. full Workspace frontend typecheck/tests/Web Storage guard/build/reproducibility PASS;
4. `pip check`, `pip-audit --strict`, and `npm audit --audit-level=high` PASS;
5. full Reference Python suite PASS;
6. code-health inventory is reviewed and every remaining high-complexity signal receives a materiality disposition;
7. ADR-0001 release/trust/read-model/product-boundary obligations remain satisfied;
8. no material functional/security/governance regression is found by focused cross-review;
9. canonical PR/merge and read-after-write evidence exist;
10. roadmap advances only after the merge evidence supports R32 closure.

## 6. Functional cross-review

This is a new R32 milestone review, not an extension of the completed F11 review.

### Iteration 1 / 7 — baseline and bounded refactor review

Reviewed functions:

- maintainability / unnecessary branching;
- security and fail-closed validation;
- ADR-0001 frontend/BFF exact-release boundary;
- product/platform and Product Contract boundaries;
- dependency and supply-chain posture;
- build/reproducibility/test coverage.

Disposition:

- configuration and asset-verification hotspots were suitable for bounded decomposition and were refactored;
- material-content validation was suitable for bounded decomposition and was refactored with focused regressions;
- numeric complexity alone is not treated as a reason for broad rewrites;
- final exact-head CI and residual-hotspot materiality review remain required.

Result: `Continue — exact-head evidence pending`.

## 7. Lifecycle and closure limits

R32 does not by itself:

- close Phase 9 / M9;
- start or close `P9.12` before R32 canonical closure;
- promote F11 Product Contract beyond `Provisional 0.1.0`;
- promote any Platform Capability lifecycle;
- create public/stable API/browser/SDK/support commitments;
- grant AI Authorization or Organizational Authority;
- admit staged Company materials or generated transient outputs into canonical state.

## 8. Current disposition

`IN PROGRESS`.

Next evidence: run the complete R32 gate on the exact final branch head created by this review commit, inspect residual code-health signals, perform focused cross-review, then either make bounded corrective changes and rerun or proceed to PR when no material objections remain.

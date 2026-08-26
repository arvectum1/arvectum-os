# R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate

Status: `PR-ready / exact-head R32 audit PASS / repository CI pending`
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

## 3. R32 implementation

R32 introduces a deterministic Workspace Python code-health inventory and a permanent read-only CI gate:

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

## 4. Exact-head R32 audit evidence

Human-authored review head `c07e9b5660fd143f3b31fb8cb2e19a294fb00d60` triggered R32 M9 Code Health Audit run `33022403675`.

Result: `SUCCESS`.

Jobs:

- Workspace static/code-health inventory — PASS;
- Python dependency vulnerability baseline — PASS;
- Frontend dependency vulnerability baseline — PASS.

Supply-chain / consistency evidence:

- Python 3.12 setup and Workspace compilation — PASS;
- exact locked Workspace dependency installation — PASS;
- `pip check` — PASS;
- `pip-audit --strict` over the locked Python dependency set — PASS;
- Node 24 exact frontend dependency installation — PASS;
- `npm audit --audit-level=high` — PASS.

Exact-head code-health inventory:

- Python modules scanned: `33`;
- Python functions/methods scanned: `439`;
- Python test modules: `14`;
- frontend source/style modules scanned: `53`;
- frontend test modules: `15`;
- complexity `>15`: `6` reviewed signals, reduced from the initial `9`;
- modules `>800` lines: `0`.

The R32 audit is deliberately not a replacement for Productive Workspace CI or the full Reference Python suite. Those repository-level checks are required on the final PR head before merge.

## 5. Residual high-signal disposition

The six remaining `>15` complexity signals were inspected individually against their security/authority role, line count, existing tests, and practical refactor value.

### `RuntimeProductCompositionProvider._discount` — complexity 27 / 62 lines

Disposition: `reviewed non-material signal / refactor-on-touch`.

The branching is predominantly independent fail-closed validation of retained P7.08 reconstruction evidence: directory/symlink checks, exact report/receipt sidecars, schema/status checks, continuity/Product Contract checks, containment checks, and external-effect non-replay checks. The function is read-only and rejects incomplete or inconsistent evidence. No material correctness, authority, or security defect was found. Splitting the checks solely to lower the metric is not justified in R32.

### `company_portfolio._normalize` — complexity 25 / 81 lines

Disposition: `reviewed non-material signal / adapter extraction on next substantive portfolio change`.

The function is an explicit adapter dispatcher for registered Company/Tender/Discount/Proxy/Creative/OS roadmap/status shapes. It does not infer canonical truth from model memory and its adapter behavior has focused regression coverage from F11. The high score reflects mutually exclusive adapter branches rather than deeply nested stateful logic. Future new adapter behavior should be extracted instead of extending this dispatcher indefinitely; no broad rewrite is required for M9 closure.

### `VerifiedRuntimeCompanyPortfolioProvider._cache_compatible` — complexity 24 / 36 lines

Disposition: `reviewed non-material signal / preserve concentrated fail-closed guards`.

The score comes from short, independent compatibility/provenance checks over non-canonical cached projections. Repository/path/adapter/exact SHA/content SHA and reconciliation state must all fail closed. This function is security/truthfulness-sensitive and was directly exercised by the F11D-03 cache regressions and real owner navigation evidence. Refactoring solely to reduce the score risks weakening an intentionally auditable guard sequence.

### `RuntimeCompanyPortfolioProvider._load_registry` — complexity 22 / 43 lines

Disposition: `reviewed non-material signal / preserve bounded registry validation`.

The branching validates schema, authority/projects shape, allowed execution targets, repository/path formats, repository/path consistency, and unique project identity. These are independent fail-closed validation rules for a small product-owned registry. No material defect was identified; extraction is appropriate only if the registry contract grows materially.

### `RuntimeCopilotProvider.answer` — complexity 17 / 84 lines

Disposition: `reviewed non-material signal / no R32 rewrite`.

The remaining branches express source availability, uncertainty, optional model synthesis, model failure, and no-evidence behavior. R31 already reviewed the Copilot's source-grounded, uncertainty-aware and authority-safe boundary. R32 found no regression or new authority path. A structural rewrite without changed behavior would create unnecessary AI-safety regression risk.

### `RuntimeCopilotProvider._evidence` — complexity 16 / 80 lines

Disposition: `reviewed non-material signal / no R32 rewrite`.

The branches isolate authorized discovery evidence from product-owned retained context, tolerate one read-side source becoming unavailable without manufacturing evidence, preserve limitations, and rank only inspectable evidence. This is intentional bounded orchestration. No material security/authority finding was found.

### Residual-signal conclusion

All six high signals are therefore **reviewed and explicitly dispositioned as non-material for R32**. They remain visible through the permanent inventory and are not suppressed or allowlisted away. Future substantive changes touching these areas must reconsider extraction/refactoring rather than blindly adding branches.

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
- final exact-head CI and residual-hotspot materiality review remained required.

Result: `Continue — exact-head evidence pending`.

### Iteration 2 / 7 — exact-head evidence and residual-hotspot review

Evidence reviewed:

- R32 audit run `33022403675` — SUCCESS;
- dependency consistency and vulnerability audits — PASS;
- complexity inventory after bounded refactors — six remaining high signals / zero oversized modules;
- exact implementations of all six high-signal functions;
- ADR-0001 read-model, product-composition, Copilot authority and exact-release boundaries;
- F11/R31 regression evidence applicable to portfolio cache and Copilot behavior.

Material objections:

- none from the six residual high signals after explicit disposition;
- repository-level Productive Workspace CI and full Reference Python CI still required on final PR head;
- no release-id bump is required for this bounded internal refactor because it introduces no browser/BFF contract or user-visible behavior change and does not rebuild or alter frontend assets. Exact repository source identity remains the commit SHA; `p9.11.10` app contract `11` remains compatible. A later release-bearing change must still move compatible SPA+BFF assets together under ADR-0001/P7.06.

Result: `PASS subject to final PR repository CI`.

No third review iteration is required unless PR CI or review surfaces a new material objection.

## 7. PR acceptance gate

Before R32 can close:

1. permanent R32 workflow remains read-only and no temporary write-enabled refactor/materialization helper is present in final diff;
2. Productive Workspace backend/full security-context tests PASS on the final PR head;
3. frontend typecheck/tests/Web Storage guard/build/reproducibility PASS on the final PR head;
4. full Reference Python suite PASS on the final PR head;
5. PR diff contains only bounded R32 audit/refactor/review changes;
6. no unresolved material review objection remains;
7. canonical merge and read-after-write evidence exist;
8. GitVerse mirror is verified;
9. roadmap advances `R32` only after merge evidence exists.

## 8. Lifecycle and closure limits

R32 does not by itself:

- close Phase 9 / M9;
- close `P9.12`;
- promote F11 Product Contract beyond `Provisional 0.1.0`;
- promote any Platform Capability lifecycle;
- create public/stable API/browser/SDK/support commitments;
- grant AI Authorization or Organizational Authority;
- admit staged Company materials or generated transient outputs into canonical state.

## 9. Current disposition

`PR-ready / exact-head R32 audit PASS / repository CI pending`.

Next action: open the R32 PR against canonical `main`, run the ordinary Productive Workspace and Reference Python checks on the exact PR head, resolve any material objection, then merge and synchronize canonical roadmap state to `R32 = Complete / PASS` and `P9.12 = Current` without closing M9 itself.

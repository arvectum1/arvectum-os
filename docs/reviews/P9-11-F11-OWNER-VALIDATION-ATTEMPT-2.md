# P9.11-F11 — Real owner validation attempt 2

Status: `FAIL / remediation technically verified / deploy + owner recheck pending`
Date: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `platform + product_contract + product_specific`
Product Contract: `P9.11-F11 Provisional 0.1.0`
Observed live Workspace: `p9.11.8` / app contract `11`
Target remediation release: `p9.11.9` / app contract `11`
Predecessor evidence: [`P9-11-F11-OWNER-VALIDATION-ATTEMPT-1.md`](P9-11-F11-OWNER-VALIDATION-ATTEMPT-1.md)

## 1. Real owner evidence

After the p9.11.8 usability remediation was governed-deployed, the owner reported:

> `показывало сначала дорожную карту в уже приемлемом виде ушел  на другую вкладку, вернулся, нихуя нет, везде "информация недоступна"`

Result: **F11 owner validation attempt 2 = FAIL**.

The p9.11.8 visual/IA repair is materially better when source-backed data is present, but ordinary navigation is not reliable enough for daily use because returning to the page can erase the useful projection.

## 2. Material finding F11D-03 — ordinary navigation re-fetches external sources and collapses to empty unavailable cards

Repository inspection establishes the implementation defect:

1. `CompanyProjects` mounts by calling `loadCompanyPortfolio()` on every visit;
2. `/api/app/v1/company/portfolio` invokes the runtime portfolio provider on every request;
3. the provider performs a new GitHub `commits/main` request and a second exact-content request for every reconciled project source;
4. any transient GitHub API, rate-limit, timeout or network failure is converted into `state=unavailable` with an empty roadmap projection;
5. no last-known-good read-model cache is used even though F11 Product Contract 0.1.0 explicitly permits a local non-canonical dashboard cache and requires the UI to distinguish current, stale cached and unavailable source states.

This means ordinary UI navigation is accidentally coupled to external source availability at that exact moment. It violates the intended Productive Workspace read-model behavior and is not acceptable for F11B owner usefulness.

## 3. Higher-authority / contract check

No Product Contract expansion is required.

The existing Provisional F11 contract already declares:

- product roadmaps/status remain `External Reference` authority;
- the dashboard is a derived non-canonical projection;
- a local dashboard cache is non-canonical, deletable and rebuildable and must never silently replace source truth;
- the UI must distinguish current source-backed information, stale cached information, unavailable source, unsupported format, reconciliation-required and conflict states;
- absence of source evidence must not be filled from chat/model memory.

ADR-0001 also explicitly admits rebuildable non-authoritative read models/projections and requires freshness limitations to be surfaced truthfully.

Therefore the bounded repair is to implement the declared read-model behavior, not to create `Governed Replica` authority.

## 4. Bounded remediation

Workspace p9.11.9 repair scope:

1. persist the last fully successful normalized F11B projection under the owner-local runtime root;
2. bind cache files to the current Organization and reject cross-Organization cache reuse;
3. preserve exact repository/path/commit SHA/content SHA-256/fetched-at/adapter evidence;
4. use a recent last-known-good cache for ordinary page revisits instead of re-fetching GitHub on every mount;
5. keep the cache explicitly non-canonical and rebuildable;
6. add an explicit owner action `Обновить из источников` which performs a live canonical-source refresh attempt;
7. when explicit/automatic refresh fails and a valid prior projection exists, keep the prior roadmap fields visible and mark the card `stale-cache` rather than emptying it;
8. when neither source nor valid cache exists, continue to show `unavailable` and do not invent status;
9. retain `reconciliation-required` where no admitted source exists;
10. preserve read-only behavior, no roadmap write, no remote execution, no authority grant and no chat/model-memory substitution.

A recent cache window is an implementation optimization only. It does not establish a freshness SLA or make cached content authoritative.

## 5. Acceptance criteria for remediation

Technical PASS requires at minimum:

- first successful source fetch writes owner-local last-known-good cache;
- a subsequent ordinary `/projects` revisit within the bounded cache window does not require another GitHub read;
- exact roadmap fields and exact source provenance remain visible from cache;
- explicit refresh attempts live source retrieval;
- failed explicit refresh with prior valid cache returns `stale-cache`, retains roadmap fields and source SHA/content hash/fetched-at evidence;
- cache is Organization-scoped and cannot cross access context;
- failed refresh with no valid cache remains `unavailable`;
- frontend keeps the previously visible project content on screen while an explicit refresh is in flight;
- frontend renders stale-cache truthfully rather than global `Портфель проектов недоступен`;
- normal BFF/session/release guards remain intact;
- CI and release-pinned production assets pass.

## 6. Governance disposition

- F11 Product Contract — `Provisional 0.1.0` unchanged;
- F11A — remediation deployed from attempt #1 / owner validation still pending;
- F11B — **owner validation attempt #2 FAIL / remediation technically verified / deploy + owner recheck pending**;
- canonical roadmap sources — remain external authority;
- local portfolio cache — non-canonical read model only;
- P9.11 — `Current`;
- R32 — `Locked`;
- canonical asset admission — unavailable;
- no Stable Product Contract or Active Platform Capability claim.

The prior F11 functional cross-review reached the seven-iteration ceiling. This is a new real-owner defect finding and bounded implementation repair, not an eighth formal functional cross-review iteration. A focused defect review may still check whether the repair introduces material security, authority, provenance or reliability regressions.

## 7. Implementation evidence

The repair branch implements the bounded design above and advances Workspace to `p9.11.9` / app contract `11`.

Focused implementation safeguards include:

- cache path is Organization-derived and does not use browser-controlled storage paths;
- cache files/directories are owner-local and permission-hardened; symlink cache directories/targets are rejected;
- cache compatibility is checked against the current explicit project registry, repository/path/adapter and exact SHA/hash shapes before reuse;
- a cache write failure cannot hide a successfully verified live External Reference projection because cache persistence is only an availability optimization;
- ordinary revisit uses a bounded recent cache window, while explicit refresh forces source retrieval;
- source failure with prior compatible cache preserves exact prior provenance and marks the card `stale-cache`;
- source failure without compatible cache remains `unavailable`;
- frontend preserves visible project data while explicit refresh is in flight;
- regression tests cover no-refetch ordinary revisit, stale fallback, Organization isolation, cache-write failure, symlink rejection and frontend stale-refresh behavior;
- a one-shot CI materialization produced the `p9.11.9` production `dist` and restored `.github/workflows/workspace-app-ci.yml` to its ordinary read-only form in the same branch update.

## 8. Technical verification

Exact implementation/release head before this evidence-only update: `5bf9adbb7f006ca6e7f90c96e84c83f7df651622`.

- Productive Workspace CI `33005070564`: `PASS`;
- Reference Python CI `33005070555`: `PASS`;
- BFF security/context suite: PASS;
- frontend typecheck/tests/Web Storage guard: PASS;
- production build and committed `dist` reproducibility: PASS;
- release-pinned production asset verification: PASS;
- temporary write-enabled materialization workflow is absent from the final PR diff; ordinary workflow is restored to `contents: read`.

This establishes technical readiness only. The p9.11.9 repair still requires governed deployment to the selected Mac and a new real owner recheck. F11 owner PASS is not established.

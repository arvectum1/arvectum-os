# P9.11 — Real daily-use dogfooding + friction/backlog closure

Status: `Complete / PASS — real owner sessions and material friction disposition evidenced`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance` boundaries
Predecessor: `R31 — Complete / PASS`
Current canonical action: `R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate`

## Canonical baseline checked

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
- direct checks: RFC-0001, RFC-0003, RFC-0004, RFC-0006 and RFC-0007;
- ADR-0001 — `Accepted`, Productive Workspace SPA + same-origin BFF topology;
- canonical master roadmap `2.86.0` and Phase 9 roadmap `1.13.0` before this implementation milestone.

No higher-authority conflict was found. No Constitution amendment, new RFC/ADR, Product Contract lifecycle transition or Platform Capability promotion is required for this bounded dogfooding mechanism.

## Historical implementation-readiness state: why P9.11 was not Complete / PASS yet

The Phase 9 M9 gate requires **real owner working sessions completed primarily through the Productive Workspace** and disposition of recurring usability friction discovered by those sessions.

Repository tests, synthetic scenarios, generated fixtures or a reviewer's simulated clicks cannot substitute for that operational evidence. This implementation therefore prepares and validates the capture/disposition mechanism but intentionally does **not** fabricate owner-session evidence and does not advance the canonical next action to R32.

## Implemented dogfooding contour

Workspace release `p9.11.0`, internal application contract `10`, adds a private `Dogfooding` surface and same-origin BFF endpoints for real-use friction capture.

The mechanism is deliberately subordinate and non-authoritative:

- each entry is a bounded **Observation**, not an RFC-0006 canonical Event;
- accumulation or repetition does not promote an entry to RFC-0007 Organizational Memory, Knowledge Candidate or validated Knowledge;
- capture and disposition do not create Authentication, Authorization, Organizational Authority, Consequential Approval or legal/contractual right;
- Organization and Actor are resolved server-side from current authorized context and are not browser-selectable fields;
- current access is revalidated for reads and writes;
- unsafe writes remain same-origin, release-pinned and CSRF-protected;
- no product-specific schema, workflow, decision rule or hidden product state is moved into the platform;
- `public_api` remains `false` and the application contract remains internal and release-scoped.

### Bounded retention and minimization

The observation store is local to the configured Workspace runtime root and is bounded to:

- retention: `90 days`;
- capacity: latest `200` retained entries;
- summary: maximum `240` characters;
- supporting detail: maximum `600` characters;
- disposition rationale: maximum `500` characters.

Expired entries are physically pruned on access. Scope keys are derived server-side and are not returned to the browser. The UI explicitly instructs the owner not to paste secrets or unnecessary protected content.

### Classification

Each real observation is classified by:

1. journey: `J1` through `J6` or `other`;
2. Workspace surface;
3. severity: `blocker | material | minor`;
4. boundary: `workspace-usability | product-specific | governance | security-authority`.

This preserves the product/platform boundary: a product-specific gap can be routed to a product-owned backlog without promoting its semantics into shared platform behavior, while governance/security findings remain in the governance path.

### Closure-blocking semantics

The derived backlog exposes `closure_blocking` as the count of retained blocker/material observations that are either:

- still `open`; or
- dispositioned as `deferred`.

A blocker cannot be deferred or routed out of closure. It may leave closure-blocking state only after factual `resolved` + ordinary-journey recheck or `not-reproducible` + recheck. A security/authority finding cannot be deferred or routed to a product backlog. Product routing is available only for non-blocker `product-specific` observations; governance routing is available only for applicable non-blocker `governance` or `security-authority` observations. The UI narrows choices accordingly, and the BFF/store enforce the same rules independently so UI behavior is not the security boundary.

There is deliberately no `accept risk` disposition in this mechanism. A consequential risk/authority exception, if ever justified, must use the applicable canonical governance/decision path rather than a dogfooding backlog shortcut.

## Real owner-session operating protocol

P9.11 closure evidence must come from actual ordinary owner work, not a scripted acceptance-only exercise.

For each real working session:

1. use the Productive Workspace as the primary interface for the work being performed;
2. use the relevant ordinary journey J1–J6 rather than a dedicated test-only path;
3. when friction materially affects the work, record the smallest sufficient observation in `Dogfooding`;
4. classify whether the issue belongs to Workspace usability, a product-owned boundary, governance, or security/authority;
5. repair recurring/material Workspace defects without weakening security, privacy, authority or fail-closed behavior;
6. re-run the ordinary journey after a repair before using `resolved`;
7. route product-specific or governance findings to the correct owned work with an explicit rationale/reference in canonical closure evidence;
8. keep material deferred items visible as closure-blocking until they are actually resolved/routed/reclassified on evidence.

The P9.11 closure review may proceed only when real owner-session evidence exists and the retained friction backlog has no unresolved material closure blockers under the canonical Phase 9 exit criteria.

## Functional cross-review

### Iteration 1 — architecture, security, retention and authority

Material objections found:

1. the first store version filtered expired entries from the projection but did not physically delete them from the local file;
2. the first disposition model exposed choices that could make blocker/security findings look closed through an inappropriate route.

Remediation:

- retention now physically prunes expired entries on access and fails closed on malformed retained-state timestamps/data;
- persistence errors are surfaced rather than silently dropping state;
- `closure_blocking` explicitly keeps open/deferred material friction visible;
- blockers cannot be deferred;
- security/authority findings cannot be deferred or routed to product work;
- routing is classification-constrained in both backend and UI.

Result: material objections addressed.

### Iteration 2 — integrated source/diff review

Reviewed the complete branch against R31 head after remediation:

- dogfooding state remains a bounded non-canonical Observation mechanism;
- current Organization/Actor scope remains server-resolved;
- browser-supplied scope headers/query parameters do not select scope;
- writes remain release/origin/CSRF protected;
- no new canonical Kernel primitive or Product Contract lifecycle promise appears;
- generated production assets are deterministic and the temporary asset-build helper is removed from the resulting implementation branch;
- tests cover scope minimization, retention pruning, closed taxonomy, authority-safe routing and closure-blocking semantics.

Result: no material architecture/product-boundary objection found before independent PR CI.

### Iteration 3 — closure semantics, deterministic assets and independent CI

One additional material closure-semantics objection was found: a `blocker` could still be dispositioned as `routed-governance`, which could remove it from the closure-blocking count before the blocking condition was factually resolved or shown not reproducible.

Remediation:

- blocker disposition is now restricted to `resolved` or `not-reproducible`;
- both outcomes require an explicit rationale and the operating protocol requires ordinary-journey recheck;
- non-blocker product/governance routing remains classification-constrained;
- UI and backend independently enforce the same allowed-disposition set.

An intermediate Productive Workspace CI attempt after this source change failed only at the committed-production-asset reproducibility gate because `dist` still represented the previous source revision. The deterministic production assets were rebuilt and committed; no test/security failure was masked.

Final clean implementation/reconciliation head `95aa06463f69489edcae204bdbcd6ea7013e9fdb` then passed:

- Productive Workspace CI run `32561762336` — `SUCCESS`;
  - BFF security and context tests — `SUCCESS`;
  - frontend typecheck — `SUCCESS`;
  - frontend interaction tests — `SUCCESS`;
  - browser Web Storage rejection gate — `SUCCESS`;
  - production build — `SUCCESS`;
  - committed production-asset reproducibility — `SUCCESS`;
  - release-pinned production-asset boundary — `SUCCESS`;
- Reference Python CI run `32561762312` — `SUCCESS`;
  - tracked Python generated-artifact rejection — `SUCCESS`;
  - architecture fitness suite — `SUCCESS`.

Post-CI repository-hygiene commits are documentation/workflow cleanup only and do not alter the tested P9.11 implementation. Temporary reconciliation helpers are not intended to survive merge.

Result: no remaining material implementation objection. Functional cross-review stops after 3 iterations of the allowed maximum 7.

Functional cross-review is implementation evidence only; it is not RFC/ADR acceptance, Product Contract promotion, Platform Capability promotion, operational-readiness approval or delegated Organizational Authority.

## P9.11 implementation-readiness result

The bounded capture/disposition mechanism is implementation-ready within the exact private `Local / Persistent Internal / owner-operated` Workspace scope. Master roadmap `2.87.0` records this state while keeping P9.11 as the current canonical action.

This result does **not** establish P9.11 closure, M9 closure, customer Production/readiness, a public/stable API/browser contract, SLA/support/certification, Stable Product Contracts or Active Platform Capabilities.

## Historical closure conditions that remained pending at implementation-readiness time

The following are intentionally **not** asserted by this implementation milestone:

- real owner working sessions have occurred primarily through Workspace;
- real recurring friction has been observed and fully dispositioned;
- `closure_blocking == 0` for the real retained working-session backlog;
- all routed product/governance findings have canonical downstream references;
- M9 is satisfied;
- R32 is the current canonical next action.

Those conditions were intentionally not asserted at implementation-readiness time. They are superseded by the real-owner closure evidence below.

## P9.11 closure evidence — 2026-08-27

P9.11 now has sufficient real owner evidence for bounded closure:

1. multiple real owner sessions occurred primarily through the live Productive Workspace rather than synthetic scenarios;
2. material usability findings F07–F11 were repaired and rechecked on ordinary owner journeys;
3. F11B project-portfolio stability/usefulness reached bounded owner PASS after the p9.11.9 cache-backed repair;
4. F11A real Company-material/template → generated DOCX → protected download → Word-open journey reached bounded owner PASS on p9.11.10;
5. remaining owner observations are minor/non-closure-blocking: future layout polish and the Word downloaded-file trust/provenance prompt;
6. no unresolved blocker/material finding remains in the evidenced P9.11 closure path;
7. the deferred F08 real task-detail → governed-action journey remains eligible for natural recheck when a genuine actionable task exists, without manufacturing a synthetic task and without reopening the resolved false-task defect;
8. security, authority, provenance and Product Contract boundaries remain fail-closed and unchanged.

Therefore **P9.11 = Complete / PASS** in its exact `Local / Persistent Internal / owner-operated` scope. The next canonical action is **R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate**.

This closure does not establish M9/P9.12 closure, customer Production/readiness, Stable Product Contracts, Active Platform Capabilities, public/stable APIs/browser support, SLA/support or any Organizational Authority delegation.

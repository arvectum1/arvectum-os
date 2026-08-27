# R33 — Asset / Product Contract / Authority Boundary Review

Status: `Complete / PASS — 6 iterations; mandatory P10.03 implementation constraints recorded`
Date: `2026-08-27`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`, `product_specific` and `governance`
Roadmap gate: `R33 — Asset / Product Contract / Authority Boundary Review`
Review subject: [`P10.02 — Arvectum Company ↔ Productive Workspace Product Contract — Provisional 0.2.0`](../contracts/P10-02-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.2.0.md)
Normative Product Contract substance: Draft `0.2.0` blob `a92c1d1aac54d565d3d32ce746925620c9d1fd12`
Predecessor authority baseline: [`P10.01 — Asset/admission + real-work authority matrix`](P10-01-asset-admission-real-work-authority-matrix.md) — `Complete / PASS`
Product Contract closure: [`P10.02 — Product Contract Publication Closure Review`](P10-02-product-contract-publication-closure.md) — `Complete / PASS`
Successor if PASS: `P10.03 — Domain-neutral organizational-asset admission execution path`

## 1. Purpose

R33 is the blocking architecture/governance gate between the lifecycle-current Company Workspace Product Contract `Provisional 0.2.0` and implementation of P10.03.

The review determines whether the approved Product Contract and P10.01 authority model can safely authorize bounded implementation without:

- leaking Company taxonomy or product business rules into shared Kernel/platform semantics;
- conflating staged receipt, canonical admission, asset designation or generated-output promotion;
- creating hidden Authorization or Organizational Authority through browser state, technical access, Product Contract possession or AI output;
- creating competing authority for external sources;
- weakening rights, classification, purpose, minimization, retention/deletion or portability requirements;
- creating a hidden product-action or cross-product execution authority;
- turning internal browser/BFF or operation names into a stable/public platform surface;
- overclaiming Product Contract, Platform Capability, Production or conformance maturity.

Maximum functional cross-review iterations: 7. Completed: 6.

R33 reviews architecture and contract boundaries. It does not prove P10.03 implementation, execute a real asset admission, promote generated output, approve a downstream product side effect, or promote any lifecycle state.

## 2. Canonical authority checked

R33 was checked against current canonical `main` at merge baseline `44a0eca323ed774d20ec12645438be0c41929185` and the following authority chain:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 `1.0.0` are `Accepted`;
3. RFC-0001 — domain-neutral platform responsibility, explicit authority modes, Governed Organizational Asset designation, Transient Output boundary, mandatory Governed Execution for consequential canonical change, Product Contract rules, security/portability/AI constraints and residual owner authority;
4. RFC-0002 — finalized five-primitive Kernel metamodel, Organizational Asset as governed designation rather than sixth primitive, immutable canonical versions, exact-version pinning, external authority preservation, projection non-authority and migration honesty;
5. RFC-0003 — separation of Identity, Authentication, Authorization, Organizational Authority and Data Governance; deny by default; least privilege; explicit Organization scope; purpose/minimization/retention/deletion/portability; fail-closed uncertainty; AI retrieval/authority constraints;
6. RFC-0004 — mandatory explicit Product Contract before governed platform reliance, Product Contract lifecycle, lifecycle separation from Platform Capability, no hidden coupling, external authority and organization-boundary preservation;
7. RFC-0005 — exact effective Product Contract/workflow/input pinning, independent gate evaluation, side-effect classes, Governed Execution for canonical mutation, AI authority limits, idempotency/retry/uncertainty/reconciliation;
8. RFC-0006 — append-only Event/provenance semantics, transport distinct from admission, telemetry/projections non-canonical by default, replay cannot repeat consequential effects without new authorization;
9. RFC-0007 — documents, summaries, repeated use and AI output do not become validated Knowledge; retrieval/derived state remains governed and non-authoritative by default;
10. RFC-0008 — Document/Artifact roles above Kernel, receipt/generation distinct from canonical admission, generated artifacts `TransientOutput` by default, explicit governed promotion, exact version/content reliance and portability;
11. ADR-0001 — browser/BFF is internal and release-scoped, not authority or canonical state; protected reads and consequential commands are server-side scoped/gated; projections remain non-authoritative;
12. [`Platform Capability Catalog`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md) — CAP-001 remains `Incubating / Provisional`, not `Active`;
13. [`Phase 3 Provisional Capability Contracts`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md) — CAP-001 owns only domain-neutral Document/Artifact identity/version/admission/derivation/exact-version mechanics and reopens the ADR gate before material new durable implementation choices;
14. Decision Authority Policy `0.2.1` — `Proposed`, non-binding; residual Organizational Authority remains with owner under Accepted rules;
15. P10.01 authority matrix — exact first-slice asset classes, authority modes, gate separation, generated-output lifecycle and real Action Request source classes;
16. P10.02 exact approved Draft blob `a92c1d1aac54d565d3d32ce746925620c9d1fd12`, independent owner Approval Record, lifecycle-current Provisional publication and closure evidence;
17. canonical master roadmap `2.97.1` and Phase 10 roadmap `1.0.1`, where R33 is the current blocking gate and P10.03 is blocked until R33 PASS.

No higher-authority source requires a new Kernel primitive, a mandatory physical schema, a public API, a new Platform Capability, `Stable` Product Contract status or `Active` CAP-001 status for P10.03.

## 3. Review matrix against the ten R33 questions

| # | Review question | Result | Finding |
|---|---|---|---|
| 1 | Does any Company-specific taxonomy leak into shared Kernel/platform behavior? | `PASS with implementation constraint` | `Брендбук`, `Логотип`, `Шаблон документа`, `Организационный источник`, `company.*` names and Company review vocabulary remain Product Contract/product semantics. P10.03 may implement only domain-neutral admission mechanics and MUST NOT hardcode those taxonomies into Kernel/CAP-001 semantics. |
| 2 | Is staged receipt clearly distinct from canonical admission? | `PASS` | `StagedNonCanonical` remains non-canonical; admission requires separate Governed Execution and creates immutable canonical state/designation rather than relabeling staging. |
| 3 | Is generated output still transient until explicit promotion? | `PASS` | Generated output remains `TransientOutput`; promotion is a separate later P10.05 operation and is unavailable for real reliance before implementation/review. |
| 4 | Is every consequential canonical mutation routed through Governed Execution? | `PASS` | `admit-staged-version`, `admit-external-reference` and later `promote-reviewed` are all declared canonical mutations with RFC-0005 gate/evidence semantics. |
| 5 | Are Authentication, Authorization, Organizational Authority, Data Governance, validation and approval distinct? | `PASS with implementation constraint` | Contract/P10.01 separate all gates. Because Decision Authority Policy remains Proposed and no delegation is evidenced, first-slice canonical admission MUST retain explicit owner Organizational Authority/Consequential Approval rather than infer approval from login, button visibility or technical authorization. |
| 6 | Does the Product Contract declare exact reliance before implementation? | `PASS` | Effective `Provisional 0.2.0` identifies CAP-001, RFC-0005/0006/0008, ADR-0001, exact operation classes, security/data/portability/failure/migration semantics and exact approved Draft identity before P10.03. |
| 7 | Are external source-of-truth modes preserved? | `PASS` | `External Reference` remains externally authoritative; local cache/copy/extraction/generated representation cannot silently become `Native`; freshness/conflict/unavailability must remain explicit. |
| 8 | Are retention, minimization, rights and deletion treated structurally? | `PASS with fail-closed constraint` | Contract requires purpose, classification/handling, rights/source, retention/deletion and portability semantics and forbids invented concrete durations. P10.03 MUST fail closed where a required handling/rights/retention decision cannot be resolved; implementation may not invent policy to make admission succeed. |
| 9 | Does any browser/BFF route accidentally become a public/stable API promise? | `PASS` | ADR-0001 and Product Contract keep browser/BFF internal and release-scoped; operation semantic names do not establish a public wire/API compatibility commitment. |
| 10 | Does any AI suggestion become approval or canonical admission? | `PASS` | AI may analyze/draft/propose only; no suggestion, confidence, repeated use or generated result creates Organizational Authority, Consequential Approval, canonical admission or validated Knowledge. |

## 4. Iteration 1 — Company taxonomy / platform responsibility

### Finding

The Product Contract necessarily uses Company-specific labels and product-facing operation identities such as `company.asset.admit-staged-version`. Those names are valid inside the product boundary but would violate Constitution Article III, RFC-0001 and CAP-001 if copied directly into shared Kernel/CAP-001 semantic types or generalized as stable platform business concepts.

### Disposition

`PASS with mandatory P10.03 constraint`:

- Company asset roles/taxonomy remain metadata/semantics owned by Arvectum Company;
- Product Contract operation names may remain product-facing semantic names;
- P10.03 shared implementation must map them onto domain-neutral CAP-001/RFC-0005 mechanics such as exact candidate resolution, governed Document Version admission, explicit asset designation and reconstruction evidence;
- shared platform code must not branch on `brandbook`, `logo`, `template`, `organizational source`, Tender, Discount or other product-specific meaning except through product-owned validators/configuration behind the declared boundary;
- no new Kernel primitive, universal `Task`, generic product-action API or Company-owned taxonomy enters the platform through R33.

No Product Contract version change is required because the approved contract already explicitly assigns Company taxonomy and business semantics to the product side.

Result: `PASS`.

## 5. Iteration 2 — staged / canonical / generated lifecycle

### Review

P10.01 and Product Contract `0.2.0` maintain four distinct semantic states:

1. received/stored candidate;
2. `StagedNonCanonical` candidate;
3. immutable canonical Document/Artifact version plus explicit asset designation after successful Governed Execution;
4. generated `TransientOutput`, which can enter canonical state only through the separately implemented/reviewed promotion path.

No persistence, preview, download, repeated use, AI confidence or generation event is defined as implicit admission.

### Disposition

`PASS`.

P10.03 must preserve separate records/evidence for staged candidate and admitted canonical version rather than mutating staging into canonical history by relabeling. P10.03 does not implement generated-output promotion; P10.05 owns that path.

## 6. Iteration 3 — authority / approval / execution

### Finding

The current owner-operated contour is operationally simple, but simplicity must not collapse technical session state into authority. The approved P10.01 matrix states explicit owner approval for current first-slice canonical admission, while Product Contract `0.2.0` preserves separate current Authorization, Organizational Authority, Data Governance, validation and applicable Consequential Approval gates.

Decision Authority Policy `0.2.1` remains `Proposed`; no approved delegation was found that transfers this first-slice authority away from the owner.

### Disposition

`PASS with mandatory P10.03 constraint`:

- successful authentication/session/CSRF/origin checks do not approve admission;
- technical Authorization does not establish Organizational Authority;
- initial P10.03 owner-operated canonical admission must preserve an explicit owner authority/approval decision for the exact candidate/version and operation;
- a later approved delegation may change who satisfies the authority/approval gate without changing Identity or silently broadening technical permission;
- all consequential mutations pin exact effective Product Contract/workflow/material/control versions and use RFC-0005 idempotency, failure and uncertainty semantics;
- no historical replay repeats a canonical/external effect without a new applicable governed execution.

No new owner approval is required for R33 itself: this is a functional boundary review and does not create a new Product Contract lifecycle transition, capability promotion, public contract or authority delegation.

Result: `PASS`.

## 7. Iteration 4 — external authority / rights / retention / portability

### Review

The contract correctly distinguishes:

- `Native` authority for the exact Company-held governed Document/Artifact version and governance envelope;
- `External Reference` authority for externally authoritative underlying content/fact scope;
- legal ownership/reuse rights from architectural asset designation;
- canonical history/evidence retention from physical deletion obligations;
- portable governed identity/version/provenance/authority/handling semantics from disposable staging/search/cache state.

Concrete retention periods are not defined by P10.02 and must not be invented by implementation.

### Disposition

`PASS with fail-closed implementation rule`.

P10.03 must require the applicable purpose, source/rights basis, Organization scope and handling/retention/deletion references where required for the asset class/use. If a required rule is unresolved, the truthful result is blocked rather than an invented default admission. Minimization applies to evidence: raw content, reusable credentials and unnecessary sensitive payload are not duplicated merely for auditability.

No competing source of truth is created.

## 8. Iteration 5 — Workspace / product-action / AI boundary

### Review

`workspace.actionable-work.project-request` is read-only/non-canonical and `workspace.product-operation.enter` is a no-side-effect routing envelope. Neither grants a Tender Agent, Discount Parser or other product operation. Actual downstream consequential product behavior remains governed by the owning product's exact effective Product Contract and workflow.

ADR-0001 additionally keeps browser/BFF state, projections and controls non-authoritative and internal/release-scoped.

AI may classify, summarize, draft and propose but cannot create a real Action Request source, approval, Organizational Authority, admission, validated Knowledge or external effect.

### Disposition

`PASS`.

R33 does not authorize P10.07 product execution, a public `/bff/*` surface, remote host execution, automatic external sending/signing/publication or cross-product internal imports.

## 9. Iteration 6 — CAP-001 / ADR / final architecture fitness

### CAP-001 lifecycle

`PASS`. CAP-001 remains `Incubating / Provisional`. P10.02 consumption of CAP-001 does not promote it to `Active` and does not create production/support/public-compatibility obligations.

### Capability boundary

`PASS`. The required P10.03 mechanism is within CAP-001's existing bounded domain-neutral scope: logical Document identity/version, governed admission, asset designation, provenance/derivation and exact-version reliance. Company taxonomy remains product-owned.

### ADR gate

`PASS for current architecture boundary; conditional implementation trigger retained`.

R33 itself selects no new concrete durable persistence, object-store, transaction/concurrency mechanism, evidence-integrity mechanism, stable serialization/API or separately deployable topology. Therefore no new ADR is required merely to close R33.

P10.03 MUST reopen the ADR gate before material reliance if implementation introduces a new durable architectural mechanism in any of those categories rather than reusing an already governed compatible mechanism without changing its architectural responsibility.

### Final higher-authority review

`PASS`. No conflict was found with Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008, ADR-0001, CAP-001's Provisional contract, P10.01 or lifecycle-current Product Contract `0.2.0`.

Material objections after iteration 6: **none**.

Final result: **`Complete / PASS after 6 iterations`**, subject to the mandatory P10.03 implementation constraints in Section 10.

## 10. Mandatory P10.03 implementation gates

R33 PASS unblocks P10.03 only within the following boundary. P10.03 must prove at minimum:

1. **Domain-neutral shared implementation** — no hardcoded Company asset taxonomy/business meaning in Kernel/CAP-001; product labels/validators remain product-owned.
2. **Exact staged input** — one exact staged candidate/version/content digest is resolved before admission; stale/mismatched inputs fail closed.
3. **No staging relabel** — canonical admission creates immutable governed state/designation and does not rewrite the staged candidate into canonical history.
4. **Current Organization/Actor** — attributable actor and exactly one Organization scope are resolved server-side.
5. **Separate current gates** — Authorization, Organizational Authority, Data Governance, validation and Consequential Approval remain independently evaluable.
6. **Owner authority at current governance state** — absent approved exact delegation, first-slice canonical admission records explicit owner Organizational Authority/approval; login/button visibility/technical write capability is insufficient.
7. **Exact version pins** — effective Product Contract `0.2.0`, workflow/operation definition and materially relied-upon governed control/input versions are preserved in execution evidence.
8. **Authority-mode fidelity** — `Native` applies only to the declared Company-held governed scope; external authority remains `External Reference` where declared, with freshness/conflict/unavailability semantics.
9. **Rights/data governance fail closed** — unresolved required purpose, classification/handling, rights/source or retention/deletion semantics block admission rather than being invented.
10. **Idempotency / uncertainty** — retry cannot silently duplicate a prior successful or possibly-successful admission; blocked/failed/uncertain/reconciliation-required outcomes remain distinguishable.
11. **Event/provenance evidence** — required canonical execution/admission/designation evidence is reconstructable; ordinary logs/telemetry do not substitute for required canonical evidence.
12. **Projection non-authority** — Workspace/read-model/search state may explain and locate candidates/assets but never authorizes the mutation.
13. **AI non-authority** — AI may propose metadata/classification/review assistance but cannot satisfy authority/approval or silently admit the asset.
14. **No Knowledge promotion** — admitted Document/Artifact/Asset state does not automatically become RFC-0007 validated Knowledge.
15. **Internal surface only** — no public/stable API/SDK/BFF compatibility commitment is created by implementation operation names or routes.
16. **No premature P10.05/P10.07 scope** — generated-output promotion and downstream product consequential actions remain unavailable until their own roadmap work/gates.
17. **ADR re-trigger** — any new materially constraining durable persistence/object-store/transaction/evidence-integrity/stable serialization/service-topology decision reopens the ADR gate before reliance.
18. **No lifecycle overclaim** — P10.03 success does not make Product Contract `Stable`, CAP-001 `Active`, the environment customer Production, or broaden conformance/support claims.

These constraints are implementation acceptance criteria derived from already binding authority; they do not amend the approved Product Contract.

## 11. Human-readable R33 result

In practical terms, R33 says:

- Arvectum OS may now implement the **generic safe mechanism** that takes one exact staged Company material and, after all current checks and explicit owner authority, admits it as an immutable governed Document/Asset version;
- the platform is not allowed to learn what a `brandbook`, `logo` or Company `template` means as shared business semantics — those remain Company/product meaning;
- storing or uploading a file is still not admission;
- AI cannot approve admission;
- external references remain external authority;
- if rights, scope, handling or required retention/deletion rules are unresolved, the correct result is `blocked`, not a guessed default;
- the browser button is only an interface to the governed command, not the authority for it;
- implementation may not quietly create a new public API, universal action system, Stable Product Contract or Active Platform Capability.

## 12. Closure disposition

R33 is `Complete / PASS` for the declared architecture/Product Contract/authority gate.

No separate owner approval is required to close this functional gate because R33 makes no new lifecycle promotion, authority delegation, public/stable contract, external commitment or Product Contract semantic change. Residual authority remains with the owner exactly as before.

P10.03 is unblocked **only** within the Section 10 constraints. P10.03 remains responsible for implementation and evidence; R33 is not implementation PASS.

Next canonical action after roadmap synchronization:

> **P10.03 — Domain-neutral organizational-asset admission execution path.**

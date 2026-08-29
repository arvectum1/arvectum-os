# DECISION-2026-08-29 — ADR-0002 Acceptance

Status: `Approved`
Decision date: `2026-08-29`
Owner / decision authority: `ООО «Арвектум»`
Task classification: `governance` with `product_contract`, `product_specific` and `platform-boundary`
Decision subject: `ADR-0002 — Company Workspace Durable Governed State`
Approved proposal version: `0.1.0`
Approved reviewed proposal blob: `50103841e624fc09a84e0a1f5aa09eae77fafba3`
Review gate: [`R34 — M10-alpha Asset Governance / Usability Review`](../../reviews/R34-m10-alpha-asset-governance-usability-review.md) — `Executed / BLOCKED`
Constitution: `1.2.0` — `Ratified`
Architecture baseline: RFC-0001 through RFC-0008 `1.0.0` — `Accepted`
Decision Authority Policy: `Proposed 0.2.1` — non-binding; residual authority remains with owner
Canonical approval reference: this decision record

## 1. Decision

**APPROVED — accept ADR-0002 proposal version `0.1.0`, identified by exact immutable blob `50103841e624fc09a84e0a1f5aa09eae77fafba3`, as the binding subordinate architecture decision for durable governed Company Workspace state within the exact bounded scope declared by the proposal.**

The approved decision permits the current Company Workspace runtime to persist the governed admission/promotion state needed by the P10.02 `Provisional 0.2.0` boundary using owner-local, immutable, schema-versioned JSON records under the existing Workspace runtime root.

The approval does not select a platform-wide database, does not create a public persistence contract, does not create a new Kernel primitive, does not promote any Platform Capability and does not close R34 or M10-alpha by itself.

## 2. Authority basis

Decision Authority Policy `0.2.1` remains `Proposed` and therefore has no binding delegated-authority force. Under the current Accepted governance baseline, residual decision authority remains with the owner of Arvectum OS.

The owner explicitly approved ADR-0002 `v0.1.0` by exact proposal blob `50103841e624fc09a84e0a1f5aa09eae77fafba3` on `2026-08-29`. This record preserves that approval canonically rather than leaving the consequential architecture decision only in conversation history.

## 3. Review basis

The ADR proposal completed five functional cross-review iterations with no unresolved material objection at proposal level.

The R34 re-review identified two independent blockers:

1. `B1` — real owner-operated Company asset-cycle evidence is absent;
2. `B2` — restart-durable governed admission/promotion state and recovery evidence are absent.

ADR-0002 addresses only the architecture choice required to remediate B2. Implementation, restart/recovery evidence and the real owner-operated cycle remain separate requirements.

## 4. Approved scope

This approval applies only to the current bounded operating contour:

- `Local / Persistent Internal / owner-operated`;
- one currently activated governing Organization: `ООО «Арвектум»`;
- Company Workspace asset admission and reviewed generated-output promotion under P10.02 `Provisional 0.2.0`;
- owner-local product-runtime persistence behind existing semantic owners;
- open, inspectable, schema-versioned JSON records plus the existing content-addressed material/output stores.

The physical file layout remains an internal implementation detail and is not a shared Platform Contract.

## 5. Required implementation discipline

Implementation under this ADR must preserve at least:

- exact Subject/Version/Event identities;
- provenance and immutable lineage;
- retry-token/fingerprint consistency;
- fail-closed behavior for unknown, corrupt or conflicting records;
- successful-result durability before reporting durable success;
- read-after-write reconstruction of the same exact committed result;
- uncertainty across restart until explicit reconciliation;
- reconstruction without replaying historical consequential effects;
- separation of staging/review/transient output from canonical admission/promotion;
- Organization scope, data-handling and secret-minimization requirements;
- portability and future migration without dependence on opaque process snapshots.

## 6. Explicit non-claims

This approval does not establish:

- customer/external Production;
- a Stable Product Contract;
- an Active Platform Capability;
- a platform-wide database/event-store architecture;
- multi-node transactionality or high availability;
- SLA/RTO/RPO/support/certification commitments;
- public/stable persistence, API or wire compatibility;
- R34 PASS or M10-alpha achievement;
- permission to replay historical consequential effects during recovery.

## 7. Effective transition

This approval becomes the decision-authority basis for publishing ADR-0002 as `Accepted` only when:

1. the ADR acceptance publication identifies exact approved proposal blob `50103841e624fc09a84e0a1f5aa09eae77fafba3`;
2. acceptance publication does not materially broaden the approved proposal;
3. ADR index is synchronized;
4. canonical roadmap and Phase 10 roadmap are synchronized to show ADR-0002 accepted and B2 implementation/recovery remediation as the current prerequisite inside R34;
5. resulting repository state is read-after-write verified.

After valid acceptance publication, the next executable R34 remediation action is implementation and verification of durable Company admission/promotion state under ADR-0002. R34 remains `BLOCKED / NOT PASS` until both durable/recovery evidence and the real owner-operated evidence cycle are complete.
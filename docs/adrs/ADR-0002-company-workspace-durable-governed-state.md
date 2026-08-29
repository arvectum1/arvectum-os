# ADR-0002 — Company Workspace Durable Governed State

Status: `Accepted`
Accepted: `2026-08-29`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `product_specific`, `platform-boundary` and `governance`
Related: Constitution `1.2.0`; RFC-0001, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0008 `1.0.0` — `Accepted`; ADR-0001 — `Accepted`; P10.02 Company Workspace Product Contract `0.2.0` — `Provisional`; R34 — `Executed / BLOCKED`
Approval: [`DECISION-2026-08-29 — ADR-0002 Acceptance`](../governance/decisions/DECISION-2026-08-29-ADR-0002-ACCEPTANCE.md) — `Approved`
Approved reviewed proposal version: `0.1.0`
Approved reviewed proposal blob: `50103841e624fc09a84e0a1f5aa09eae77fafba3`

## 1. Acceptance publication

This file is the canonical `Accepted` publication of ADR-0002.

The complete normative substance is the owner-approved reviewed proposal identified by immutable blob:

`50103841e624fc09a84e0a1f5aa09eae77fafba3`

The proposal was reviewed through five functional cross-review iterations with no unresolved material objection at proposal level, then explicitly approved by the residual owner authority on `2026-08-29`.

This publication changes lifecycle status and records approval evidence. It does not materially broaden the approved proposal.

## 2. Accepted decision

For the bounded Company Workspace runtime, the governed state produced by Company asset admission and reviewed generated-output promotion SHALL become restart-durable through a product-local owner-local persistence adapter using immutable, schema-versioned JSON records under the existing Workspace runtime root.

The adapter is subordinate to existing Accepted RFC semantics and the P10.02 `Provisional 0.2.0` Product Contract. It is not a new Kernel primitive, a mandatory platform database, a public persistence API, a shared Platform Capability or a production-readiness claim.

## 3. Required properties

The accepted implementation must preserve the complete requirements of proposal blob `50103841e624fc09a84e0a1f5aa09eae77fafba3`, including at minimum:

1. owner-only filesystem scope consistent with the existing Company materials store;
2. immutable schema-versioned records for committed admission/promotion results and retry/uncertainty evidence;
3. temporary-file plus durable close/fsync and atomic replacement/rename semantics appropriate to the local filesystem;
4. refusal of unsafe paths, symlinks and conflicting identity reuse;
5. exact Organization, Subject, Version, Event, digest, lineage and provenance reconstruction;
6. deterministic retry-token/fingerprint conflict detection;
7. no duplication of raw Company document bytes into governance metadata when existing content-addressed stores already hold them;
8. no persistence of reusable credentials/secrets for audit convenience;
9. no successful durable result reported until the durable record exists and read-after-write reconstructs the same exact semantic result;
10. truthful failed/uncertain/reconciliation-required state when durable outcome cannot be proved;
11. restart recovery by reconstruction only, never by replaying historical consequential effects;
12. fail-closed treatment of uncertain prior attempts and unknown/corrupt/incompatible schemas;
13. coherent backup/restore coverage of governed metadata plus referenced retained source/output bytes;
14. explicit portability/migration path without Python pickle, opaque process snapshots or proprietary mandatory encoding;
15. no hidden dependency by other products on Company-specific filesystem paths or schemas.

## 4. Product / platform boundary

Platform-owned semantics remain those defined by the Constitution and Accepted RFCs: identity/versioning, Governed Execution, Event/provenance, Document/Artifact and Organizational Asset semantics.

Company-owned implementation remains responsible for this bounded persistence adapter, its owner-local runtime directory composition and Company-specific projections/UX.

Another product does not inherit this persistence mechanism automatically. Reuse or promotion into a shared Platform Capability requires a separate governed decision and evidence.

## 5. Security and authority boundary

Persistence is not authority.

A recovered record does not by itself grant current Authentication, Authorization, Organizational Authority, Data Governance permission or Consequential Approval for a new operation.

The implementation must preserve one-Organization scope, least privilege, data minimization, classification/purpose/rights/retention/deletion constraints and secret-safe logging.

## 6. Recovery and replay

Recovery reconstructs already-established governed state. It must not repeat historical canonical admission, reviewed promotion or any external consequential effect.

If a prior effect may have succeeded but durable outcome is uncertain, restart must preserve that uncertainty and require reconciliation rather than silently retrying.

If the durable committed record already exists but the original client response was lost, retry must resolve the same committed result idempotently.

## 7. Backup, restore and update requirement

R34 may not pass on the basis of this ADR alone.

Implementation evidence must prove at least that:

- admitted Company asset identity/version/provenance/Event evidence survives restart;
- promotion survives restart while the source remains `TransientOutput`;
- pre-promotion admitted versions remain immutable and retrievable;
- backup and restore reconstruct the exact retained state;
- update/restart does not silently reinterpret stored schema versions;
- unknown/corrupt records fail closed;
- recovery does not replay consequential effects.

## 8. Alternatives and rationale

The approved proposal considered and rejected, for the current stage:

- remaining in-memory through R34 — insufficient for required restart/recovery evidence;
- selecting SQLite as a platform-wide canonical database now — broader than required and risks hidden platform coupling;
- Python pickle/process snapshots — opaque, runtime-coupled and poor for portability/safe migration;
- one mutable JSON snapshot as the only history — too weak for append-only effect/retry evidence;
- an external DMS/object store/event database — unnecessary infrastructure for the current Local / Persistent Internal / owner-operated slice.

Owner-local immutable JSON was selected because it is the minimum bounded, inspectable, reversible mechanism that removes the known R34 durability blocker without pretending to solve general platform persistence.

## 9. Lifecycle and non-claims

ADR-0002 is now binding within its declared scope.

Acceptance does **not** by itself:

- implement the persistence adapter;
- close R34;
- achieve M10-alpha;
- promote P10.02 to `Stable`;
- promote CAP-001 or another capability to `Active`;
- establish customer/external Production;
- create SLA/RTO/RPO/support/certification commitments;
- define a platform-wide database/event-store architecture;
- create public/stable persistence or wire compatibility.

## 10. Next canonical action

The next executable R34 remediation step is to implement and verify durable Company admission/promotion state under this ADR, including restart, retry/reconciliation, backup/restore and update compatibility evidence.

Only after that evidence exists should the real owner-operated Company asset cycle be executed as closing R34 evidence.

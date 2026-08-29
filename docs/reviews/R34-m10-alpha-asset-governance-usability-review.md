# R34 — M10-alpha Asset Governance / Usability Review

**Version:** 0.3.0  
**Status:** Executed / BLOCKED — durable-state implementation/recovery evidence + real owner-operated evidence required  
**Date:** 2026-08-29  
**Review target:** first real owner-operated Arvectum Company asset cycle  
**Gate verdict:** `NOT PASS`  
**Milestone:** `M10-alpha` remains unclaimed

## 1. Review objective

R34 is the mandatory M10-alpha governance/usability gate after P10.05. It determines whether the first real owner-operated Arvectum Company asset cycle is usable, governance-correct, durable and reconstructable under actual organizational evidence.

A PASS may not be inferred from implementation completeness, automated tests, synthetic fixtures or prior closure reviews alone.

## 2. Canonical authority checked

R34 remains subordinate to:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted`;
- ADR-0002 — `Company Workspace Durable Governed State`, `Accepted 2026-08-29`;
- P10.02 Company Workspace Product Contract `0.2.0` — `Provisional`;
- canonical roadmap and Phase 10 roadmap;
- P10.03/P10.04/P10.05 implementation and closure evidence.

No conflict with higher-authority canonical semantics is identified.

## 3. Current gate state

Two independent blockers remain.

### B1 — real owner-operated evidence is absent

No canonical evidence packet yet demonstrates the required first real owner-operated Company asset cycle across the R34 review dimensions.

CI, regression tests, synthetic fixtures and P10.03–P10.05 closure evidence remain implementation context only. They cannot substitute for the real owner-operated milestone evidence.

### B2 — restart-durable governed state is not yet implemented/proven

P10.03/P10.04/P10.05 intentionally closed with bounded in-memory admission/promotion state and made no restart-durable persistence claim.

ADR-0002 is now `Accepted` and selects the bounded remediation architecture:

- product-local owner-local persistence under the existing Workspace runtime root;
- immutable schema-versioned JSON records for committed and retry/uncertainty evidence;
- existing content-addressed material/output stores retained for bytes;
- reconstruction without replaying historical consequential effects;
- no platform-wide database mandate, new Kernel primitive, public persistence API or automatic Platform Capability promotion.

The architecture-decision prerequisite is therefore closed. The implementation and recovery evidence required by B2 are **not** yet complete.

A successful single-process click-through is still insufficient for R34 PASS.

## 4. Current R34 scope matrix

| Review area | Current evidence | Current finding |
| --- | --- | --- |
| Owner usability | P10.04 owner-facing UX; no real owner cycle | `BLOCKED / NOT EVALUATED LIVE` |
| Exact version / provenance | bounded semantic + regression evidence | `BLOCKED pending durable reconstruction + real evidence` |
| Authorization / Organizational Authority / Data Governance | RFC/Product Contract/implementation evidence | `BLOCKED pending real point-of-use evidence` |
| Data handling / logging | structural controls exist | `BLOCKED pending real evidence` |
| Partial failure / retry | semantic retry/idempotency model exists | `BLOCKED pending durable restart/reconciliation evidence` |
| Generated output | P10.05 transient/review/promotion semantics exist | `BLOCKED pending durable promotion state + real promotion evidence` |
| Recovery / update compatibility | ADR-0002 accepted; implementation absent | `BLOCKER B2` |
| Product/platform coupling | ADR-0002 explicitly product-local | no present architecture violation; implementation must preserve this boundary |

## 5. Findings

### F1 — live evidence remains mandatory

R34 is an owner-operated milestone gate. Synthetic execution cannot substitute for real organizational evidence.

**Severity:** gate blocker.  
**Disposition:** unresolved until B2 implementation/recovery evidence passes and one real bounded owner-operated cycle is executed and reviewed.

### F2 — durable/reconstructable state remains a material implementation blocker

ADR-0002 now supplies the accepted architecture decision, but the production/reference runtime has not yet demonstrated that Company asset admission and reviewed-output promotion reconstruct exactly across restart/restore/update.

R34 therefore remains blocked until implementation proves exact identities, versions, provenance, Event references, retry state and promotion state survive the declared recovery boundary.

**Severity:** gate blocker.  
**Disposition:** implementation and evidence required.

### F3 — no RFC amendment is required

Accepted RFCs intentionally remain technology-neutral while requiring reconstructability, portability, safe retry/replay and append-only Event meaning. ADR-0002 is the correct subordinate decision level for the concrete Company-local persistence choice.

### F4 — ADR-0002 is accepted but bounded

ADR-0002 is binding only for the declared Company Workspace scope. It does not create a platform-wide database choice, public persistence API, Stable Product Contract, Active Platform Capability or production-readiness claim.

### F5 — generated output classification remains correct

Generated output remains `TransientOutput` by default. Review alone does not canonicalize it. Promotion is a separate Governed Execution creating a new immutable governed version. The durable implementation must preserve that separation across restart/recovery.

### F6 — historical recovery must not replay consequential effects

Recovery may reconstruct admitted state from durable evidence but must not re-run historical canonical admission/promotion or external effects. Any new consequential effect still requires current applicable Governed Execution and gates.

## 6. Functional cross-review state

The prior R34 review completed six functional iterations. ADR-0002 proposal separately completed five functional iterations with no unresolved material objection at proposal level.

After owner approval and ADR acceptance, the remaining material objections are implementation/evidence blockers rather than unresolved architecture design objections:

1. **Governance/authority:** accepted persistence must not become authorization or authority. `PASS at architecture level`; live evidence pending.
2. **Architecture/product boundary:** ADR-0002 keeps storage product-local and bounded. `PASS at architecture level`.
3. **Events/idempotency/recovery:** implementation must prove immutable durable evidence and reconstruction without replay. `BLOCKED pending implementation evidence`.
4. **Security/privacy:** raw content/secrets must not be duplicated into governance records/logs. `BLOCKED pending implementation evidence`.
5. **Portability/migration:** schema-versioned open representation is accepted. `PASS at architecture level`; migration/recovery tests pending.
6. **Usability/milestone integrity:** real owner validation remains absent. `BLOCKED pending B1`.

No additional design-review iteration is useful before implementation evidence exists.

## 7. Required remediation sequence

The current canonical sequence is:

```text
ADR-0002 Accepted ✓
        ↓
durable Company admission/promotion state implementation
        ↓
restart + retry/reconciliation + backup/restore + update evidence
        ↓
one real owner-operated Company asset cycle
        ↓
R34 re-review
        ↓ PASS only if criteria satisfied
M10-alpha
```

## 8. Required implementation/recovery evidence

Before the live cycle can close R34, evidence must show at least:

1. committed admission survives process restart with the same Document/Asset/Event identities;
2. exact source digest/version and lineage remain resolvable;
3. retry after a lost response resolves an existing successful result without duplicating the consequential effect;
4. uncertain prior attempt remains fail-closed across restart until reconciliation;
5. reviewed promotion survives restart while the source output remains `TransientOutput`;
6. pre-promotion source/admitted versions remain unchanged;
7. corrupted, partial, conflicting or unknown-schema durable records fail closed;
8. backup → restore reconstructs exact admitted/promoted state and referenced retained bytes;
9. update/restart does not silently reinterpret stored schema versions;
10. recovery/replay does not repeat consequential effects;
11. governed contents, secrets and reusable credentials are not duplicated into logs or persistence metadata unnecessarily;
12. persistence paths/schemas do not become hidden platform dependencies for other products.

## 9. Required real owner evidence packet

After the durable-state evidence passes, one real bounded Company asset cycle must capture:

1. owner/operator and Organization context without secrets;
2. UTC timestamps plus environment/build/commit identity;
3. one real bounded Company material and classification without embedding unnecessary raw contents in governance markdown;
4. exact asset/version/checksum/provenance/ownership/Event references;
5. owner-visible list/detail and exact-version retrieval/use;
6. point-of-use Authorization, Organizational Authority and Data Governance evidence;
7. one safe negative/denied or partial-failure path plus retry/recovery behavior;
8. generated transient output, human review, explicit governed promotion and resulting new version;
9. original version/output state unchanged as required;
10. restart/restore/update compatibility evidence;
11. owner UX observations and P0/P1/P2/P3 defect classification;
12. references to evidence artifacts rather than sensitive payload copies.

## 10. Exit criteria

R34 may become `Closed / PASS` only when:

- ADR-0002 implementation and durable/recovery evidence pass;
- the real owner-operated evidence packet is reviewed;
- no unresolved P0/P1 exists in M10-alpha scope;
- no unresolved structural concern exists around ownership, exact-version pinning, provenance, governed promotion, data handling, authority/gates, retry/reconciliation or recovery;
- generated output remains transient unless separately promoted;
- the owner path is usable enough without product-specific semantic inflation into shared platform behavior.

Only then may the roadmap claim `M10-alpha`.

## 11. Current review decision

**R34:** `Executed / BLOCKED`  
**Gate verdict:** `NOT PASS`  
**Blocker B1:** real owner-operated Company asset-cycle evidence absent  
**Blocker B2:** ADR-0002 implementation + restart/recovery evidence absent  
**ADR-0002:** `Accepted` — architecture decision prerequisite closed  
**Next executable action:** implement and verify durable Company admission/promotion state under ADR-0002  
**M10-alpha:** remains unclaimed  
**RFC amendment required:** none  
**Product Contract lifecycle transition performed:** none  
**Platform Capability promotion performed:** none

# R34 — M10-alpha Asset Governance / Usability Review

**Version:** 0.2.0  
**Status:** Executed / BLOCKED — durable-state remediation + real owner-operated evidence required  
**Date:** 2026-08-29  
**Review target:** first real owner-operated Arvectum Company asset cycle  
**Canonical baseline reviewed:** `main@717f9091572ade1c961d2b85e93c1ba0772c39fc`  
**Gate verdict:** `NOT PASS`  
**Milestone:** `M10-alpha` remains unclaimed

## 1. Review objective

R34 is the mandatory M10-alpha governance/usability gate after P10.05. It must determine whether the first real owner-operated Arvectum Company asset cycle is both usable and governance-correct under actual organizational evidence, including restart/recovery/update compatibility.

A PASS may not be inferred from implementation completeness, automated tests, synthetic fixtures or prior closure reviews alone.

## 2. Canonical inputs checked

The review was re-executed against:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted`;
- P10.02 Company Workspace Product Contract `0.2.0` — `Provisional`;
- roadmap `2.97.5` and Phase 10 operational guide;
- P10.03/P10.04/P10.05 implementation and closure evidence;
- `reference/python/arvectum_os_ref/organizational_asset_admission.py`;
- `reference/python/workspace_app/company_asset_library.py`;
- `reference/python/workspace_app/company_asset_governed_provider.py`;
- `reference/python/workspace_app/company_generated_outputs.py`;
- `reference/python/workspace_app/company_materials.py`;
- merged R34 v0.1.0 baseline at `main@717f9091572ade1c961d2b85e93c1ba0772c39fc`.

No conflict with higher-authority canonical semantics was found. The deeper implementation review did identify a material implementation/architecture decision gap that the original R34 v0.1.0 had not yet classified explicitly.

## 3. Gate admission / evidence state

Two independent blockers exist.

### B1 — required real owner-operated evidence is absent

No canonical evidence packet demonstrates the first real owner-operated Company asset cycle across R34 dimensions. CI, regression tests, synthetic fixtures and P10.03–P10.05 closure evidence remain implementation context only.

### B2 — restart-durable governed Company asset state is not implemented

P10.03/P10.04/P10.05 intentionally retain admission/promotion canonical state in bounded in-memory semantic state. Their closure records explicitly do not claim restart-durable canonical state, durable Governed Execution/Event storage, transparent continuity across restart or restore/update survival.

This becomes a gate blocker at R34 because Phase 10 and R34 require the real organizational-asset cycle to be durable/reconstructable and require backup/restore/update compatibility evidence.

A successful single-process live click-through would therefore still be insufficient for R34 PASS.

The semantic owner also explicitly leaves selection of a database/object store/durable idempotency ledger/serialization contract behind the applicable ADR gate. R34 must not silently choose one through implementation.

## 4. R34 scope matrix

| Review area | Current evidence | Finding |
| --- | --- | --- |
| Owner usability | P10.04 owner-facing UX; no real owner cycle | `BLOCKED / NOT EVALUATED LIVE` |
| Exact version / provenance | bounded semantic + regression evidence | `BLOCKED pending real evidence and restart reconstruction` |
| Authorization / Organizational Authority / Data Governance | RFC/Product Contract/implementation evidence | `BLOCKED pending real point-of-use evidence` |
| Data handling / logging | structural controls exist | `BLOCKED pending real evidence` |
| Partial failure / retry | in-memory semantic retry/idempotency model exists | `BLOCKED: durability across restart not established` |
| Generated output | P10.05 transient/review/promotion semantics exist | `BLOCKED pending durable promotion state + real promotion` |
| Recovery / update compatibility | explicit P10.04/P10.05 non-claim | `BLOCKER B2` |
| Product/platform coupling | current code remains bounded/product-composed | no present violation; persistence choice requires explicit boundary decision |

## 5. Findings

### F1 — live evidence remains mandatory

R34 is an owner-operated milestone gate. Synthetic execution cannot substitute for real organizational evidence.

**Severity:** gate blocker.  
**Disposition:** unresolved until B2 is remediated sufficiently to make the real cycle valid, then one real bounded owner-operated cycle is executed and captured.

### F2 — durable/reconstructable state is a material R34 blocker

`OrganizationalAssetAdmissionState` and `ReviewedGeneratedOutputPromotionState` are in-memory. Staging/review/transient bytes/manifests are filesystem-backed, but the consequential admission/promotion result and required retry/event reconstruction state do not survive process restart as current canonical runtime state.

That means current runtime cannot yet prove the R34 requirement that an admitted/promoted asset remains reconstructable through restart/backup/restore/update.

**Severity:** gate blocker.  
**Disposition:** requires an explicit subordinate architecture decision and implementation/evidence before the live R34 cycle can close the gate.

### F3 — no RFC amendment is required

Accepted RFCs intentionally remain technology-neutral and permit simple reversible storage while requiring reconstructability, portability, append-only Event meaning and safe retry/replay semantics.

The missing choice is concrete and subordinate, not a change to Kernel/RFC semantics. A new ADR is the minimally sufficient governance level.

### F4 — ADR-0002 proposal is the bounded remediation direction

`ADR-0002 — Company Workspace Durable Governed State` is prepared as `Proposed 0.1.0` on the R34 remediation branch. It chooses product-local owner-local immutable schema-versioned JSON records under the existing runtime root, with rebuildable projections, no new shared Platform Capability, no public/stable persistence API and no database mandate.

The proposal has no normative force until exact owner approval and valid acceptance publication.

### F5 — generated output classification remains correct

Generated output remains `TransientOutput` by default. Review alone does not canonicalize it. Promotion is a separate Governed Execution creating a new immutable governed version. R34 requires the durable implementation to preserve that separation across restart/recovery.

### F6 — historical recovery must not replay consequential effects

Recovery may reconstruct admitted state from durable evidence but must not re-run historical canonical admission/promotion or external effects. Any new consequential effect still requires a current applicable Governed Execution and gates.

## 6. Functional cross-review

This is functional review, not formal ADR approval or lifecycle promotion.

1. **Governance/authority:** B1 remains; B2 must not be solved by treating persistence as current authorization or owner approval. `PASS with blockers retained`.
2. **Architecture/product boundary:** a product-local persistence adapter is sufficient; platform-wide DB/event-store selection would overreach. `PASS after ADR-0002 direction`.
3. **Events/idempotency/recovery:** immutable per-operation durable evidence + reconstruction without side-effect replay is required. `PASS after ADR-0002 direction`.
4. **Security/privacy:** governed metadata may persist; raw content remains in existing content-addressed stores; secrets/reusable credentials must not be copied into records/logs. `PASS`.
5. **Portability/migration:** open schema-versioned representation is required; pickle/opaque process snapshots are unsuitable. `PASS`.
6. **Usability/milestone integrity:** live owner validation cannot occur as closing evidence until durable-state blocker is removed; M10-alpha remains unclaimed. `PASS`.

No seventh iteration is useful before owner disposition of the exact ADR proposal and implementation evidence.

## 7. R34 remediation sequence

The canonical safe sequence is:

```text
ADR-0002 Proposed + reviewed
        ↓ explicit exact owner approval
ADR-0002 Accepted publication + index/roadmap sync
        ↓
durable Company admission/promotion state implementation
        ↓
restart + backup/restore + update + retry/reconciliation evidence
        ↓
one real owner-operated Company asset cycle
        ↓
R34 re-review
        ↓ PASS only if criteria satisfied
M10-alpha claim
```

Implementation may be prepared experimentally in parallel only while it remains bounded/reversible and is not used to claim canonical closure before the ADR is validly accepted.

## 8. Required implementation/recovery evidence

Before the live cycle can close R34, evidence must show at least:

1. committed admission survives process restart with the same Document/Asset/Event identities;
2. exact source digest/version and lineage remain resolvable;
3. successful retry after lost response resolves the existing result without duplicate consequential effect;
4. uncertain prior attempt remains fail-closed across restart until reconciliation;
5. promotion survives restart while source output remains `TransientOutput`;
6. pre-promotion source/admitted versions remain unchanged;
7. corrupted/partial/unknown-schema durable records fail closed;
8. backup → restore reconstructs exact admitted/promoted state and referenced retained bytes;
9. update/restart does not silently reinterpret stored schema versions;
10. recovery/replay does not repeat consequential external effects;
11. governed contents/secrets are not duplicated into logs.

## 9. Required real owner evidence packet

After the durable-state gate is satisfied, one real bounded Company asset cycle must capture:

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

- ADR/persistence remediation required by B2 is validly governed and implemented;
- durable/recovery evidence above passes;
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
**Blocker B2:** restart-durable governed admission/promotion state + recovery evidence absent  
**Required architecture action:** ADR-0002 exact owner disposition before canonical implementation reliance  
**M10-alpha:** remains unclaimed  
**RFC amendment required:** none  
**Product Contract lifecycle transition performed:** none  
**Platform Capability promotion performed:** none

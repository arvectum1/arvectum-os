# R34 — M10-alpha Asset Governance / Usability Review

**Version:** 0.4.1  
**Status:** Executed / BLOCKED — B2 closed; B1 execution runbook prepared but real owner-operated evidence still required  
**Date:** 2026-08-30  
**Review target:** first real owner-operated Arvectum Company asset cycle  
**Gate verdict:** `NOT PASS`  
**Milestone:** `M10-alpha` remains unclaimed

## 1. Review objective

R34 is the mandatory M10-alpha governance/usability gate after P10.05. It determines whether the first real owner-operated Arvectum Company asset cycle is usable, governance-correct, durable and reconstructable under actual organizational evidence.

A PASS may not be inferred from implementation completeness, automated tests, synthetic fixtures, a prepared runbook or prior closure reviews alone.

## 2. Canonical authority checked

R34 remains subordinate to:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR-0001 — `Accepted`;
- ADR-0002 — `Company Workspace Durable Governed State`, `Accepted 2026-08-29`;
- P10.02 Company Workspace Product Contract `0.2.0` — `Provisional`;
- canonical roadmap and Phase 10 roadmap;
- P10.03/P10.04/P10.05 implementation and closure evidence;
- R34-D1 durable-state implementation merged to `main` at `5f65061095094d9b58a4b293b2a5a8f01d88ad10`;
- R34-D2 Productive Workspace wiring/qualification merged in PR #34 at `152bacd55436ebc46b36bd61d4e43f89e6b45eb6`, with final pre-merge head `5e040f560f58fcdb90d21abfac1eb333ab3225a1`;
- [`R34-B1 — Owner-Operated Company Asset Cycle Execution / Evidence Runbook`](R34-b1-owner-operated-company-asset-cycle-runbook.md) `0.1.1` — `Prepared / NOT EXECUTED`.

No conflict with higher-authority canonical semantics is identified.

## 3. Current gate state

One gate blocker remains.

### B1 — real owner-operated evidence is absent — OPEN

No canonical evidence packet yet demonstrates the required first real owner-operated Company asset cycle across the R34 review dimensions.

The bounded R34-B1 execution/evidence runbook is now prepared and maps the actual Productive Workspace owner path: real Company-owned material selection/attestation → staged receipt → owner review → Governed Execution admission → accepted identity/provenance → same-runtime-root restart/reconstruction → genuine later retrieval/use → owner usability observations.

The runbook is preparation, not milestone evidence. CI, regression tests, synthetic fixtures, a prepared procedure and P10.03–P10.05/R34-D1/R34-D2 engineering evidence cannot substitute for the real owner-operated milestone evidence.

### B2 — restart-durable governed state — CLOSED

ADR-0002 selected the bounded remediation architecture and R34-D1 implemented the product-local owner-local durable-state adapter. R34-D2 then corrected the actual Productive Workspace composition so the existing P10.04/P10.05 owner path uses the durable admission/promotion pair and qualified the resulting recovery boundary.

The accepted and qualified path preserves:

- product-local owner-local persistence under the existing Workspace runtime root;
- immutable schema-versioned JSON records for committed and retry/uncertainty evidence;
- existing content-addressed material/output stores for retained bytes;
- exact reconstruction without replaying historical consequential effects;
- fail-closed corrupt, partial, conflicting or unknown-schema durable state;
- `TransientOutput` classification of the generated source after separate promotion;
- no platform-wide database mandate, new Kernel primitive, public persistence API or automatic Platform Capability promotion.

B2 is therefore technically closed by the D1 implementation plus D2 Productive Workspace wiring/qualification evidence. Closing B2 does **not** close R34 because B1 is independent and remains open.

## 4. Current R34 scope matrix

| Review area | Current evidence | Current finding |
| --- | --- | --- |
| Owner usability | P10.04 owner-facing UX + R34-B1 prepared runbook; no real owner cycle | `BLOCKED / NOT EVALUATED LIVE — B1` |
| Exact version / provenance | P10.03 semantics + D1/D2 restart reconstruction | `TECHNICAL PASS; real point-of-use evidence pending B1` |
| Authorization / Organizational Authority / Data Governance | RFC/Product Contract/implementation evidence + runbook boundary | `BLOCKED pending real point-of-use evidence — B1` |
| Data handling / logging | D2 metadata/content separation + structural controls + evidence minimization procedure | `TECHNICAL PASS; real evidence pending B1` |
| Partial failure / retry | semantic idempotency + durable lost-response/uncertainty evidence | `TECHNICAL PASS` |
| Generated output | P10.05 semantics + durable promotion reconstruction; source remains transient | `TECHNICAL PASS; real use/promotion evidence only where exercised` |
| Recovery / update compatibility | ADR-0002 + D1/D2 restart/restore/schema evidence | `B2 CLOSED` |
| Product/platform coupling | ADR-0002 + D1/D2 product-local implementation | no present architecture violation |

## 5. Findings

### F1 — live evidence remains mandatory

R34 is an owner-operated milestone gate. Synthetic execution or a prepared runbook cannot substitute for real organizational evidence.

**Severity:** gate blocker.  
**Disposition:** unresolved until one real bounded owner-operated cycle is executed and reviewed.

### F2 — durable/reconstructable state blocker is closed

R34-D1 implemented ADR-0002 durable storage and recovery semantics. R34-D2 corrected the actual Productive Workspace composition to use that durable pair and added qualification evidence for restart, idempotent lost-response retry, uncertainty preservation, backup/restore, corruption handling, owner-local filesystem safety and retained-byte reconstruction.

**Severity:** former gate blocker.  
**Disposition:** `CLOSED / TECHNICAL PASS`.

This disposition is deliberately bounded to the declared Productive Workspace owner-local persistence scope. It is not a Production, SLA, RTO/RPO, multi-process writer, public persistence API or lifecycle-promotion claim.

### F3 — no RFC amendment is required

Accepted RFCs intentionally remain technology-neutral while requiring reconstructability, portability, safe retry/replay and append-only Event meaning. ADR-0002 remains the correct subordinate decision level for the concrete Company-local persistence choice.

### F4 — ADR-0002 remains bounded

ADR-0002 is binding only for the declared Company Workspace scope. It does not create a platform-wide database choice, public persistence API, Stable Product Contract, Active Platform Capability or production-readiness claim.

### F5 — generated output classification remains correct

Generated output remains `TransientOutput` by default. Review alone does not canonicalize it. Promotion is a separate Governed Execution creating a new immutable governed version. D2 verifies that this separation survives restart/recovery and that the source remains transient after promotion.

For B1, genuine later use of an admitted asset is required. Generated-output promotion is only live B1 evidence where the real cycle actually exercises that separate operation; the runbook does not force an artificial promotion merely to manufacture evidence.

### F6 — historical recovery does not replay consequential effects

D2 verifies that a committed result can be reconstructed and returned after restart/lost response without creating a second canonical effect/Event. Recovery reconstructs admitted/promoted history; it does not re-run the historical mutation. Any genuinely new consequential effect still requires current applicable Governed Execution and gates.

### F7 — uncertainty and idempotency evidence survive restart

The existing semantic owner remains responsible for retry-token/fingerprint conflict decisions. D2 does not duplicate that semantic ownership in persistence. Instead it verifies that exact `retry_token`, immutable request `fingerprint` and typed `ConsequentialOutcome.UNCERTAIN` survive durable reconstruction, while the pre-effect journal remains available to block blind retry/rebinding until reconciliation.

### F8 — B1 execution is now bounded without weakening the gate

The R34-B1 runbook fixes the exact real-cycle procedure and evidence-minimization rules without creating evidence by declaration. It requires a real Company-owned material, explicit owner ownership/rights/handling attestation, actual Productive Workspace UI execution, exact immutable identifiers/digests, same-runtime-root restart/reconstruction and genuine later retrieval/use.

A third-party, licensed or otherwise merely authorized-for-use material may be valid in another governed scenario but cannot satisfy the current M10-alpha definition. The runbook also explicitly forbids committing credentials/unnecessary raw contents and forbids deliberate durable-state corruption merely to produce a live negative-path screenshot. If no safe real negative path occurs, the live packet must say so and may reference D2 for the engineering negative-path dimension rather than fabricate owner evidence.

## 6. R34-D2 qualification evidence

R34-D2 qualifies the exact existing Company admission/promotion owner path rather than introducing a new generic route or P10.08 entry point.

Productive composition evidence:

- `reference/python/p9_03_workspace.py` builds the existing P10.04/P10.05 path with `build_durable_company_governed_executors(settings.runtime_root)`;
- Company Asset Library and generated-output composition share the same durable admission dependency;
- generated-output promotion uses the paired durable promotion executor;
- existing P7.04 operation-specific grants and all RFC-0005 authority/gate semantics for **new** consequential effects remain unchanged.

Qualification evidence includes:

1. Productive Workspace actually uses the ADR-0002 durable pair;
2. committed admission survives restart with exact semantic state, Event, digest and provenance;
3. lost-response retry returns the durable committed result without repeating the effect/Event, including after the new-operation grant is revoked because this path reconstructs prior history rather than authorizing a new effect;
4. reviewed generated-output promotion survives restart while the source remains `TransientOutput` and `canonical_authority == False`;
5. coherent backup → restore of governed metadata, retained source/output bytes and generated-output review evidence reconstructs exact state and digests;
6. corrupt JSON, partial relational history and unknown schema fail closed;
7. unpublished stale temp files are not interpreted as committed state;
8. unsafe runtime/record symlinks fail closed and POSIX owner-local permissions remain restrictive;
9. governed metadata does not duplicate raw Company document bytes/content payloads;
10. exact typed uncertainty, retry token and fingerprint survive reconstruction;
11. unresolved pre-effect evidence survives restart and blocks blind retry/rebinding;
12. recovery reconstructs history and never treats historical replay as permission for a new effect.

At technical evidence head `434976f24c9767f0e6b79c12beb66afcd9e54975`, and again at final PR head `5e040f560f58fcdb90d21abfac1eb333ab3225a1` after canonical status synchronization:

- Productive Workspace CI — `PASS`;
- Reference Python CI — `PASS`;
- functional cross-review — no unresolved material technical objection.

PR #34 merged to canonical `main` at `152bacd55436ebc46b36bd61d4e43f89e6b45eb6`.

## 7. Functional cross-review state

The prior R34 review completed six functional iterations. ADR-0002 proposal separately completed five functional iterations with no unresolved material objection at proposal level. R34-D1/D2 implementation evidence was then cross-reviewed against the accepted boundaries. R34-B1 runbook preparation is a subordinate procedural step and does not constitute a seventh gate review or formal approval.

Current findings:

1. **Governance/authority:** persistence reconstructs prior governed state and does not create current Authorization or Organizational Authority. The runbook keeps Company ownership/right and consequential approval as owner decisions. `TECHNICAL PASS`; live evidence pending B1.
2. **Architecture/product boundary:** storage remains product-local and bounded; no new generic route/entry point or Platform Capability is created. `PASS`.
3. **Events/idempotency/recovery:** committed and uncertain evidence survives restart; historical effects are not replayed. `PASS`.
4. **Security/privacy:** governed metadata does not duplicate raw payloads or reusable credentials; filesystem paths/permissions/symlinks are fail-closed within the declared owner-local boundary; B1 evidence is explicitly minimized. `PASS`.
5. **Portability/migration:** current schema is explicit/open/versioned; unknown/future schema fails closed rather than being silently reinterpreted; no general migration compatibility beyond the qualified schema is claimed. `PASS for declared scope`.
6. **Concurrency:** implementation uses in-process locking only. No cross-process writer-safety claim is made. `PASS for declared single-process owner-local scope`.
7. **Usability/milestone integrity:** real owner validation remains absent even though the execution procedure is now prepared. `BLOCKED pending B1`.

No material technical objection remains for B2. The sole R34 gate blocker is B1.

## 8. Required remediation sequence

The current canonical sequence is:

```text
ADR-0002 Accepted ✓
        ↓
R34-D1 durable implementation ✓
        ↓
R34-D2 Productive Workspace wiring + qualification ✓
        ↓
B2 CLOSED ✓
        ↓
R34-B1 execution/evidence runbook Prepared ✓
        ↓
one real owner-operated Company asset cycle + evidence packet  ← NEXT
        ↓
R34 re-review
        ↓ PASS only if criteria satisfied
M10-alpha
```

P10.06 remains sequenced after M10-alpha on the canonical critical path. R34-D2 and the B1 runbook do not implement or claim P10.08.

## 9. Required real owner evidence packet

The exact execution/evidence procedure is now canonicalized in [`R34-B1 — Owner-Operated Company Asset Cycle Execution / Evidence Runbook`](R34-b1-owner-operated-company-asset-cycle-runbook.md).

One real bounded Company asset cycle must capture at minimum:

1. owner/operator and Organization context without secrets;
2. UTC timestamps plus environment/build/commit identity;
3. one real bounded Company-owned material plus explicit owner ownership/handling attestation without embedding unnecessary raw contents in governance markdown;
4. exact staged and admitted asset/version/checksum/provenance/ownership/Event references;
5. owner-visible review/list/detail and exact-version retrieval/use;
6. point-of-use Authorization, Organizational Authority and Data Governance evidence;
7. restart/recovery reconstruction of the exact real admitted result;
8. one safe negative/denied or partial-failure path where naturally/safely exercised; otherwise explicit `NOT EXERCISED IN REAL CYCLE` with D2 technical evidence reference;
9. generated transient output and separate promotion evidence only where the real cycle actually exercises those paths;
10. original admitted version/history unchanged as required;
11. owner UX observations and P0/P1/P2/P3 defect classification;
12. references to evidence artifacts rather than sensitive payload copies.

Synthetic data, fixture-only runs, automated CI or the prepared runbook cannot replace this packet.

## 10. Exit criteria

R34 may become `Closed / PASS` only when:

- B2 durable/recovery evidence remains valid;
- the real owner-operated evidence packet is reviewed;
- no unresolved P0/P1 exists in M10-alpha scope;
- no unresolved structural concern exists around ownership, exact-version pinning, provenance, data handling, authority/gates, retry/reconciliation or recovery;
- genuine later retrieval/use of the exact admitted version is demonstrated through Workspace;
- generated output remains transient unless separately promoted;
- the owner path is usable enough without product-specific semantic inflation into shared platform behavior.

Only then may the roadmap claim `M10-alpha`.

## 11. Current review decision

**R34:** `Executed / BLOCKED`  
**Gate verdict:** `NOT PASS`  
**Blocker B1:** `OPEN` — runbook prepared; real owner-operated Company asset-cycle execution/evidence absent  
**Blocker B2:** `CLOSED / TECHNICAL PASS` — ADR-0002 durable implementation + Productive Workspace wiring + restart/recovery qualification complete  
**ADR-0002:** `Accepted`  
**R34-D1:** merged/verified at `5f65061095094d9b58a4b293b2a5a8f01d88ad10`  
**R34-D2:** merged/verified via PR #34 at `152bacd55436ebc46b36bd61d4e43f89e6b45eb6`; final pre-merge head `5e040f560f58fcdb90d21abfac1eb333ab3225a1`  
**R34-B1 runbook:** `0.1.1 Prepared / NOT EXECUTED`  
**Next executable action:** owner selects one real qualifying Company-owned material and executes the prepared R34-B1 runbook through Productive Workspace; capture the resulting evidence packet and re-run R34  
**M10-alpha:** remains unclaimed  
**P10.06:** not started; remains after M10-alpha on the canonical critical path  
**RFC amendment required:** none  
**Product Contract lifecycle transition performed:** none (`Provisional 0.2.0` remains current)  
**Platform Capability promotion performed:** none  
**Production/SLA/RTO/RPO/multi-process claim:** none
# P9.11-F11 — Provisional transition record

Status: `Complete`
Version: `0.1.0`
Date: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` + `governance`
Parent finding: [`P9.11-F11 — Материалы компании и единый портфель проектов`](P9-11-F11-company-materials-and-project-portfolio.md)
Product Contract publication: [`Provisional 0.1.0`](../contracts/P9-11-F11-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.1.0.md)
Approval: [`DECISION-2026-08-26-P9-11-F11-PROVISIONAL-APPROVAL`](../governance/decisions/DECISION-2026-08-26-P9-11-F11-PROVISIONAL-APPROVAL.md)

## 1. Owner approval

The owner explicitly approved the exact F11 Product Contract boundary:

> `утверждаю Product Contract F11 v0.1.0 в Provisional scope`

The approved Draft is preserved by blob SHA `e1b65f4d38779b9b63300aec279f6062acfe3720`.

## 2. Transition result

Lifecycle transition:

`Draft 0.1.0 → Provisional 0.1.0`

The transition admits bounded implementation and real validation only within the exact approved scope. It does not close F11A/F11B, promote the contract to Stable, promote a Platform Capability, grant authority, or establish operational readiness.

## 3. Cross-review after approval

Functional re-review checked the approved boundary against:

- Constitution `1.2.0`;
- RFC-0001 architecture/product boundary;
- RFC-0004 Product Contract lifecycle and hidden-coupling prohibition;
- RFC-0005 Governed Execution for consequential canonical mutation;
- RFC-0006 provenance/telemetry distinction;
- RFC-0007 Observation/Knowledge separation;
- RFC-0008 Document/Artifact and Transient Output semantics;
- ADR-0001 Productive Workspace SPA/BFF/no-browser-authority topology.

Material objections: **none**.

One safety clarification from the prior design review remains binding: generic archives/uncontrolled nested active content are excluded; DOCX/PPTX may be admitted only as validated OOXML classes under the implementation allowlist, while macro-enabled Office formats remain excluded in the first slice.

This functional review is not implementation acceptance, owner-usefulness PASS, Product Contract Stable promotion or operational-readiness approval.

## 4. Current disposition

- F10A — bounded owner PASS for guide understandability;
- F11 Product Contract — `Provisional 0.1.0` after exact owner approval;
- F11A — implementation admitted, not yet PASS;
- F11B — implementation admitted, not yet PASS;
- P9.11 — remains Current;
- R32 — remains Locked.

## 5. Next canonical implementation sequence

1. F11A1 — safe Organization-scoped asset/template intake + immutable version/provenance path;
2. F11A2 — exact-version project-bound standard document generation, output transient by default;
3. F11B1 — explicit Company project registry and canonical roadmap/status source descriptors;
4. F11B2 — read-only adapters/projection with SHA/freshness/conflict/reconciliation/execution-target presentation;
5. governed Workspace release/deploy;
6. real owner validation of both journeys;
7. disposition further real friction before R32.

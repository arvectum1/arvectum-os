# P9.11-F11 — Implementation plan

Status: `In progress`
Date: `2026-08-26`
Task classification: `platform` + `product_contract` + `product_specific`
Product Contract: `P9.11-F11 Provisional 0.1.0`

Implementation slices:

1. `F11B1` explicit Company project registry from approved AC-301 PORT identities and canonical roadmap source descriptors;
2. `F11B2` read-only server-side portfolio projection with exact source SHA/freshness/error states and Workspace `/projects` UI;
3. `F11A1` safe Company material intake/list/version path reusing the P7.03 governed durable store only after exact F11 admission checks;
4. `F11A2` project-bound standard DOCX generation from an exact admitted DOCX template, producing a transient output with exact input provenance;
5. tests, release bump, governed deploy, real owner acceptance.

No roadmap write access, remote host execution, external sending/signing/publication, automatic Knowledge promotion, Stable API, or Platform Capability promotion is introduced.

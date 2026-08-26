from pathlib import Path

p = Path("docs/roadmap/ROADMAP.md")
text = p.read_text(encoding="utf-8")

def rep(old: str, new: str, count: int = 1) -> None:
    global text
    actual = text.count(old)
    if actual != count:
        raise SystemExit(f"ROADMAP replacement expected {count}, found {actual}: {old[:140]!r}")
    text = text.replace(old, new, count)

rep("Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.13.22`.",
    "Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.13.23`.")

rep("- [`P9.11-F11 — Материалы компании и единый портфель проектов`](../reviews/P9-11-F11-company-materials-and-project-portfolio.md) — `Product Contract Provisional 0.1.0; F11D-03 p9.11.9 remediation deployed; F11B owner recheck #3 pending`;",
    "- [`P9.11-F11 — Материалы компании и единый портфель проектов`](../reviews/P9-11-F11-company-materials-and-project-portfolio.md) — `bounded F11A/F11B owner PASS; Product Contract remains Provisional 0.1.0`;" )

rep("- [`P9.11-F11 selected-Mac deployment`](../reviews/P9-11-F11-LOCAL-DEPLOY-2026-08-26.md) — `Recorded / technical deployment PASS / owner validation pending`.",
    "- [`P9.11-F11 selected-Mac deployment`](../reviews/P9-11-F11-LOCAL-DEPLOY-2026-08-26.md) — `historical initial deployment PASS; later p9.11.9/p9.11.10 remediation and owner evidence supersede its pending-validation state`." )

rep("- **F11A/F11B disposition:** remediation deployed / **OWNER RECHECK PENDING**; canonical asset admission unavailable;",
    "- **F11A/F11B disposition:** **bounded owner PASS**; canonical asset admission remains unavailable and Product Contract remains Provisional 0.1.0;" )

rep("- R32 remains locked and therefore no M9 code-health PASS is claimed.",
    "- F11 p9.11.10 repair: PR #19 exact reviewed head `3b849e926346240011c010a58085a2cc57fe05f1` passed Productive Workspace CI `33015126576` and Reference Python CI `33015126605`; release-bearing merge `470878b8778fbac009d1ae52092879cf50d8f3f1`; selected-Mac P7.06 transaction `129845fa731fee12f2f9d2ada6894c42bc366b582835f8c299533d78565ad877` deployed exact p9.11.10 with healthy P7.02/P7.05, `CURRENT_EXACT`, `MANAGED_SPAWN_PROOF`, loopback-only listener, exact assets and launcher PASS;\n- real owner closure: F11B recheck #3 bounded PASS with only minor layout polish; F11A attempt #2 bounded PASS for template → generated DOCX → protected download → Word-open journey, with Word trust/provenance prompt retained as minor/non-blocking;\n- P9.11 is Complete / PASS; R32 is Current; no M9 code-health PASS is claimed before R32 completes." )

rep("> **P9.11 — perform real owner recheck #3 of F11B portfolio navigation stability and F11 usefulness on live p9.11.9. Attempt #2 remains FAIL; deployed remediation is not owner PASS. For F11A, owner validation remains pending and must use real Company material/template inputs while retaining StagedNonCanonical and TransientOutput boundaries. For F11B, verify useful cards remain visible across ordinary navigation and source-backed/reconciliation states, execution-location evidence and exact provenance remain truthful. Any material friction becomes the next P9.11 finding. P9.11 remains Current and R32 remains Locked.**",
    "> **R32 — M9 Productive Workspace Hardening + Milestone Code Health Gate. P9.11 is Complete / PASS from real owner sessions and material-friction disposition. Preserve existing security, authority, provenance, Product Contract and no-canonical-admission boundaries; do not infer M9/P9.12 closure until R32 itself passes.**" )

p.write_text(text, encoding="utf-8")
Path(".github/workflows/p9-11-owner-closure-cleanup.yml").unlink(missing_ok=True)
Path("scripts/p9_11_owner_closure_cleanup.py").unlink(missing_ok=True)

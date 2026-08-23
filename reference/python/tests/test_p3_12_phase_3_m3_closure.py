from __future__ import annotations

import unittest
from pathlib import Path

TEST_ROOT = Path(__file__).resolve().parent
REPO_ROOT = TEST_ROOT.parents[2]
DOCS_ROOT = REPO_ROOT / "docs"
CAPABILITY_IDS = ("CAP-001", "CAP-002", "CAP-003", "CAP-004")


class P312Phase3M3ClosureTests(unittest.TestCase):
    """Guards the bounded Phase 3 / M3 closure state without freezing later phases."""

    def test_canonical_closure_review_records_bounded_m3_pass(self) -> None:
        review = (
            DOCS_ROOT / "reviews" / "P3-12-phase-3-m3-closure-review.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Status: `Complete`", review)
        self.assertIn("Milestone: `M3 — Validated shared capability baseline` — `Achieved`", review)
        self.assertIn(
            "PASS — M3 achieved for the declared bounded shared-capability reference scope.",
            review,
        )
        self.assertIn("CAP-001 through CAP-004 remain `Incubating / Provisional`", review)
        self.assertIn("Phase 4 is **not automatically activated**", review)

    def test_phase_3_roadmap_is_closed_without_capability_promotion(self) -> None:
        roadmap = (
            DOCS_ROOT / "roadmap" / "PHASE-3-SHARED-PLATFORM-CAPABILITIES.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Status: `Complete`", roadmap)
        self.assertIn("Milestone: `M3 — Validated shared capability baseline` — `Achieved`", roadmap)
        self.assertIn(
            "| `P3.12` | Phase 3 / M3 closure review | 🟩 Complete / PASS | `██████████ 100%` |",
            roadmap,
        )
        for capability_id in CAPABILITY_IDS:
            self.assertNotIn(f"{capability_id} | `Active`", roadmap)

    def test_canonical_roadmap_preserves_m3_scope_as_later_phases_progress(self) -> None:
        roadmap = (DOCS_ROOT / "roadmap" / "ROADMAP.md").read_text(encoding="utf-8")

        rows = [
            line
            for line in roadmap.splitlines()
            if line.startswith("| `Phase ")
        ]
        phase_3_rows = [line for line in rows if line.startswith("| `Phase 3` |")]
        phase_4_rows = [line for line in rows if line.startswith("| `Phase 4` |")]
        self.assertEqual(len(phase_3_rows), 1)
        self.assertEqual(len(phase_4_rows), 1)
        phase_3 = phase_3_rows[0]
        self.assertIn("Shared Platform Capabilities", phase_3)
        self.assertIn("🟩 Complete", phase_3)
        self.assertIn("`M3` Validated shared capability baseline", phase_3)
        self.assertNotIn("Active", phase_3)
        # Preserve the exact M3 capability disposition without freezing a global
        # claim that no later, separately governed Platform Capability can ever
        # become Active. The catalog test below independently guards CAP-001..004.
        self.assertIn("CAP-001 through CAP-004 remain `Incubating / Provisional`", roadmap)
        self.assertIn(
            "Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.",
            roadmap,
        )

    def test_capability_catalog_preserves_exact_incubating_provisional_set(self) -> None:
        catalog = (
            DOCS_ROOT / "catalogs" / "PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md"
        ).read_text(encoding="utf-8")

        for capability_id in CAPABILITY_IDS:
            rows = [
                line
                for line in catalog.splitlines()
                if line.startswith(f"| `{capability_id}` |")
            ]
            self.assertEqual(len(rows), 1, capability_id)
            self.assertIn("| `Incubating` | `Provisional` |", rows[0])
            self.assertIn("M3 achieved", rows[0])
            self.assertNotIn("| `Active` |", rows[0])

    def test_root_readme_preserves_m3_scope_as_later_phases_progress(self) -> None:
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(
            "`Phase 3 — Shared Platform Capabilities` — `Complete`, `M3 — Validated shared capability baseline` achieved for the bounded shared-capability reference scope",
            readme,
        )
        self.assertIn("`Phase 4 — Workspace / Operator Experience`", readme)
        for capability_id in CAPABILITY_IDS:
            self.assertIn(f"`{capability_id}", readme)
        self.assertIn("`Incubating / Provisional`", readme)
        self.assertIn("do **not** promote any capability to `Active`", readme)
        self.assertIn("The P4.08 bounded Product Contract remains `Provisional 0.1.0`", readme)


if __name__ == "__main__":
    unittest.main()

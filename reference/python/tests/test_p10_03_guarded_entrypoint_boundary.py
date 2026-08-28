from __future__ import annotations

from pathlib import Path
import unittest


class P1003GuardedEntrypointBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[1]

    def test_product_and_workspace_modules_do_not_bypass_governed_asset_admission_guard(self) -> None:
        offenders: list[str] = []
        forbidden_call = "admit_organizational_asset("
        for package in ("workspace_app", "p10_03_company_asset_ref"):
            for path in (self.root / package).rglob("*.py"):
                if forbidden_call in path.read_text(encoding="utf-8"):
                    offenders.append(str(path.relative_to(self.root)))
        self.assertEqual(
            offenders,
            [],
            "product/workspace code must enter P10.03 canonical admission through the governed guard",
        )

    def test_guard_is_domain_neutral_and_delegates_once_to_semantic_owner(self) -> None:
        guard = (
            self.root
            / "arvectum_os_ref"
            / "organizational_asset_admission_guard.py"
        ).read_text(encoding="utf-8")
        self.assertEqual(guard.count("return admit_organizational_asset("), 1)
        self.assertNotIn("company.asset.", guard)
        self.assertNotIn("project_id", guard)
        self.assertNotIn("semantic_role", guard)


if __name__ == "__main__":
    unittest.main()

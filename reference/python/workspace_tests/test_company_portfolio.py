from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.company_portfolio import CompanyPortfolioError, SourceDocument
from workspace_app.company_portfolio_verified import VerifiedRuntimeCompanyPortfolioProvider


class FakeReader:
    def __init__(self, sources: dict[str, str]):
        self.sources = sources
        self.hashes: dict[tuple[str, str, str], str] = {}

    def read(self, descriptor):  # type: ignore[no-untyped-def]
        markdown = self.sources[descriptor.project_id]
        source = SourceDocument(
            descriptor.repository,
            descriptor.roadmap_path,
            "a" * 40,
            markdown,
            "2026-08-26T10:00:00Z",
        )
        self.hashes[(source.repository, source.path, source.commit_sha)] = hashlib.sha256(markdown.encode("utf-8")).hexdigest()
        return source

    def content_sha256_for(self, repository: str, path: str, commit_sha: str) -> str | None:
        return self.hashes.get((repository, path, commit_sha))


def _access() -> AccessContext:
    return AccessContext(
        organization=Identity("org", "ООО «Арвектум»", "local"),
        actor=Identity("actor", "owner", "ООО «Арвектум»"),
        principal_kind="human",
        credential_id="credential",
        grant_id="grant",
    )


def _registry(root: Path) -> Path:
    path = root / "registry.json"
    path.write_text(
        json.dumps(
            {
                "schema": "arvectum.company.workspace-project-registry/1",
                "authority": {"portfolio_identity": "AC-301", "git_primary": "2026-08-25 migration closure"},
                "projects": [
                    {
                        "id": "COMPANY",
                        "label": "Arvectum Company",
                        "kind": "company",
                        "disposition": "continue",
                        "repository": "arvectum1/arvectum-company",
                        "roadmap_path": "docs/roadmap/ROADMAP.md",
                        "adapter": "company-roadmap-v1",
                        "execution_targets": [],
                    },
                    {
                        "id": "PORT-007",
                        "label": "Data Platform",
                        "kind": "initiative",
                        "disposition": "clarify",
                        "repository": "arvectum1/data-platform",
                        "roadmap_path": None,
                        "adapter": "reconciliation-required",
                        "execution_targets": [],
                    },
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return path


class CompanyPortfolioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_company_portfolio_preserves_source_authority_hash_and_reconciliation(self) -> None:
        markdown = """# Roadmap\nСтатус: Active\nВерсия: 0.44.0\nТекущее каноническое действие: AC-505 — external evidence wait\n\n## 9. Available implementation paths now\n### A. Canonical empirical M5 path\n### B. Parallel business-evidence work\n"""
        provider = VerifiedRuntimeCompanyPortfolioProvider(
            _registry(self.root),
            reader=FakeReader({"COMPANY": markdown}),  # type: ignore[arg-type]
        )

        payload = provider.project(_access())
        self.assertEqual(
            payload["projection"],
            {
                "derived": True,
                "canonical_authority": False,
                "read_only": True,
                "roadmap_write_available": False,
                "remote_execution_available": False,
                "chat_or_model_memory_used_as_authority": False,
                "visibility_implies_permission": False,
            },
        )
        company, data_platform = payload["projects"]
        self.assertEqual(company["state"], "current-source-backed")
        self.assertEqual(company["source"]["commit_sha"], "a" * 40)
        self.assertEqual(company["source"]["content_sha256"], hashlib.sha256(markdown.encode("utf-8")).hexdigest())
        self.assertEqual(company["roadmap"]["current"], ["AC-505 — external evidence wait"])
        self.assertEqual(
            company["roadmap"]["branches"],
            ["A. Canonical empirical M5 path", "B. Parallel business-evidence work"],
        )
        self.assertEqual(company["execution_targets"], ["unspecified"])
        self.assertEqual(data_platform["state"], "reconciliation-required")
        self.assertIsNone(data_platform["source"])
        self.assertEqual(data_platform["roadmap"]["current"], [])

    def test_company_portfolio_isolates_source_failure_without_manufacturing_status(self) -> None:
        class SelectiveReader(FakeReader):
            def read(self, descriptor):  # type: ignore[no-untyped-def]
                if descriptor.project_id == "COMPANY":
                    raise CompanyPortfolioError("network detail must not leak")
                return super().read(descriptor)

        registry = json.loads(_registry(self.root).read_text(encoding="utf-8"))
        registry["projects"][1]["roadmap_path"] = "README.md"
        registry["projects"][1]["adapter"] = "generic-roadmap-v1"
        path = self.root / "registry-two.json"
        path.write_text(json.dumps(registry, ensure_ascii=False), encoding="utf-8")
        provider = VerifiedRuntimeCompanyPortfolioProvider(
            path,
            reader=SelectiveReader({"PORT-007": "# Data Platform\nStatus: Planned"}),  # type: ignore[arg-type]
        )
        payload = provider.project(_access())
        self.assertEqual(payload["projects"][0]["state"], "unavailable")
        self.assertEqual(payload["projects"][0]["roadmap"]["current"], [])
        self.assertEqual(payload["projects"][1]["state"], "current-source-backed")
        self.assertRegex(payload["projects"][1]["source"]["content_sha256"], r"^[0-9a-f]{64}$")

    def test_missing_content_hash_fails_closed_instead_of_claiming_source_backing(self) -> None:
        class NoHashReader(FakeReader):
            def content_sha256_for(self, repository: str, path: str, commit_sha: str) -> str | None:
                return None

        provider = VerifiedRuntimeCompanyPortfolioProvider(
            _registry(self.root),
            reader=NoHashReader({"COMPANY": "# Roadmap\nStatus: Active"}),  # type: ignore[arg-type]
        )
        card = provider.project(_access())["projects"][0]
        self.assertEqual(card["state"], "unavailable")
        self.assertIsNone(card["source"])
        self.assertEqual(card["roadmap"]["current"], [])


if __name__ == "__main__":
    unittest.main()

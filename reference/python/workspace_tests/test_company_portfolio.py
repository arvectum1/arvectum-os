from __future__ import annotations

import json
from pathlib import Path

from arvectum_os_ref.identity import Identity

from workspace_app.access import AccessContext
from workspace_app.company_portfolio import RuntimeCompanyPortfolioProvider, SourceDocument


class FakeReader:
    def __init__(self, sources: dict[str, str]):
        self.sources = sources

    def read(self, descriptor):  # type: ignore[no-untyped-def]
        markdown = self.sources[descriptor.project_id]
        return SourceDocument(
            descriptor.repository,
            descriptor.roadmap_path,
            "a" * 40,
            markdown,
            "2026-08-26T10:00:00Z",
        )


def _access() -> AccessContext:
    return AccessContext(
        organization=Identity("org", "ООО «Арвектум»", "local"),
        actor=Identity("actor", "owner", "ООО «Арвектум»"),
        principal_kind="human",
        credential_id="credential",
        grant_id="grant",
    )


def _registry(tmp_path: Path) -> Path:
    path = tmp_path / "registry.json"
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


def test_company_portfolio_preserves_source_authority_and_reconciliation(tmp_path: Path) -> None:
    markdown = """# Roadmap\nСтатус: Active\nВерсия: 0.44.0\nТекущее каноническое действие: AC-505 — external evidence wait\n\n## 9. Available implementation paths now\n### A. Canonical empirical M5 path\n### B. Parallel business-evidence work\n"""
    provider = RuntimeCompanyPortfolioProvider(
        _registry(tmp_path),
        reader=FakeReader({"COMPANY": markdown}),  # type: ignore[arg-type]
    )

    payload = provider.project(_access())

    assert payload["projection"] == {
        "derived": True,
        "canonical_authority": False,
        "read_only": True,
        "roadmap_write_available": False,
        "remote_execution_available": False,
        "chat_or_model_memory_used_as_authority": False,
        "visibility_implies_permission": False,
    }
    company, data_platform = payload["projects"]
    assert company["state"] == "current-source-backed"
    assert company["source"]["commit_sha"] == "a" * 40
    assert company["roadmap"]["current"] == ["AC-505 — external evidence wait"]
    assert company["roadmap"]["branches"] == [
        "A. Canonical empirical M5 path",
        "B. Parallel business-evidence work",
    ]
    assert company["execution_targets"] == ["unspecified"]
    assert data_platform["state"] == "reconciliation-required"
    assert data_platform["source"] is None
    assert data_platform["roadmap"]["current"] == []


def test_company_portfolio_does_not_fail_other_cards_when_one_source_is_unavailable(tmp_path: Path) -> None:
    class SelectiveReader(FakeReader):
        def read(self, descriptor):  # type: ignore[no-untyped-def]
            if descriptor.project_id == "COMPANY":
                raise RuntimeError("network detail must not leak")
            return super().read(descriptor)

    registry = json.loads(_registry(tmp_path).read_text(encoding="utf-8"))
    registry["projects"][1]["roadmap_path"] = "README.md"
    registry["projects"][1]["adapter"] = "generic-roadmap-v1"
    path = tmp_path / "registry-two.json"
    path.write_text(json.dumps(registry, ensure_ascii=False), encoding="utf-8")

    provider = RuntimeCompanyPortfolioProvider(
        path,
        reader=SelectiveReader({"PORT-007": "# Data Platform\nStatus: Planned"}),  # type: ignore[arg-type]
    )
    payload = provider.project(_access())

    # Runtime source failures must be isolated per project card and never manufacture status.
    assert payload["projects"][0]["state"] == "unavailable"
    assert payload["projects"][0]["roadmap"]["current"] == []
    assert payload["projects"][1]["state"] == "current-source-backed"

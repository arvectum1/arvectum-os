from __future__ import annotations

import hashlib
from typing import Any

from .access import AccessContext
from .company_portfolio import CompanyPortfolioError, RuntimeCompanyPortfolioProvider, _normalize


class VerifiedRuntimeCompanyPortfolioProvider(RuntimeCompanyPortfolioProvider):
    """F11B runtime projection with exact source content identity.

    The underlying reader resolves repository/path at an exact commit SHA. This
    projection additionally exposes SHA-256 of the exact UTF-8 roadmap bytes so
    the owner can distinguish a source identity from a merely recent fetch.
    """

    def project(self, access: AccessContext) -> dict[str, Any]:
        if not isinstance(access, AccessContext):
            raise CompanyPortfolioError("server-authorized AccessContext is required")
        cards: list[dict[str, Any]] = []
        for descriptor in self._descriptors:
            base = {
                "id": descriptor.project_id,
                "label": descriptor.label,
                "kind": descriptor.kind,
                "disposition": descriptor.disposition,
                "repository": descriptor.repository,
                "roadmap_path": descriptor.roadmap_path,
                "execution_targets": list(descriptor.execution_targets) or ["unspecified"],
                "authority_mode": "External Reference",
                "projection_authority": "non-authoritative",
            }
            empty_roadmap = {
                "status": None,
                "version": None,
                "source_updated": None,
                "done": [],
                "current": [],
                "branches": [],
                "unlocked": [],
                "blocked": [],
            }
            if descriptor.roadmap_path is None:
                cards.append(
                    {
                        **base,
                        "state": "reconciliation-required",
                        "message": "Канонический roadmap/status source для этого проекта пока не стандартизирован.",
                        "source": None,
                        "roadmap": empty_roadmap,
                    }
                )
                continue
            try:
                source = self.reader.read(descriptor)
                roadmap = _normalize(descriptor, source)
            except CompanyPortfolioError:
                cards.append(
                    {
                        **base,
                        "state": "unavailable",
                        "message": "Канонический источник сейчас недоступен; статус не подменяется кэшем или памятью модели.",
                        "source": None,
                        "roadmap": empty_roadmap,
                    }
                )
                continue
            source_bytes = source.markdown.encode("utf-8")
            cards.append(
                {
                    **base,
                    "state": "current-source-backed",
                    "message": "Данные прочитаны напрямую из зарегистрированного канонического roadmap source.",
                    "source": {
                        "repository": source.repository,
                        "path": source.path,
                        "commit_sha": source.commit_sha,
                        "content_sha256": hashlib.sha256(source_bytes).hexdigest(),
                        "fetched_at": source.fetched_at,
                        "freshness": "fresh-fetch",
                        "adapter": descriptor.adapter,
                    },
                    "roadmap": roadmap,
                }
            )
        return {
            "schema": "arvectum.workspace.company-portfolio/1",
            "generated_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat().replace("+00:00", "Z"),
            "product_contract": {"id": "P9.11-F11", "version": "0.1.0", "lifecycle": "Provisional"},
            "projection": {
                "derived": True,
                "canonical_authority": False,
                "read_only": True,
                "roadmap_write_available": False,
                "remote_execution_available": False,
                "chat_or_model_memory_used_as_authority": False,
                "visibility_implies_permission": False,
            },
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "cross_organization_aggregation": False,
            },
            "registry_authority": self._authority,
            "projects": cards,
        }


__all__ = ["VerifiedRuntimeCompanyPortfolioProvider"]

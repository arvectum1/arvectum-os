from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from .access import AccessContext
from .company_portfolio import (
    CompanyPortfolioError,
    GitHubRoadmapReader,
    ProjectDescriptor,
    RuntimeCompanyPortfolioProvider,
    SourceDocument,
)


class ContentHashingGitHubRoadmapReader(GitHubRoadmapReader):
    """Read exact canonical roadmap bytes and retain only their integrity digest."""

    def __init__(self, token: str | None = None, *, timeout_seconds: float = 8.0) -> None:
        super().__init__(token, timeout_seconds=timeout_seconds)
        self._hashes: dict[tuple[str, str, str], str] = {}

    def read(self, descriptor: ProjectDescriptor) -> SourceDocument:
        source = super().read(descriptor)
        key = (source.repository, source.path, source.commit_sha)
        self._hashes[key] = hashlib.sha256(source.markdown.encode("utf-8")).hexdigest()
        return source

    def content_sha256_for(self, repository: str, path: str, commit_sha: str) -> str | None:
        return self._hashes.get((repository, path, commit_sha))


class VerifiedRuntimeCompanyPortfolioProvider(RuntimeCompanyPortfolioProvider):
    """F11B projection requiring exact source content identity for every live card.

    The base provider remains responsible for allowlisting, exact commit resolution,
    normalization and fail-closed source states. This wrapper adds the Product
    Contract requirement that a successful source-backed projection expose a
    SHA-256 digest of the exact UTF-8 roadmap bytes used for normalization.
    """

    def __init__(
        self,
        registry_path: Path | None = None,
        *,
        reader: GitHubRoadmapReader | None = None,
    ) -> None:
        super().__init__(registry_path, reader=reader or ContentHashingGitHubRoadmapReader())

    def project(self, access: AccessContext) -> dict[str, Any]:
        payload = super().project(access)
        hash_lookup = getattr(self.reader, "content_sha256_for", None)
        for card in payload["projects"]:
            source = card.get("source")
            if card.get("state") != "current-source-backed" or not isinstance(source, dict):
                continue
            digest = None
            if callable(hash_lookup):
                digest = hash_lookup(source.get("repository"), source.get("path"), source.get("commit_sha"))
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                card["state"] = "unavailable"
                card["message"] = "Точная идентичность содержимого канонического источника не подтверждена."
                card["source"] = None
                card["roadmap"] = {
                    "status": None,
                    "version": None,
                    "source_updated": None,
                    "done": [],
                    "current": [],
                    "branches": [],
                    "unlocked": [],
                    "blocked": [],
                }
                continue
            source["content_sha256"] = digest
        return payload


__all__ = ["ContentHashingGitHubRoadmapReader", "VerifiedRuntimeCompanyPortfolioProvider"]

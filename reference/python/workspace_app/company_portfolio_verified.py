from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
from datetime import datetime, timezone
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


_CACHE_SCHEMA = "arvectum.workspace.company-portfolio-cache/1"
_DEFAULT_CACHE_MAX_AGE_SECONDS = 15 * 60


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _identity_text(identity: object) -> str:
    return f"{identity.namespace}:{identity.value}@{identity.scope}"  # type: ignore[attr-defined]


def _parse_utc(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def _secure_dir(path: Path) -> None:
    if path.exists() and (path.is_symlink() or not path.is_dir()):
        raise CompanyPortfolioError("portfolio cache directory must be a real directory")
    path.mkdir(parents=True, exist_ok=True)
    if path.is_symlink() or not path.is_dir():
        raise CompanyPortfolioError("portfolio cache directory must be a real directory")
    try:
        os.chmod(path, 0o700)
    except OSError as exc:
        raise CompanyPortfolioError("portfolio cache directory permissions could not be secured") from exc


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    _secure_dir(path.parent)
    if path.is_symlink():
        raise CompanyPortfolioError("portfolio cache target must not be a symlink")
    temporary = path.with_suffix(path.suffix + f".{secrets.token_hex(6)}.tmp")
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    try:
        temporary.write_text(data, encoding="utf-8")
        os.chmod(temporary, 0o600)
        os.replace(temporary, path)
        os.chmod(path, 0o600)
    except OSError as exc:
        raise CompanyPortfolioError("portfolio cache write failed") from exc
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass


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


class PortfolioProjectionCache:
    """Owner-local rebuildable cache for the last fully successful F11B projection.

    The cache is explicitly non-canonical. It exists only to keep ordinary Workspace
    navigation usable when GitHub is temporarily unavailable or rate-limited. Exact
    source SHA/content digest/fetched-at evidence is retained and the caller must label
    cached/stale presentation truthfully.
    """

    def __init__(self, runtime_root: Path, *, max_age_seconds: int = _DEFAULT_CACHE_MAX_AGE_SECONDS) -> None:
        if max_age_seconds < 1:
            raise ValueError("portfolio cache max age must be positive")
        self.root = runtime_root.expanduser() / "workspace-company-portfolio-cache"
        self.max_age_seconds = max_age_seconds

    def _path(self, access: AccessContext) -> Path:
        organization = _identity_text(access.organization)
        key = hashlib.sha256(organization.encode("utf-8")).hexdigest()
        return self.root / f"{key}.json"

    def load(self, access: AccessContext) -> dict[str, Any] | None:
        path = self._path(access)
        if not path.exists():
            return None
        try:
            if path.is_symlink() or not path.is_file():
                return None
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict):
            return None
        if payload.get("schema") != _CACHE_SCHEMA or payload.get("organization") != _identity_text(access.organization):
            return None
        if _parse_utc(payload.get("saved_at")) is None or not isinstance(payload.get("projection"), dict):
            return None
        return payload

    def fresh(self, cached: dict[str, Any]) -> bool:
        saved_at = _parse_utc(cached.get("saved_at"))
        if saved_at is None:
            return False
        age = (datetime.now(timezone.utc) - saved_at).total_seconds()
        return 0 <= age <= self.max_age_seconds

    def save(self, access: AccessContext, projection: dict[str, Any]) -> None:
        projects = projection.get("projects")
        if not isinstance(projects, list):
            raise CompanyPortfolioError("portfolio cache requires a complete projection")
        payload = {
            "schema": _CACHE_SCHEMA,
            "organization": _identity_text(access.organization),
            "saved_at": _utc_now(),
            "projection": projection,
        }
        _atomic_json(self._path(access), payload)


class VerifiedRuntimeCompanyPortfolioProvider(RuntimeCompanyPortfolioProvider):
    """F11B projection with exact content identity and resilient non-canonical caching."""

    def __init__(
        self,
        registry_path: Path | None = None,
        *,
        reader: GitHubRoadmapReader | None = None,
        cache_root: Path | None = None,
        cache_max_age_seconds: int = _DEFAULT_CACHE_MAX_AGE_SECONDS,
    ) -> None:
        super().__init__(registry_path, reader=reader or ContentHashingGitHubRoadmapReader())
        self.cache = PortfolioProjectionCache(cache_root, max_age_seconds=cache_max_age_seconds) if cache_root is not None else None

    def _validate_hashes(self, payload: dict[str, Any]) -> None:
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

    def _cache_compatible(self, cached: dict[str, Any]) -> dict[str, Any] | None:
        raw_projection = cached.get("projection")
        if not isinstance(raw_projection, dict):
            return None
        try:
            projection = json.loads(json.dumps(raw_projection, ensure_ascii=False))
        except (TypeError, ValueError):
            return None
        cards = projection.get("projects")
        if not isinstance(cards, list):
            return None
        by_id = {card.get("id"): card for card in cards if isinstance(card, dict) and isinstance(card.get("id"), str)}
        if len(by_id) != len(self._descriptors):
            return None
        for descriptor in self._descriptors:
            card = by_id.get(descriptor.project_id)
            if not isinstance(card, dict):
                return None
            if card.get("repository") != descriptor.repository or card.get("roadmap_path") != descriptor.roadmap_path:
                return None
            if descriptor.repository is None or descriptor.roadmap_path is None:
                if card.get("state") != "reconciliation-required":
                    return None
                continue
            source = card.get("source")
            if card.get("state") != "current-source-backed" or not isinstance(source, dict):
                return None
            if source.get("repository") != descriptor.repository or source.get("path") != descriptor.roadmap_path:
                return None
            if not isinstance(source.get("commit_sha"), str) or not re.fullmatch(r"[0-9a-f]{40}", source["commit_sha"]):
                return None
            if not isinstance(source.get("content_sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", source["content_sha256"]):
                return None
            if source.get("adapter") != descriptor.adapter:
                return None
        return projection

    def _present_cached(self, cached: dict[str, Any], *, stale: bool) -> dict[str, Any] | None:
        projection = self._cache_compatible(cached)
        if projection is None:
            return None
        projection["generated_at"] = _utc_now()
        for card in projection["projects"]:
            if card.get("state") != "current-source-backed":
                continue
            source = card["source"]
            if stale:
                card["state"] = "stale-cache"
                card["message"] = (
                    "Канонический источник сейчас недоступен; показана последняя успешно полученная сводка. "
                    "Она не является новым canonical state."
                )
                source["freshness"] = "stale-cache"
            else:
                card["state"] = "cached-source-backed"
                card["message"] = (
                    "Показана последняя успешно полученная сводка из локального non-canonical read-model cache; "
                    "точный источник и время получения сохранены."
                )
                source["freshness"] = "cached-within-window"
        return projection

    def _complete_source_refresh(self, payload: dict[str, Any]) -> bool:
        by_id = {card.get("id"): card for card in payload.get("projects", []) if isinstance(card, dict)}
        for descriptor in self._descriptors:
            if descriptor.repository is None or descriptor.roadmap_path is None:
                continue
            if by_id.get(descriptor.project_id, {}).get("state") != "current-source-backed":
                return False
        return True

    def _merge_stale_fallback(self, payload: dict[str, Any], cached: dict[str, Any] | None) -> dict[str, Any]:
        if cached is None:
            return payload
        cached_projection = self._cache_compatible(cached)
        if cached_projection is None:
            return payload
        cached_by_id = {
            card.get("id"): card
            for card in cached_projection.get("projects", [])
            if isinstance(card, dict) and isinstance(card.get("id"), str)
        }
        merged: list[dict[str, Any]] = []
        for card in payload["projects"]:
            if card.get("state") != "unavailable":
                merged.append(card)
                continue
            fallback = cached_by_id.get(card.get("id"))
            if not isinstance(fallback, dict) or fallback.get("state") != "current-source-backed":
                merged.append(card)
                continue
            stale_card = json.loads(json.dumps(fallback, ensure_ascii=False))
            stale_card["state"] = "stale-cache"
            stale_card["message"] = (
                "Канонический источник сейчас недоступен; показана последняя успешно полученная сводка. "
                "Точный SHA и время последнего успешного получения сохранены."
            )
            source = stale_card.get("source")
            if isinstance(source, dict):
                source["freshness"] = "stale-cache"
            merged.append(stale_card)
        payload["projects"] = merged
        return payload

    def project(self, access: AccessContext, *, force_refresh: bool = False) -> dict[str, Any]:
        if not isinstance(access, AccessContext):
            raise CompanyPortfolioError("server-authorized AccessContext is required")

        cached = self.cache.load(access) if self.cache is not None else None
        if cached is not None and not force_refresh and self.cache is not None and self.cache.fresh(cached):
            cached_projection = self._present_cached(cached, stale=False)
            if cached_projection is not None:
                return cached_projection

        payload = super().project(access)
        self._validate_hashes(payload)

        if self._complete_source_refresh(payload):
            if self.cache is not None:
                try:
                    self.cache.save(access, payload)
                except CompanyPortfolioError:
                    # The cache is a non-canonical availability optimization only.
                    # A cache persistence failure must not hide a successfully verified
                    # live External Reference projection from the authorized owner.
                    pass
            return payload

        return self._merge_stale_fallback(payload, cached)


__all__ = [
    "ContentHashingGitHubRoadmapReader",
    "PortfolioProjectionCache",
    "VerifiedRuntimeCompanyPortfolioProvider",
]

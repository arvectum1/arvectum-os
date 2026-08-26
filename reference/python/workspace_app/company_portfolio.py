from __future__ import annotations

import base64
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .access import AccessContext


class CompanyPortfolioError(RuntimeError):
    """The Company portfolio projection cannot be produced safely."""


_ALLOWED_TARGETS = frozenset(
    {
        "web",
        "mac-mini",
        "macbook",
        "windows-laptop",
        "windows-test-laptop",
        "linux-test-laptop",
        "unspecified",
    }
)
_REPOSITORY_RE = re.compile(r"^arvectum1/[A-Za-z0-9_.-]+$")
_PATH_RE = re.compile(r"^[A-Za-z0-9_./ -]+\.md$")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _plain(line: str) -> str:
    text = line.strip().strip("`|#*- ")
    text = text.replace("**", "").replace("__", "")
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    return " ".join(text.split())


def _bounded(text: str, limit: int = 640) -> str:
    value = " ".join(str(text).split())
    return value[:limit]


def _first_value(markdown: str, labels: tuple[str, ...]) -> str | None:
    for raw in markdown.splitlines():
        line = raw.strip()
        for label in labels:
            if line.lower().startswith(label.lower()):
                value = _plain(line[len(label) :].lstrip(" :—-"))
                if value:
                    return _bounded(value)
    return None


def _matching_lines(markdown: str, tokens: tuple[str, ...], *, limit: int = 6) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in markdown.splitlines():
        upper = raw.upper()
        if not any(token in upper for token in tokens):
            continue
        value = _plain(raw)
        if not value or len(value) < 4 or value in seen:
            continue
        seen.add(value)
        result.append(_bounded(value))
        if len(result) >= limit:
            break
    return result


def _section_headings(markdown: str, section_title: str, *, limit: int = 6) -> list[str]:
    active = False
    result: list[str] = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            if active:
                break
            active = section_title.lower() in line.lower()
            continue
        if active and line.startswith("### "):
            result.append(_bounded(_plain(line)))
            if len(result) >= limit:
                break
    return result


@dataclass(frozen=True, slots=True)
class ProjectDescriptor:
    project_id: str
    label: str
    kind: str
    disposition: str
    repository: str
    roadmap_path: str | None
    adapter: str
    execution_targets: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SourceDocument:
    repository: str
    path: str
    commit_sha: str
    markdown: str
    fetched_at: str


class GitHubRoadmapReader:
    """Server-side read-only GitHub source reader.

    Repository/path values come exclusively from the packaged allowlisted Company
    registry. Browser input cannot select an arbitrary repository or URL.
    """

    def __init__(self, token: str | None = None, *, timeout_seconds: float = 8.0) -> None:
        self.token = token if token is not None else os.getenv("ARVECTUM_WORKSPACE_GITHUB_TOKEN")
        self.timeout_seconds = timeout_seconds

    def _json(self, url: str) -> dict[str, Any]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "Arvectum-OS-Workspace-F11",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        try:
            with urlopen(Request(url, headers=headers), timeout=self.timeout_seconds) as response:  # noqa: S310 - fixed allowlisted host
                raw = response.read(2_000_000)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            raise CompanyPortfolioError("canonical roadmap source unavailable") from exc
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CompanyPortfolioError("canonical roadmap response invalid") from exc
        if not isinstance(payload, dict):
            raise CompanyPortfolioError("canonical roadmap response invalid")
        return payload

    def read(self, descriptor: ProjectDescriptor) -> SourceDocument:
        if not _REPOSITORY_RE.fullmatch(descriptor.repository):
            raise CompanyPortfolioError("repository outside F11 allowlist contract")
        if descriptor.roadmap_path is None or not _PATH_RE.fullmatch(descriptor.roadmap_path):
            raise CompanyPortfolioError("canonical roadmap source requires reconciliation")
        repository = descriptor.repository
        commit = self._json(f"https://api.github.com/repos/{repository}/commits/main")
        sha = commit.get("sha")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise CompanyPortfolioError("canonical source SHA unavailable")
        source = self._json(
            f"https://api.github.com/repos/{repository}/contents/{descriptor.roadmap_path}?ref={sha}"
        )
        encoded = source.get("content")
        encoding = source.get("encoding")
        if encoding != "base64" or not isinstance(encoded, str):
            raise CompanyPortfolioError("canonical roadmap bytes unavailable")
        try:
            markdown = base64.b64decode(encoded, validate=False).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise CompanyPortfolioError("canonical roadmap content invalid") from exc
        if len(markdown) > 1_500_000:
            raise CompanyPortfolioError("canonical roadmap exceeds bounded reader limit")
        return SourceDocument(repository, descriptor.roadmap_path, sha, markdown, _utc_now())


def _normalize(descriptor: ProjectDescriptor, source: SourceDocument) -> dict[str, Any]:
    markdown = source.markdown
    status = _first_value(markdown, ("Статус", "Status"))
    version = _first_value(markdown, ("Версия", "Version"))
    updated = _first_value(markdown, ("Обновлено", "Updated", "Дата фиксации"))
    current: list[str] = []
    branches: list[str] = []
    unlocked: list[str] = []
    blocked: list[str] = []
    done: list[str] = []

    if descriptor.adapter == "company-roadmap-v1":
        current_action = _first_value(markdown, ("Текущее каноническое действие",))
        if current_action:
            current.append(current_action)
        branches = _section_headings(markdown, "Available implementation paths now")
        unlocked = branches[:]
        blocked = _matching_lines(markdown, ("EXTERNAL EVIDENCE WAIT", " NOT ADMITTED", " LOCKED", " BLOCKED"))
        done = _matching_lines(markdown, ("COMPLETE / PASS",), limit=5)
    elif descriptor.adapter == "os-roadmap-v1":
        current = _matching_lines(markdown, ("P9.11", "NEXT CANONICAL ACTION"), limit=4)
        branches = _section_headings(markdown, "Parallel development lanes")
        unlocked = _matching_lines(markdown, (" AVAILABLE", " CURRENT", " READY"), limit=6)
        blocked = _matching_lines(markdown, (" LOCKED", " PENDING", " BLOCKED"), limit=6)
        done = _matching_lines(markdown, ("COMPLETE / PASS",), limit=5)
    elif descriptor.adapter == "proxy-roadmap-v1":
        current = _matching_lines(markdown, ("CURRENT",), limit=5)
        branches = _section_headings(markdown, "What can be done now")
        unlocked = _matching_lines(markdown, ("READY",), limit=6)
        blocked = _matching_lines(markdown, ("STOP-GATE", "PENDING", "HOLD"), limit=6)
        done = _matching_lines(markdown, ("DONE",), limit=5)
    elif descriptor.adapter == "creative-roadmap-v1":
        priority = _first_value(markdown, ("Current priority",))
        if priority:
            current.append(priority)
        if not current:
            current = _matching_lines(markdown, ("CURRENT PRIORITY",), limit=3)
        done = _matching_lines(markdown, ("DONE", "COMPLETE"), limit=4)
    else:
        current = _matching_lines(markdown, ("CURRENT", "ТЕКУЩ", "NEXT", "СЛЕДУЮЩ"), limit=5)
        unlocked = _matching_lines(markdown, ("READY", "ГОТОВО К", "ДОСТУП"), limit=5)
        blocked = _matching_lines(markdown, ("BLOCKED", "PENDING", "LOCKED", "ЗАБЛОК"), limit=5)
        done = _matching_lines(markdown, ("DONE", "COMPLETE", "PASS", "ГОТОВО"), limit=5)

    return {
        "status": status,
        "version": version,
        "source_updated": updated,
        "done": done,
        "current": current,
        "branches": branches,
        "unlocked": unlocked,
        "blocked": blocked,
    }


class RuntimeCompanyPortfolioProvider:
    def __init__(self, registry_path: Path | None = None, *, reader: GitHubRoadmapReader | None = None) -> None:
        self.registry_path = registry_path or Path(__file__).with_name("company_project_registry.json")
        self.reader = reader or GitHubRoadmapReader()
        self._descriptors, self._authority = self._load_registry()

    def _load_registry(self) -> tuple[tuple[ProjectDescriptor, ...], dict[str, str]]:
        try:
            payload = json.loads(self.registry_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CompanyPortfolioError("Company project registry unavailable") from exc
        if payload.get("schema") != "arvectum.company.workspace-project-registry/1":
            raise CompanyPortfolioError("Company project registry schema mismatch")
        authority = payload.get("authority")
        projects = payload.get("projects")
        if not isinstance(authority, dict) or not isinstance(projects, list):
            raise CompanyPortfolioError("Company project registry invalid")
        descriptors: list[ProjectDescriptor] = []
        ids: set[str] = set()
        for item in projects:
            if not isinstance(item, dict):
                raise CompanyPortfolioError("Company project registry invalid")
            targets = tuple(item.get("execution_targets", ()))
            if any(target not in _ALLOWED_TARGETS for target in targets):
                raise CompanyPortfolioError("Company execution target outside contract")
            descriptor = ProjectDescriptor(
                project_id=str(item.get("id", "")),
                label=str(item.get("label", "")),
                kind=str(item.get("kind", "")),
                disposition=str(item.get("disposition", "")),
                repository=str(item.get("repository", "")),
                roadmap_path=item.get("roadmap_path"),
                adapter=str(item.get("adapter", "")),
                execution_targets=targets,
            )
            if not descriptor.project_id or descriptor.project_id in ids or not descriptor.label:
                raise CompanyPortfolioError("Company project identity invalid")
            if not _REPOSITORY_RE.fullmatch(descriptor.repository):
                raise CompanyPortfolioError("Company repository locator invalid")
            ids.add(descriptor.project_id)
            descriptors.append(descriptor)
        return tuple(descriptors), {str(k): str(v) for k, v in authority.items()}

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
            if descriptor.roadmap_path is None:
                cards.append(
                    {
                        **base,
                        "state": "reconciliation-required",
                        "message": "Канонический roadmap/status source для этого проекта пока не стандартизирован.",
                        "source": None,
                        "roadmap": {"status": None, "version": None, "source_updated": None, "done": [], "current": [], "branches": [], "unlocked": [], "blocked": []},
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
                        "roadmap": {"status": None, "version": None, "source_updated": None, "done": [], "current": [], "branches": [], "unlocked": [], "blocked": []},
                    }
                )
                continue
            cards.append(
                {
                    **base,
                    "state": "current-source-backed",
                    "message": "Данные прочитаны напрямую из зарегистрированного канонического roadmap source.",
                    "source": {
                        "repository": source.repository,
                        "path": source.path,
                        "commit_sha": source.commit_sha,
                        "fetched_at": source.fetched_at,
                        "freshness": "fresh-fetch",
                        "adapter": descriptor.adapter,
                    },
                    "roadmap": roadmap,
                }
            )
        return {
            "schema": "arvectum.workspace.company-portfolio/1",
            "generated_at": _utc_now(),
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


__all__ = ["CompanyPortfolioError", "GitHubRoadmapReader", "RuntimeCompanyPortfolioProvider"]

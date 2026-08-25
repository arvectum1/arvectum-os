from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Callable, Protocol
from urllib.parse import quote

import p7_05_operational_visibility as p705
from .access import AccessContext


class AttentionProjectionError(RuntimeError):
    """Fail-closed error while producing the non-authoritative My Work projection."""


class AttentionKind(str, Enum):
    WAITING_APPROVAL = "waiting-approval"
    WAITING_INPUT = "waiting-input"
    RECONCILIATION_REQUIRED = "reconciliation-required"
    GUARDED_ACTION_FAILED = "guarded-action-failed"
    RECOVERABLE_SYSTEM_CONDITION = "recoverable-system-condition"
    RECENT_OUTCOME = "recent-outcome"
    INFORMATIONAL = "informational"


class AttentionGroup(str, Enum):
    DECISION_REQUIRED = "decision-required"
    BLOCKED_FAILED = "blocked-failed"
    RECONCILIATION_REQUIRED = "reconciliation-required"
    RECENT_OUTCOME = "recent-outcome"
    INFORMATIONAL = "informational"


class AttentionUrgency(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ProjectionFreshness(str, Enum):
    FRESH = "fresh"
    STALE = "stale"
    DEGRADED = "degraded"


_KIND_GROUP = {
    AttentionKind.WAITING_APPROVAL: AttentionGroup.DECISION_REQUIRED,
    AttentionKind.WAITING_INPUT: AttentionGroup.DECISION_REQUIRED,
    AttentionKind.RECONCILIATION_REQUIRED: AttentionGroup.RECONCILIATION_REQUIRED,
    AttentionKind.GUARDED_ACTION_FAILED: AttentionGroup.BLOCKED_FAILED,
    AttentionKind.RECOVERABLE_SYSTEM_CONDITION: AttentionGroup.BLOCKED_FAILED,
    AttentionKind.RECENT_OUTCOME: AttentionGroup.RECENT_OUTCOME,
    AttentionKind.INFORMATIONAL: AttentionGroup.INFORMATIONAL,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _bounded_text(value: str, *, field: str, limit: int = 240) -> str:
    if not isinstance(value, str):
        raise AttentionProjectionError(f"{field} must be text")
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > limit or "\x00" in normalized:
        raise AttentionProjectionError(f"{field} is empty or outside the bounded presentation contract")
    return normalized


def _attention_id(source_fingerprint: str) -> str:
    fingerprint = _bounded_text(source_fingerprint, field="source_fingerprint", limit=1024)
    return hashlib.sha256(fingerprint.encode("utf-8")).hexdigest()[:20]


@dataclass(frozen=True, slots=True)
class AttentionItem:
    attention_id: str
    kind: AttentionKind
    urgency: AttentionUrgency
    title: str
    reason: str
    source_label: str
    next_step: str
    evidence_mode: str = "live"
    observed_at: str | None = None
    technical_evidence_available: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.kind, AttentionKind) or not isinstance(self.urgency, AttentionUrgency):
            raise AttentionProjectionError("attention kind/urgency must be explicit")
        if not isinstance(self.attention_id, str) or len(self.attention_id) != 20 or any(
            ch not in "0123456789abcdef" for ch in self.attention_id
        ):
            raise AttentionProjectionError("attention_id must be a bounded opaque identifier")
        for field in ("title", "reason", "source_label", "next_step"):
            _bounded_text(getattr(self, field), field=field)
        if self.evidence_mode not in {"live", "scenario"}:
            raise AttentionProjectionError("evidence_mode must be live or scenario")
        if self.observed_at is not None:
            _bounded_text(self.observed_at, field="observed_at", limit=64)
        if not isinstance(self.technical_evidence_available, bool):
            raise AttentionProjectionError("technical_evidence_available must be explicit")

    @property
    def group(self) -> AttentionGroup:
        return _KIND_GROUP[self.kind]

    @property
    def open_href(self) -> str:
        return f"/my-work?focus={quote(self.attention_id, safe='')}"

    def to_payload(self) -> dict[str, object]:
        return {
            "id": self.attention_id,
            "kind": self.kind.value,
            "group": self.group.value,
            "urgency": self.urgency.value,
            "title": self.title,
            "reason": self.reason,
            "source": self.source_label,
            "next_step": self.next_step,
            "evidence_mode": self.evidence_mode,
            "observed_at": self.observed_at,
            "open_href": self.open_href,
            "interaction": "inspect-only",
            "technical_evidence_available": self.technical_evidence_available,
            "authority_provided": False,
        }


@dataclass(frozen=True, slots=True)
class ProjectionHealth:
    state: ProjectionFreshness
    code: str
    message: str
    observed_at: str
    heartbeat_age_seconds: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.state, ProjectionFreshness):
            raise AttentionProjectionError("projection health state must be explicit")
        _bounded_text(self.code, field="health.code", limit=80)
        _bounded_text(self.message, field="health.message")
        _bounded_text(self.observed_at, field="health.observed_at", limit=64)
        if self.heartbeat_age_seconds is not None and not isinstance(self.heartbeat_age_seconds, (int, float)):
            raise AttentionProjectionError("heartbeat age must be numeric when present")

    def to_payload(self) -> dict[str, object]:
        return {
            "state": self.state.value,
            "code": self.code,
            "message": self.message,
            "observed_at": self.observed_at,
            "heartbeat_age_seconds": self.heartbeat_age_seconds,
        }


@dataclass(frozen=True, slots=True)
class AttentionProjection:
    generated_at: str
    health: ProjectionHealth
    items: tuple[AttentionItem, ...]

    def __post_init__(self) -> None:
        _bounded_text(self.generated_at, field="generated_at", limit=64)
        if not isinstance(self.health, ProjectionHealth):
            raise AttentionProjectionError("health must be a ProjectionHealth")
        if not isinstance(self.items, tuple) or any(not isinstance(item, AttentionItem) for item in self.items):
            raise AttentionProjectionError("items must be immutable typed attention items")
        ids = tuple(item.attention_id for item in self.items)
        if len(set(ids)) != len(ids):
            raise AttentionProjectionError("attention projection cannot contain duplicate item ids")

    def to_payload(self) -> dict[str, object]:
        return {
            "schema": "arvectum.workspace.my-work/1",
            "generated_at": self.generated_at,
            "projection": {
                "derived": True,
                "canonical_authority": False,
                "organizational_authority_provided": False,
                "consequential_action_available": False,
                "visibility_implies_permission": False,
            },
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "denied_item_counts_exposed": False,
            },
            "health": self.health.to_payload(),
            "items": [item.to_payload() for item in self.items],
        }


class AttentionProvider(Protocol):
    def project(self, access: AccessContext) -> AttentionProjection:
        ...


HealthReader = Callable[[Path], p705.HealthStatus]


def scenario_item(
    *,
    source_fingerprint: str,
    kind: AttentionKind,
    urgency: AttentionUrgency,
    title: str,
    reason: str,
    source_label: str,
    next_step: str,
    observed_at: str | None = None,
) -> AttentionItem:
    """Build visibly controlled acceptance evidence; never use this as a live-state claim."""
    return AttentionItem(
        attention_id=_attention_id(f"scenario:{source_fingerprint}"),
        kind=kind,
        urgency=urgency,
        title=title,
        reason=reason,
        source_label=source_label,
        next_step=next_step,
        evidence_mode="scenario",
        observed_at=observed_at,
        technical_evidence_available=False,
    )


def _runtime_health(status: p705.HealthStatus, observed_at: str) -> ProjectionHealth:
    if status.state == "healthy":
        return ProjectionHealth(
            ProjectionFreshness.FRESH,
            status.code,
            "Attention sources were evaluated against the current healthy persistent runtime.",
            observed_at,
            status.heartbeat_age_seconds,
        )
    freshness = ProjectionFreshness.STALE if status.code == "HEARTBEAT_STALE" else ProjectionFreshness.DEGRADED
    message = (
        "The persistent runtime heartbeat is stale. Work items are withheld until current source state can be revalidated."
        if freshness is ProjectionFreshness.STALE
        else "A required persistent runtime source is unavailable or degraded. Work items are withheld until source health is restored."
    )
    return ProjectionHealth(freshness, status.code, message, observed_at, status.heartbeat_age_seconds)


def _runtime_condition(status: p705.HealthStatus, observed_at: str) -> AttentionItem:
    stale = status.code == "HEARTBEAT_STALE"
    return AttentionItem(
        attention_id=_attention_id(f"runtime-health:{status.code}"),
        kind=AttentionKind.RECOVERABLE_SYSTEM_CONDITION,
        urgency=AttentionUrgency.HIGH if status.state == "down" else AttentionUrgency.MEDIUM,
        title="Workspace source is not current" if stale else "Workspace source needs attention",
        reason=(
            "The persistent runtime heartbeat is stale, so derived work items cannot be presented as current."
            if stale
            else "A required persistent runtime source is unavailable or degraded, so the queue is fail-closed."
        ),
        source_label="Arvectum OS persistent runtime",
        next_step="Restore persistent runtime health, then refresh My Work before acting on derived queue state.",
        observed_at=observed_at,
        technical_evidence_available=False,
    )


class RuntimeAttentionProvider:
    """Bounded live P9.04 adapter over already-governed/private runtime evidence.

    The adapter never scans opaque governed payloads for guessed business statuses.
    UI4 preflight evidence is deliberately excluded: it proves no concrete
    owner-relevant work outcome, so Waiting governance gates cannot create work.
    """

    def __init__(
        self,
        runtime_root: Path,
        *,
        health_reader: HealthReader = p705.classify_health,
    ) -> None:
        self.runtime_root = runtime_root.expanduser()
        self.health_reader = health_reader

    def project(self, access: AccessContext) -> AttentionProjection:
        if not isinstance(access, AccessContext):
            raise AttentionProjectionError("server-authorized AccessContext is required")
        observed_at = _utc_now()
        status = self.health_reader(self.runtime_root)
        health = _runtime_health(status, observed_at)
        if health.state is not ProjectionFreshness.FRESH:
            return AttentionProjection(observed_at, health, (_runtime_condition(status, observed_at),))

        return AttentionProjection(observed_at, health, ())


__all__ = [
    "AttentionGroup",
    "AttentionItem",
    "AttentionKind",
    "AttentionProjection",
    "AttentionProjectionError",
    "AttentionProvider",
    "AttentionUrgency",
    "ProjectionFreshness",
    "ProjectionHealth",
    "RuntimeAttentionProvider",
    "scenario_item",
]

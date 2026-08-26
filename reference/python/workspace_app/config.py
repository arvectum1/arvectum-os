from __future__ import annotations

import ipaddress
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import SplitResult, urlsplit


class ConfigurationError(RuntimeError):
    pass


def _truthy(name: str, default: bool = False) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _positive_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    if value is None:
        return default
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be an integer") from exc
    if parsed <= 0:
        raise ConfigurationError(f"{name} must be positive")
    return parsed


def _is_loopback(host: str) -> bool:
    normalized = host.strip("[]").lower()
    if normalized == "localhost":
        return True
    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


def _copilot_endpoint() -> str | None:
    value = os.environ.get("ARVECTUM_WORKSPACE_COPILOT_MODEL_URL")
    if value is None or not value.strip():
        return None
    endpoint = value.strip()
    parsed = urlsplit(endpoint)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or not parsed.path:
        raise ConfigurationError("ARVECTUM_WORKSPACE_COPILOT_MODEL_URL must be an absolute HTTP(S) endpoint")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ConfigurationError("Copilot model endpoint must not embed credentials, query parameters, or fragments")
    if not _is_loopback(parsed.hostname):
        raise ConfigurationError("P9.08 Copilot model endpoint is restricted to loopback in the current owner-operated contour")
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ConfigurationError("Copilot model endpoint port is invalid")
    return endpoint


def _origin_parts(origin: str) -> SplitResult:
    parsed = urlsplit(origin)
    if parsed.scheme not in {"http", "https"}:
        raise ConfigurationError("ARVECTUM_WORKSPACE_ORIGIN must be an origin only")
    if not parsed.hostname or parsed.path not in {"", "/"}:
        raise ConfigurationError("ARVECTUM_WORKSPACE_ORIGIN must be an origin only")
    if parsed.query or parsed.fragment:
        raise ConfigurationError("ARVECTUM_WORKSPACE_ORIGIN must be an origin only")
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ConfigurationError("ARVECTUM_WORKSPACE_ORIGIN port is invalid")
    return parsed


def _validate_bind_profile(
    parsed: SplitResult,
    bind_host: str,
    bind_port: int,
    allow_loopback_http: bool,
) -> None:
    if not 1 <= bind_port <= 65535:
        raise ConfigurationError("ARVECTUM_WORKSPACE_BIND_PORT is invalid")
    if parsed.scheme == "http":
        if not allow_loopback_http:
            raise ConfigurationError("HTTP requires the explicit loopback-only exception")
        if not _is_loopback(parsed.hostname or "") or not _is_loopback(bind_host):
            raise ConfigurationError("HTTP Workspace profile is permitted only on loopback")
        return
    if not _is_loopback(bind_host) and _truthy("ARVECTUM_WORKSPACE_REQUIRE_LOOPBACK_BIND", True):
        raise ConfigurationError("non-loopback bind requires an explicitly reviewed deployment profile")


def _allowed_hosts(origin_host: str) -> tuple[str, ...]:
    configured_hosts = os.environ.get("ARVECTUM_WORKSPACE_ALLOWED_HOSTS", origin_host)
    allowed = tuple(sorted({item.strip().lower() for item in configured_hosts.split(",") if item.strip()}))
    if not allowed:
        raise ConfigurationError("at least one allowed Host is required")
    if origin_host.lower() not in allowed:
        raise ConfigurationError("public origin Host must be allowlisted")
    return allowed


def _runtime_root() -> Path:
    default = Path.home() / "Library" / "Application Support" / "ArvectumOS" / "persistent-internal"
    return Path(os.environ.get("ARVECTUM_P7_02_ROOT", str(default))).expanduser()


def _display_labels() -> tuple[str, str]:
    organization = os.environ.get("ARVECTUM_WORKSPACE_ORGANIZATION_LABEL", "ООО «Арвектум»").strip()
    actor = os.environ.get("ARVECTUM_WORKSPACE_ACTOR_LABEL", "Owner operator").strip()
    if not organization or not actor:
        raise ConfigurationError("Organization and actor display labels must be non-empty")
    return organization, actor


def _session_expiry() -> tuple[int, int]:
    idle = _positive_int("ARVECTUM_WORKSPACE_SESSION_IDLE_SECONDS", 1800)
    absolute = _positive_int("ARVECTUM_WORKSPACE_SESSION_ABSOLUTE_SECONDS", 28800)
    if idle > absolute:
        raise ConfigurationError("session idle expiry cannot exceed absolute expiry")
    return idle, absolute


def _copilot_profile() -> tuple[str | None, str, int]:
    model_url = _copilot_endpoint()
    model_name = os.environ.get("ARVECTUM_WORKSPACE_COPILOT_MODEL", "local-grounded-model").strip()
    if not model_name or len(model_name) > 160:
        raise ConfigurationError("ARVECTUM_WORKSPACE_COPILOT_MODEL must be bounded non-empty text")
    timeout = _positive_int("ARVECTUM_WORKSPACE_COPILOT_MODEL_TIMEOUT_SECONDS", 20)
    if timeout > 120:
        raise ConfigurationError("Copilot model timeout exceeds the bounded P9.08 profile")
    return model_url, model_name, timeout


@dataclass(frozen=True)
class WorkspaceSettings:
    runtime_root: Path
    public_origin: str
    bind_host: str
    bind_port: int
    allowed_hosts: tuple[str, ...]
    organization_label: str
    actor_label: str
    session_idle_seconds: int
    session_absolute_seconds: int
    allow_loopback_http: bool
    copilot_model_url: str | None = None
    copilot_model_name: str = "local-grounded-model"
    copilot_model_timeout_seconds: int = 20

    @property
    def secure_cookie(self) -> bool:
        return urlsplit(self.public_origin).scheme == "https"

    @property
    def cookie_name(self) -> str:
        return "__Host-arvectum_workspace_session" if self.secure_cookie else "arvectum_workspace_session"

    @classmethod
    def from_env(cls) -> "WorkspaceSettings":
        origin = os.environ.get("ARVECTUM_WORKSPACE_ORIGIN", "http://127.0.0.1:8769").strip()
        bind_host = os.environ.get("ARVECTUM_WORKSPACE_BIND_HOST", "127.0.0.1").strip()
        bind_port = _positive_int("ARVECTUM_WORKSPACE_BIND_PORT", 8769)
        allow_loopback_http = _truthy("ARVECTUM_WORKSPACE_ALLOW_LOOPBACK_HTTP", True)

        parsed = _origin_parts(origin)
        _validate_bind_profile(parsed, bind_host, bind_port, allow_loopback_http)
        allowed_hosts = _allowed_hosts(parsed.netloc)
        organization_label, actor_label = _display_labels()
        idle, absolute = _session_expiry()
        copilot_model_url, copilot_model_name, copilot_model_timeout_seconds = _copilot_profile()

        return cls(
            runtime_root=_runtime_root(),
            public_origin=origin.rstrip("/"),
            bind_host=bind_host,
            bind_port=bind_port,
            allowed_hosts=allowed_hosts,
            organization_label=organization_label,
            actor_label=actor_label,
            session_idle_seconds=idle,
            session_absolute_seconds=absolute,
            allow_loopback_http=allow_loopback_http,
            copilot_model_url=copilot_model_url,
            copilot_model_name=copilot_model_name,
            copilot_model_timeout_seconds=copilot_model_timeout_seconds,
        )


__all__ = ["ConfigurationError", "WorkspaceSettings", "_is_loopback"]

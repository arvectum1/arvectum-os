"""ADR-0002 product-local durable governed state for Company Workspace.

This module persists only already-governed P10.03/P10.05 semantic results and
retry evidence.  It does not grant authority, replay consequential effects, or
create a platform-wide storage contract.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.document_artifact_governance import (
    AdmittedDocumentVersion,
    ArtifactContent,
    ArtifactState,
    HandlingConstraints,
)
from arvectum_os_ref.event_provenance import CanonicalEvent
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.organizational_asset_admission import (
    CommittedOrganizationalAssetAdmission,
    OrganizationalAssetAdmissionState,
)
from arvectum_os_ref.reviewed_generated_output_promotion import (
    CommittedReviewedGeneratedOutputPromotion,
    ExactGeneratedOutputSource,
    ReviewedGeneratedOutputPromotionState,
)
from arvectum_os_ref.runtime_consistency import (
    ConsequentialAttempt,
    ConsequentialOutcome,
    RetrySemantics,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass


_SCHEMA = "arvectum.company-governed-state"
_SCHEMA_VERSION = 1
_KINDS = frozenset({"admission", "promotion"})


class CompanyGovernedStateError(RuntimeError):
    """Durable governed state is absent, unsafe, corrupt, or inconsistent."""


_DATACLASS_TYPES = (
    Identity,
    OrganizationScope,
    Principal,
    ActorContext,
    ExternalAuthorityContract,
    CanonicalRecord,
    HandlingConstraints,
    ArtifactContent,
    AdmittedDocumentVersion,
    CanonicalEvent,
    ConsequentialAttempt,
    CommittedOrganizationalAssetAdmission,
    ExactGeneratedOutputSource,
    CommittedReviewedGeneratedOutputPromotion,
)
_DATACLASS_REGISTRY = {value.__name__: value for value in _DATACLASS_TYPES}
_ENUM_TYPES = (
    AuthorityMode,
    ArtifactState,
    RetrySemantics,
    ConsequentialOutcome,
    OperationSideEffectClass,
)
_ENUM_REGISTRY = {value.__name__: value for value in _ENUM_TYPES}


def _encode(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise CompanyGovernedStateError("durable governed state refuses naive datetime values")
        return {"$datetime": value.isoformat()}
    if isinstance(value, Enum):
        enum_type = type(value)
        if enum_type not in _ENUM_TYPES:
            raise CompanyGovernedStateError(f"unsupported durable enum type: {enum_type.__name__}")
        return {"$enum": enum_type.__name__, "value": value.value}
    if isinstance(value, tuple):
        return {"$tuple": [_encode(item) for item in value]}
    if isinstance(value, list):
        return [_encode(item) for item in value]
    value_type = type(value)
    if is_dataclass(value) and value_type in _DATACLASS_TYPES:
        return {
            "$type": value_type.__name__,
            "fields": {field.name: _encode(getattr(value, field.name)) for field in fields(value)},
        }
    raise CompanyGovernedStateError(f"unsupported durable governed-state value: {value_type.__name__}")


def _decode(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, list):
        return [_decode(item) for item in value]
    if not isinstance(value, dict):
        raise CompanyGovernedStateError("durable governed-state value has unsupported JSON shape")
    if set(value) == {"$datetime"}:
        raw = value["$datetime"]
        if not isinstance(raw, str):
            raise CompanyGovernedStateError("durable datetime encoding is invalid")
        try:
            parsed = datetime.fromisoformat(raw)
        except ValueError as exc:
            raise CompanyGovernedStateError("durable datetime encoding is invalid") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise CompanyGovernedStateError("durable datetime must remain timezone-aware")
        return parsed
    if set(value) == {"$tuple"}:
        raw = value["$tuple"]
        if not isinstance(raw, list):
            raise CompanyGovernedStateError("durable tuple encoding is invalid")
        return tuple(_decode(item) for item in raw)
    if set(value) == {"$enum", "value"}:
        name = value["$enum"]
        raw = value["value"]
        enum_type = _ENUM_REGISTRY.get(name) if isinstance(name, str) else None
        if enum_type is None:
            raise CompanyGovernedStateError("unknown durable enum schema")
        try:
            return enum_type(raw)
        except (TypeError, ValueError) as exc:
            raise CompanyGovernedStateError("durable enum value is invalid") from exc
    if set(value) == {"$type", "fields"}:
        name = value["$type"]
        raw_fields = value["fields"]
        cls = _DATACLASS_REGISTRY.get(name) if isinstance(name, str) else None
        if cls is None or not isinstance(raw_fields, dict):
            raise CompanyGovernedStateError("unknown durable dataclass schema")
        expected = {field.name for field in fields(cls)}
        if set(raw_fields) != expected:
            raise CompanyGovernedStateError(f"durable {name} fields do not match the supported schema")
        decoded = {key: _decode(raw_fields[key]) for key in expected}
        try:
            return cls(**decoded)
        except (TypeError, ValueError) as exc:
            raise CompanyGovernedStateError(f"durable {name} payload violates semantic invariants") from exc
    raise CompanyGovernedStateError("unknown durable governed-state tagged value")


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:24]


class CompanyGovernedStateStore:
    """Owner-local append-only JSON realization of ADR-0002 for Company Workspace."""

    def __init__(self, runtime_root: Path) -> None:
        if not isinstance(runtime_root, Path):
            raise TypeError("Company governed-state runtime_root must be a Path")
        self.runtime_root = runtime_root.expanduser()
        if self.runtime_root.is_symlink():
            raise CompanyGovernedStateError("Company governed-state runtime root must not be a symlink")
        self.root = self.runtime_root / "workspace-company-governed-state"
        self._ensure_dir(self.root)
        for kind in _KINDS:
            self._ensure_dir(self.root / kind)
            self._ensure_dir(self.root / kind / "committed")
            self._ensure_dir(self.root / kind / "attempts")
            self._ensure_dir(self.root / kind / "intents")

    @staticmethod
    def _ensure_dir(path: Path) -> None:
        if path.exists() and path.is_symlink():
            raise CompanyGovernedStateError("Company governed-state directories must not be symlinks")
        try:
            path.mkdir(parents=True, exist_ok=True, mode=0o700)
            if path.is_symlink() or not path.is_dir():
                raise CompanyGovernedStateError("Company governed-state directory is unsafe")
            if os.name != "nt":
                path.chmod(0o700)
        except OSError as exc:
            raise CompanyGovernedStateError("Company governed-state directory is unavailable") from exc

    @staticmethod
    def _read_regular(path: Path) -> bytes:
        try:
            if path.is_symlink() or not path.is_file():
                raise CompanyGovernedStateError("durable governed-state record must be a regular file")
            return path.read_bytes()
        except OSError as exc:
            raise CompanyGovernedStateError("durable governed-state record is unavailable") from exc

    @staticmethod
    def _fsync_dir(path: Path) -> None:
        if os.name == "nt":
            return
        try:
            descriptor = os.open(path, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        except OSError as exc:
            raise CompanyGovernedStateError("durable governed-state directory sync failed") from exc

    def _write_immutable(self, path: Path, data: bytes) -> None:
        self._ensure_dir(path.parent)
        if path.exists():
            if self._read_regular(path) != data:
                raise CompanyGovernedStateError("immutable governed-state identity was reused with different content")
            return
        temp_name: str | None = None
        try:
            fd, temp_name = tempfile.mkstemp(prefix=".tmp-governed-", dir=path.parent)
            if os.name != "nt":
                os.fchmod(fd, 0o600)
            with os.fdopen(fd, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(temp_name, path)
            except FileExistsError:
                if self._read_regular(path) != data:
                    raise CompanyGovernedStateError(
                        "immutable governed-state identity was concurrently reused with different content"
                    )
            except OSError as exc:
                raise CompanyGovernedStateError("atomic immutable governed-state publish failed") from exc
            if os.name != "nt":
                path.chmod(0o600)
            self._fsync_dir(path.parent)
        except OSError as exc:
            raise CompanyGovernedStateError("durable governed-state write failed") from exc
        finally:
            if temp_name is not None:
                try:
                    os.unlink(temp_name)
                except FileNotFoundError:
                    pass
                except OSError:
                    pass

    def _record_bytes(self, *, kind: str, stream: str, sequence: int, payload: object) -> bytes:
        return _canonical_json(
            {
                "schema": _SCHEMA,
                "schema_version": _SCHEMA_VERSION,
                "kind": kind,
                "stream": stream,
                "sequence": sequence,
                "payload": _encode(payload),
            }
        )

    def _persist_stream(self, *, kind: str, stream: str, values: tuple[object, ...]) -> None:
        if kind not in _KINDS or stream not in {"committed", "attempts"}:
            raise CompanyGovernedStateError("unsupported governed-state stream")
        directory = self.root / kind / stream
        for sequence, value in enumerate(values):
            data = self._record_bytes(kind=kind, stream=stream, sequence=sequence, payload=value)
            path = directory / f"{sequence:08d}-{_digest(data)}.json"
            self._write_immutable(path, data)

    def _load_stream(self, *, kind: str, stream: str, expected_type: type) -> tuple[object, ...]:
        directory = self.root / kind / stream
        self._ensure_dir(directory)
        try:
            paths = sorted(directory.iterdir())
        except OSError as exc:
            raise CompanyGovernedStateError("durable governed-state stream is unavailable") from exc
        records: list[tuple[int, object]] = []
        seen_sequences: set[int] = set()
        for path in paths:
            if path.name.startswith(".tmp-governed-"):
                continue
            if path.suffix != ".json":
                raise CompanyGovernedStateError("unexpected file exists in governed-state stream")
            data = self._read_regular(path)
            if path.name != f"{path.name[:8]}-{_digest(data)}.json":
                raise CompanyGovernedStateError("durable governed-state record digest/name mismatch")
            try:
                envelope = json.loads(data.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise CompanyGovernedStateError("durable governed-state record is not valid JSON") from exc
            if not isinstance(envelope, dict) or set(envelope) != {
                "schema",
                "schema_version",
                "kind",
                "stream",
                "sequence",
                "payload",
            }:
                raise CompanyGovernedStateError("durable governed-state record envelope is invalid")
            if (
                envelope["schema"] != _SCHEMA
                or envelope["schema_version"] != _SCHEMA_VERSION
                or envelope["kind"] != kind
                or envelope["stream"] != stream
                or not isinstance(envelope["sequence"], int)
                or envelope["sequence"] < 0
            ):
                raise CompanyGovernedStateError("durable governed-state record schema is unsupported")
            sequence = envelope["sequence"]
            if sequence in seen_sequences:
                raise CompanyGovernedStateError("durable governed-state stream contains duplicate sequence")
            seen_sequences.add(sequence)
            payload = _decode(envelope["payload"])
            if not isinstance(payload, expected_type):
                raise CompanyGovernedStateError("durable governed-state record has wrong semantic type")
            records.append((sequence, payload))
        records.sort(key=lambda item: item[0])
        if [sequence for sequence, _ in records] != list(range(len(records))):
            raise CompanyGovernedStateError("durable governed-state stream sequence is incomplete")
        return tuple(value for _, value in records)

    @staticmethod
    def _validate_attempt_links(*, committed: tuple[object, ...], attempts: tuple[ConsequentialAttempt, ...]) -> None:
        for attempt in attempts:
            same_token = tuple(
                item
                for item in attempts
                if item.retry_token == attempt.retry_token and item.fingerprint == attempt.fingerprint
            )
            if attempt.outcome is ConsequentialOutcome.UNCERTAIN and any(
                item.outcome is ConsequentialOutcome.SUCCEEDED for item in same_token
            ):
                raise CompanyGovernedStateError("uncertain and succeeded durable attempts conflict")
            if attempt.outcome is not ConsequentialOutcome.SUCCEEDED:
                continue
            matches = tuple(
                item
                for item in committed
                if getattr(item, "retry_token", None) == attempt.retry_token
                and getattr(item, "fingerprint", None) == attempt.fingerprint
            )
            if len(matches) != 1:
                raise CompanyGovernedStateError("succeeded durable attempt does not resolve one commit")
            match = matches[0]
            if (
                attempt.result_version_id != match.designation.version_id
                or attempt.event_version_id != match.event.version_id
            ):
                raise CompanyGovernedStateError("succeeded durable attempt identities differ from commit")
        for item in committed:
            matches = tuple(
                attempt
                for attempt in attempts
                if attempt.outcome is ConsequentialOutcome.SUCCEEDED
                and attempt.retry_token == item.retry_token
                and attempt.fingerprint == item.fingerprint
            )
            if len(matches) != 1:
                raise CompanyGovernedStateError("durable commit does not resolve one succeeded attempt")

    def load_admission_state(self) -> OrganizationalAssetAdmissionState:
        committed = self._load_stream(
            kind="admission", stream="committed", expected_type=CommittedOrganizationalAssetAdmission
        )
        attempts = self._load_stream(
            kind="admission", stream="attempts", expected_type=ConsequentialAttempt
        )
        self._validate_attempt_links(committed=committed, attempts=attempts)
        return OrganizationalAssetAdmissionState(
            committed=committed,
            admitted_events=tuple(item.event for item in committed),
            attempts=attempts,
        )

    def persist_admission_state(self, state: OrganizationalAssetAdmissionState) -> OrganizationalAssetAdmissionState:
        if not isinstance(state, OrganizationalAssetAdmissionState):
            raise TypeError("admission state must be OrganizationalAssetAdmissionState")
        if state.admitted_events != tuple(item.event for item in state.committed):
            raise CompanyGovernedStateError("admission Event stream differs from committed admission history")
        self._persist_stream(kind="admission", stream="committed", values=state.committed)
        self._persist_stream(kind="admission", stream="attempts", values=state.attempts)
        loaded = self.load_admission_state()
        if loaded != state:
            raise CompanyGovernedStateError("admission read-after-write reconstruction mismatch")
        return loaded

    def load_promotion_state(self) -> ReviewedGeneratedOutputPromotionState:
        committed = self._load_stream(
            kind="promotion", stream="committed", expected_type=CommittedReviewedGeneratedOutputPromotion
        )
        attempts = self._load_stream(
            kind="promotion", stream="attempts", expected_type=ConsequentialAttempt
        )
        self._validate_attempt_links(committed=committed, attempts=attempts)
        return ReviewedGeneratedOutputPromotionState(
            committed=committed,
            admitted_events=tuple(item.event for item in committed),
            attempts=attempts,
        )

    def persist_promotion_state(
        self, state: ReviewedGeneratedOutputPromotionState
    ) -> ReviewedGeneratedOutputPromotionState:
        if not isinstance(state, ReviewedGeneratedOutputPromotionState):
            raise TypeError("promotion state must be ReviewedGeneratedOutputPromotionState")
        if state.admitted_events != tuple(item.event for item in state.committed):
            raise CompanyGovernedStateError("promotion Event stream differs from committed promotion history")
        self._persist_stream(kind="promotion", stream="committed", values=state.committed)
        self._persist_stream(kind="promotion", stream="attempts", values=state.attempts)
        loaded = self.load_promotion_state()
        if loaded != state:
            raise CompanyGovernedStateError("promotion read-after-write reconstruction mismatch")
        return loaded

    def intent_time(self, *, kind: str, key: tuple[str, ...], proposed: datetime) -> datetime:
        if kind not in _KINDS:
            raise CompanyGovernedStateError("unsupported governed-state intent kind")
        if not isinstance(key, tuple) or not key or any(not isinstance(item, str) or not item for item in key):
            raise CompanyGovernedStateError("governed-state intent key must be explicit")
        if not isinstance(proposed, datetime) or proposed.tzinfo is None or proposed.utcoffset() is None:
            raise CompanyGovernedStateError("governed-state intent time must be timezone-aware")
        encoded_key = _canonical_json(list(key))
        identity = hashlib.sha256(encoded_key).hexdigest()
        path = self.root / kind / "intents" / f"{identity}.json"
        if not path.exists():
            data = _canonical_json(
                {
                    "schema": _SCHEMA,
                    "schema_version": _SCHEMA_VERSION,
                    "kind": kind,
                    "stream": "intent",
                    "key": list(key),
                    "command_at": proposed.isoformat(),
                }
            )
            self._write_immutable(path, data)
        data = self._read_regular(path)
        try:
            envelope = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CompanyGovernedStateError("durable governed-state intent is invalid JSON") from exc
        if (
            not isinstance(envelope, dict)
            or set(envelope) != {"schema", "schema_version", "kind", "stream", "key", "command_at"}
            or envelope["schema"] != _SCHEMA
            or envelope["schema_version"] != _SCHEMA_VERSION
            or envelope["kind"] != kind
            or envelope["stream"] != "intent"
            or envelope["key"] != list(key)
            or not isinstance(envelope["command_at"], str)
        ):
            raise CompanyGovernedStateError("durable governed-state intent schema is invalid")
        try:
            value = datetime.fromisoformat(envelope["command_at"])
        except ValueError as exc:
            raise CompanyGovernedStateError("durable governed-state intent time is invalid") from exc
        if value.tzinfo is None or value.utcoffset() is None:
            raise CompanyGovernedStateError("durable governed-state intent time must remain timezone-aware")
        return value


__all__ = ["CompanyGovernedStateError", "CompanyGovernedStateStore"]

"""ADR-0002 product-local durable governed state for Company Workspace.

This module persists only already-governed P10.03/P10.05 semantic results,
retry evidence, and a bounded pre-effect journal used to make crash windows
fail closed. It does not grant authority, replay consequential effects, or
create a platform-wide storage contract.
"""
from __future__ import annotations

import hashlib
import json
import os
import tempfile
import threading
import uuid
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
_EFFECT_OUTCOMES = frozenset({"no_effect", "committed"})
_WRITE_LOCK = threading.RLock()


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
    # String-valued Enum members must be handled before the primitive str branch.
    if isinstance(value, Enum):
        enum_type = type(value)
        if enum_type not in _ENUM_TYPES:
            raise CompanyGovernedStateError(f"unsupported durable enum type: {enum_type.__name__}")
        return {"$enum": enum_type.__name__, "value": value.value}
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, datetime):
        if value.tzinfo is None or value.utcoffset() is None:
            raise CompanyGovernedStateError("durable governed state refuses naive datetime values")
        return {"$datetime": value.isoformat()}
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
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


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
            self._ensure_dir(self.root / kind / "effects")

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
        """Publish one immutable record using temp+fsync+atomic rename+read-back."""

        self._ensure_dir(path.parent)
        temp_name: str | None = None
        with _WRITE_LOCK:
            if path.exists():
                if self._read_regular(path) != data:
                    raise CompanyGovernedStateError(
                        "immutable governed-state identity was reused with different content"
                    )
                return
            try:
                fd, temp_name = tempfile.mkstemp(prefix=".tmp-governed-", dir=path.parent)
                if os.name != "nt":
                    os.fchmod(fd, 0o600)
                with os.fdopen(fd, "wb") as handle:
                    handle.write(data)
                    handle.flush()
                    os.fsync(handle.fileno())

                # Re-check while holding the in-process single-writer lock.
                if path.exists():
                    if self._read_regular(path) != data:
                        raise CompanyGovernedStateError(
                            "immutable governed-state identity was concurrently reused with different content"
                        )
                    return

                os.replace(temp_name, path)
                temp_name = None
                if os.name != "nt":
                    path.chmod(0o600)
                self._fsync_dir(path.parent)
                if self._read_regular(path) != data:
                    raise CompanyGovernedStateError(
                        "durable governed-state read-after-write verification failed"
                    )
            except CompanyGovernedStateError:
                raise
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
    def _validate_attempt_links(
        *, committed: tuple[object, ...], attempts: tuple[ConsequentialAttempt, ...]
    ) -> None:
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
                raise CompanyGovernedStateError(
                    "succeeded durable attempt identities differ from commit"
                )
        for item in committed:
            matches = tuple(
                attempt
                for attempt in attempts
                if attempt.outcome is ConsequentialOutcome.SUCCEEDED
                and attempt.retry_token == item.retry_token
                and attempt.fingerprint == item.fingerprint
            )
            if len(matches) != 1:
                raise CompanyGovernedStateError(
                    "durable commit does not resolve one succeeded attempt"
                )

    def load_admission_state(self) -> OrganizationalAssetAdmissionState:
        committed = self._load_stream(
            kind="admission",
            stream="committed",
            expected_type=CommittedOrganizationalAssetAdmission,
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

    def persist_admission_state(
        self, state: OrganizationalAssetAdmissionState
    ) -> OrganizationalAssetAdmissionState:
        if not isinstance(state, OrganizationalAssetAdmissionState):
            raise TypeError("admission state must be OrganizationalAssetAdmissionState")
        if state.admitted_events != tuple(item.event for item in state.committed):
            raise CompanyGovernedStateError(
                "admission Event stream differs from committed admission history"
            )
        self._persist_stream(kind="admission", stream="committed", values=state.committed)
        self._persist_stream(kind="admission", stream="attempts", values=state.attempts)
        loaded = self.load_admission_state()
        if loaded != state:
            raise CompanyGovernedStateError("admission read-after-write reconstruction mismatch")
        return loaded

    def load_promotion_state(self) -> ReviewedGeneratedOutputPromotionState:
        committed = self._load_stream(
            kind="promotion",
            stream="committed",
            expected_type=CommittedReviewedGeneratedOutputPromotion,
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
            raise CompanyGovernedStateError(
                "promotion Event stream differs from committed promotion history"
            )
        self._persist_stream(kind="promotion", stream="committed", values=state.committed)
        self._persist_stream(kind="promotion", stream="attempts", values=state.attempts)
        loaded = self.load_promotion_state()
        if loaded != state:
            raise CompanyGovernedStateError("promotion read-after-write reconstruction mismatch")
        return loaded

    @staticmethod
    def _validate_intent_key(kind: str, key: tuple[str, ...]) -> None:
        if kind not in _KINDS:
            raise CompanyGovernedStateError("unsupported governed-state intent kind")
        if (
            not isinstance(key, tuple)
            or not key
            or any(not isinstance(item, str) or not item for item in key)
        ):
            raise CompanyGovernedStateError("governed-state intent key must be explicit")

    def intent_time(self, *, kind: str, key: tuple[str, ...], proposed: datetime) -> datetime:
        self._validate_intent_key(kind, key)
        if (
            not isinstance(proposed, datetime)
            or proposed.tzinfo is None
            or proposed.utcoffset() is None
        ):
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
            or set(envelope)
            != {"schema", "schema_version", "kind", "stream", "key", "command_at"}
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
            raise CompanyGovernedStateError(
                "durable governed-state intent time must remain timezone-aware"
            )
        return value

    def _effect_envelope(self, path: Path, *, kind: str, stream: str) -> dict[str, Any]:
        data = self._read_regular(path)
        try:
            envelope = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CompanyGovernedStateError("durable effect journal record is invalid JSON") from exc
        required = {
            "schema",
            "schema_version",
            "kind",
            "stream",
            "attempt_id",
            "key",
            "retry_token",
            "timestamp",
        }
        if (
            not isinstance(envelope, dict)
            or set(envelope) - {"outcome"} != required
            or envelope.get("schema") != _SCHEMA
            or envelope.get("schema_version") != _SCHEMA_VERSION
            or envelope.get("kind") != kind
            or envelope.get("stream") != stream
            or not isinstance(envelope.get("attempt_id"), str)
            or not envelope["attempt_id"]
            or not isinstance(envelope.get("key"), list)
            or not envelope["key"]
            or any(not isinstance(item, str) or not item for item in envelope["key"])
            or not isinstance(envelope.get("retry_token"), str)
            or not envelope["retry_token"]
            or not isinstance(envelope.get("timestamp"), str)
        ):
            raise CompanyGovernedStateError("durable effect journal record schema is invalid")
        try:
            stamp = datetime.fromisoformat(envelope["timestamp"])
        except ValueError as exc:
            raise CompanyGovernedStateError("durable effect journal timestamp is invalid") from exc
        if stamp.tzinfo is None or stamp.utcoffset() is None:
            raise CompanyGovernedStateError("durable effect journal timestamp must be timezone-aware")
        if stream == "effect-resolution":
            if set(envelope) != required | {"outcome"} or envelope.get("outcome") not in _EFFECT_OUTCOMES:
                raise CompanyGovernedStateError("durable effect resolution is invalid")
        elif set(envelope) != required:
            raise CompanyGovernedStateError("durable effect start is invalid")
        return envelope

    def _effect_records(self, *, kind: str) -> tuple[tuple[dict[str, Any], dict[str, Any] | None], ...]:
        if kind not in _KINDS:
            raise CompanyGovernedStateError("unsupported governed-state effect kind")
        directory = self.root / kind / "effects"
        self._ensure_dir(directory)
        try:
            paths = sorted(directory.iterdir())
        except OSError as exc:
            raise CompanyGovernedStateError("durable effect journal is unavailable") from exc
        starts: dict[str, dict[str, Any]] = {}
        resolutions: dict[str, dict[str, Any]] = {}
        for path in paths:
            if path.name.startswith(".tmp-governed-"):
                continue
            if path.name.endswith(".started.json"):
                envelope = self._effect_envelope(path, kind=kind, stream="effect-start")
                attempt_id = envelope["attempt_id"]
                if path.name != f"{attempt_id}.started.json" or attempt_id in starts:
                    raise CompanyGovernedStateError("durable effect start identity is inconsistent")
                starts[attempt_id] = envelope
            elif path.name.endswith(".resolved.json"):
                envelope = self._effect_envelope(path, kind=kind, stream="effect-resolution")
                attempt_id = envelope["attempt_id"]
                if path.name != f"{attempt_id}.resolved.json" or attempt_id in resolutions:
                    raise CompanyGovernedStateError("durable effect resolution identity is inconsistent")
                resolutions[attempt_id] = envelope
            else:
                raise CompanyGovernedStateError("unexpected file exists in durable effect journal")
        if set(resolutions) - set(starts):
            raise CompanyGovernedStateError("durable effect resolution lacks its start record")
        result = []
        for attempt_id, start in starts.items():
            resolution = resolutions.get(attempt_id)
            if resolution is not None and (
                resolution["key"] != start["key"]
                or resolution["retry_token"] != start["retry_token"]
            ):
                raise CompanyGovernedStateError("durable effect resolution differs from its start")
            result.append((start, resolution))
        return tuple(result)

    def begin_effect(
        self,
        *,
        kind: str,
        key: tuple[str, ...],
        retry_token: str,
        started_at: datetime,
        committed_retry_tokens: tuple[str, ...] = (),
    ) -> str:
        """Persist a pre-effect marker; unresolved same-token history blocks blind retry."""

        self._validate_intent_key(kind, key)
        if not isinstance(retry_token, str) or not retry_token:
            raise CompanyGovernedStateError("durable effect retry token must be explicit")
        if (
            not isinstance(started_at, datetime)
            or started_at.tzinfo is None
            or started_at.utcoffset() is None
        ):
            raise CompanyGovernedStateError("durable effect start time must be timezone-aware")
        if not isinstance(committed_retry_tokens, tuple) or any(
            not isinstance(item, str) or not item for item in committed_retry_tokens
        ):
            raise CompanyGovernedStateError("committed retry-token evidence is invalid")
        for start, resolution in self._effect_records(kind=kind):
            if start["retry_token"] != retry_token:
                continue
            if tuple(start["key"]) != key:
                raise CompanyGovernedStateError(
                    "durable effect retry token was bound to a different product command"
                )
            if resolution is None and retry_token not in committed_retry_tokens:
                raise CompanyGovernedStateError(
                    "durable effect has an unresolved prior outcome; reconciliation is required"
                )

        attempt_id = uuid.uuid4().hex
        envelope = {
            "schema": _SCHEMA,
            "schema_version": _SCHEMA_VERSION,
            "kind": kind,
            "stream": "effect-start",
            "attempt_id": attempt_id,
            "key": list(key),
            "retry_token": retry_token,
            "timestamp": started_at.isoformat(),
        }
        path = self.root / kind / "effects" / f"{attempt_id}.started.json"
        data = _canonical_json(envelope)
        self._write_immutable(path, data)
        loaded = self._effect_envelope(path, kind=kind, stream="effect-start")
        if loaded != envelope:
            raise CompanyGovernedStateError("durable effect start read-after-write mismatch")
        return attempt_id

    def resolve_effect(
        self,
        *,
        kind: str,
        attempt_id: str,
        outcome: str,
        resolved_at: datetime,
        committed_retry_tokens: tuple[str, ...] = (),
    ) -> None:
        """Append an immutable resolution for one previously persisted effect marker."""

        if kind not in _KINDS:
            raise CompanyGovernedStateError("unsupported governed-state effect kind")
        if not isinstance(attempt_id, str) or not attempt_id:
            raise CompanyGovernedStateError("durable effect attempt identity must be explicit")
        if outcome not in _EFFECT_OUTCOMES:
            raise CompanyGovernedStateError("durable effect outcome is unsupported")
        if (
            not isinstance(resolved_at, datetime)
            or resolved_at.tzinfo is None
            or resolved_at.utcoffset() is None
        ):
            raise CompanyGovernedStateError("durable effect resolution time must be timezone-aware")
        if not isinstance(committed_retry_tokens, tuple) or any(
            not isinstance(item, str) or not item for item in committed_retry_tokens
        ):
            raise CompanyGovernedStateError("committed retry-token evidence is invalid")

        start_path = self.root / kind / "effects" / f"{attempt_id}.started.json"
        start = self._effect_envelope(start_path, kind=kind, stream="effect-start")
        retry_token = start["retry_token"]
        if outcome == "committed" and retry_token not in committed_retry_tokens:
            raise CompanyGovernedStateError(
                "effect cannot be resolved as committed before durable commit reconstruction"
            )
        envelope = {
            "schema": _SCHEMA,
            "schema_version": _SCHEMA_VERSION,
            "kind": kind,
            "stream": "effect-resolution",
            "attempt_id": attempt_id,
            "key": start["key"],
            "retry_token": retry_token,
            "timestamp": resolved_at.isoformat(),
            "outcome": outcome,
        }
        path = self.root / kind / "effects" / f"{attempt_id}.resolved.json"
        data = _canonical_json(envelope)
        self._write_immutable(path, data)
        loaded = self._effect_envelope(path, kind=kind, stream="effect-resolution")
        if loaded != envelope:
            raise CompanyGovernedStateError("durable effect resolution read-after-write mismatch")


__all__ = ["CompanyGovernedStateError", "CompanyGovernedStateStore"]

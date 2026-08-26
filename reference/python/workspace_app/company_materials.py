from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import re
import secrets
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from .access import AccessContext


class CompanyMaterialsError(RuntimeError):
    """Bounded F11A staged-material operation cannot be completed safely."""


class CompanyMaterialsInputError(CompanyMaterialsError):
    """User supplied material metadata or bytes are outside the bounded contract."""


class CompanyMaterialUnavailable(CompanyMaterialsError):
    """The exact requested staged material/version cannot be resolved."""


MAX_MATERIAL_BYTES = 8 * 1024 * 1024
MAX_DOCX_EXPANDED_BYTES = 32 * 1024 * 1024
_ALLOWED_MEDIA_TYPES = frozenset(
    {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/svg+xml",
        "text/plain",
        "text/markdown",
        "application/octet-stream",
    }
)
_SAFE_ID = re.compile(r"^[A-Za-z0-9_.-]{8,96}$")
_SAFE_PROJECT_ID = re.compile(r"^(?:PORT-[0-9]{3}|COMPANY)$")
_WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_SUPPORTED_PLACEHOLDERS = ("{{TITLE}}", "{{BODY}}", "{{DATE}}")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _identity_text(identity: object) -> str:
    return f"{identity.namespace}:{identity.value}@{identity.scope}"  # type: ignore[attr-defined]


def _bounded(value: object, name: str, *, maximum: int = 320, required: bool = True) -> str:
    if not isinstance(value, str):
        raise CompanyMaterialsInputError(f"{name} must be text")
    normalized = " ".join(value.split())
    if required and not normalized:
        raise CompanyMaterialsInputError(f"{name} is required")
    if len(normalized) > maximum:
        raise CompanyMaterialsInputError(f"{name} exceeds bounded length")
    return normalized


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".{secrets.token_hex(6)}.tmp")
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    try:
        temporary.write_text(data, encoding="utf-8")
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass


def _content_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _decode_content(value: object) -> bytes:
    if not isinstance(value, str) or not value:
        raise CompanyMaterialsInputError("content_base64 is required")
    try:
        content = base64.b64decode(value, validate=True)
    except (ValueError, TypeError) as exc:
        raise CompanyMaterialsInputError("content_base64 is invalid") from exc
    if not content or len(content) > MAX_MATERIAL_BYTES:
        raise CompanyMaterialsInputError("material bytes are empty or exceed 8 MiB")
    return content


@dataclass(frozen=True, slots=True)
class MaterialVersion:
    material_id: str
    version_id: str
    predecessor_version_id: str | None
    project_id: str
    filename: str
    media_type: str
    semantic_role: str
    classification: str
    purpose: str
    rights: str
    retention_rule: str
    uploader: str
    received_at: str
    content_sha256: str
    size_bytes: int
    state: str = "StagedNonCanonical"

    def to_payload(self) -> dict[str, Any]:
        return {
            "material_id": self.material_id,
            "version_id": self.version_id,
            "predecessor_version_id": self.predecessor_version_id,
            "project_id": self.project_id,
            "filename": self.filename,
            "media_type": self.media_type,
            "semantic_role": self.semantic_role,
            "classification": self.classification,
            "purpose": self.purpose,
            "rights": self.rights,
            "retention_rule": self.retention_rule,
            "uploader": self.uploader,
            "received_at": self.received_at,
            "content_sha256": self.content_sha256,
            "size_bytes": self.size_bytes,
            "state": self.state,
            "canonical_authority": False,
            "validated_knowledge": False,
        }


class CompanyMaterialsStore:
    """Product-owned, owner-local staged material store for F11A.

    This store deliberately does not admit platform canonical Documents or
    Artifacts. It preserves exact bytes, immutable version identity, attribution,
    handling metadata and lineage so a future governed admission path can consume
    explicit evidence rather than reconstructing it from browser state.
    """

    def __init__(self, runtime_root: Path) -> None:
        self.root = runtime_root.expanduser() / "workspace-company-materials"
        self.blobs = self.root / "blobs"
        self.manifests = self.root / "materials"
        self.transient = self.root / "transient"

    def _manifest_path(self, material_id: str) -> Path:
        if not _SAFE_ID.fullmatch(material_id):
            raise CompanyMaterialUnavailable("material identity invalid")
        return self.manifests / f"{material_id}.json"

    def _read_manifest(self, material_id: str) -> dict[str, Any]:
        path = self._manifest_path(material_id)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CompanyMaterialUnavailable("material manifest unavailable") from exc
        if payload.get("schema") != "arvectum.company.staged-material/1" or payload.get("material_id") != material_id:
            raise CompanyMaterialUnavailable("material manifest invalid")
        versions = payload.get("versions")
        if not isinstance(versions, list) or not versions:
            raise CompanyMaterialUnavailable("material manifest has no versions")
        return payload

    def _version(self, material_id: str, version_id: str) -> dict[str, Any]:
        if not _SAFE_ID.fullmatch(version_id):
            raise CompanyMaterialUnavailable("version identity invalid")
        manifest = self._read_manifest(material_id)
        matches = [item for item in manifest["versions"] if isinstance(item, dict) and item.get("version_id") == version_id]
        if len(matches) != 1:
            raise CompanyMaterialUnavailable("exact staged material version unavailable")
        version = matches[0]
        if version.get("state") != "StagedNonCanonical":
            raise CompanyMaterialUnavailable("unsupported material state")
        return version

    def _write_blob(self, content: bytes, sha256: str) -> None:
        self.blobs.mkdir(parents=True, exist_ok=True)
        target = self.blobs / sha256
        if target.exists():
            if target.is_file() and _content_sha256(target.read_bytes()) == sha256:
                return
            raise CompanyMaterialsError("content-addressed staged blob conflict")
        temporary = self.blobs / f".{sha256}.{secrets.token_hex(6)}.tmp"
        try:
            temporary.write_bytes(content)
            if _content_sha256(temporary.read_bytes()) != sha256:
                raise CompanyMaterialsError("staged blob integrity verification failed")
            os.replace(temporary, target)
        finally:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass

    def _validated_metadata(self, payload: dict[str, Any]) -> dict[str, str]:
        project_id = _bounded(payload.get("project_id", "COMPANY"), "project_id", maximum=24)
        if not _SAFE_PROJECT_ID.fullmatch(project_id):
            raise CompanyMaterialsInputError("project_id must be COMPANY or stable PORT-nnn identity")
        filename = _bounded(payload.get("filename"), "filename", maximum=240)
        if "/" in filename or "\\" in filename or filename in {".", ".."}:
            raise CompanyMaterialsInputError("filename must be a basename")
        media_type = _bounded(payload.get("media_type", "application/octet-stream"), "media_type", maximum=160)
        if media_type not in _ALLOWED_MEDIA_TYPES:
            raise CompanyMaterialsInputError("media_type is outside the bounded F11A allowlist")
        return {
            "project_id": project_id,
            "filename": filename,
            "media_type": media_type,
            "semantic_role": _bounded(payload.get("semantic_role"), "semantic_role", maximum=96),
            "classification": _bounded(payload.get("classification"), "classification", maximum=96),
            "purpose": _bounded(payload.get("purpose"), "purpose", maximum=240),
            "rights": _bounded(payload.get("rights"), "rights", maximum=240),
            "retention_rule": _bounded(payload.get("retention_rule"), "retention_rule", maximum=240),
        }

    def stage(self, access: AccessContext, payload: object) -> dict[str, Any]:
        if not isinstance(access, AccessContext):
            raise CompanyMaterialsError("server-authorized AccessContext is required")
        if not isinstance(payload, dict):
            raise CompanyMaterialsInputError("material payload must be an object")
        allowed = {
            "material_id",
            "project_id",
            "filename",
            "media_type",
            "semantic_role",
            "classification",
            "purpose",
            "rights",
            "retention_rule",
            "content_base64",
        }
        if not set(payload).issubset(allowed):
            raise CompanyMaterialsInputError("material payload contains unsupported fields")
        metadata = self._validated_metadata(payload)
        content = _decode_content(payload.get("content_base64"))
        sha256 = _content_sha256(content)
        material_id_raw = payload.get("material_id")
        predecessor: str | None = None
        manifest: dict[str, Any]
        if material_id_raw is None:
            material_id = f"MAT-{secrets.token_hex(16)}"
            manifest = {
                "schema": "arvectum.company.staged-material/1",
                "material_id": material_id,
                "created_at": _utc_now(),
                "versions": [],
            }
        else:
            material_id = _bounded(material_id_raw, "material_id", maximum=96)
            manifest = self._read_manifest(material_id)
            latest = manifest["versions"][-1]
            predecessor = str(latest["version_id"])
            if latest.get("content_sha256") == sha256 and all(latest.get(key) == value for key, value in metadata.items()):
                raise CompanyMaterialsInputError("new version must differ in bytes or declared metadata")

        received_at = _utc_now()
        version_basis = json.dumps(
            {
                "material_id": material_id,
                "predecessor": predecessor,
                "sha256": sha256,
                "metadata": metadata,
                "received_at": received_at,
                "uploader": _identity_text(access.actor),
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        version_id = f"MV-{hashlib.sha256(version_basis).hexdigest()[:32]}"
        version = MaterialVersion(
            material_id=material_id,
            version_id=version_id,
            predecessor_version_id=predecessor,
            uploader=_identity_text(access.actor),
            received_at=received_at,
            content_sha256=sha256,
            size_bytes=len(content),
            **metadata,
        ).to_payload()
        self._write_blob(content, sha256)
        manifest["versions"].append(version)
        manifest["latest_version_id"] = version_id
        _atomic_json(self._manifest_path(material_id), manifest)
        return {
            "schema": "arvectum.workspace.company-material/1",
            "material": version,
            "governance": self._governance_payload(),
        }

    def project(self, access: AccessContext) -> dict[str, Any]:
        if not isinstance(access, AccessContext):
            raise CompanyMaterialsError("server-authorized AccessContext is required")
        materials: list[dict[str, Any]] = []
        if self.manifests.is_dir():
            for path in sorted(self.manifests.glob("MAT-*.json")):
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                    versions = payload.get("versions")
                    if payload.get("schema") != "arvectum.company.staged-material/1" or not isinstance(versions, list) or not versions:
                        continue
                    materials.append(
                        {
                            "material_id": payload.get("material_id"),
                            "latest_version_id": payload.get("latest_version_id"),
                            "versions": versions,
                        }
                    )
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    continue
        return {
            "schema": "arvectum.workspace.company-materials/1",
            "generated_at": _utc_now(),
            "product_contract": {"id": "P9.11-F11", "version": "0.1.0", "lifecycle": "Provisional"},
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "cross_organization_access": False,
            },
            "materials": materials,
            "governance": self._governance_payload(),
        }

    @staticmethod
    def _governance_payload() -> dict[str, Any]:
        return {
            "state": "StagedNonCanonical",
            "canonical_admission_available": False,
            "canonical_state_changed": False,
            "organizational_authority_provided_by_upload": False,
            "validated_knowledge_created": False,
            "reason": (
                "Текущий F11A сохраняет owner-local staged evidence и точные версии, но не выдаёт "
                "Authorization/Organizational Authority и не подменяет RFC-0005 Governed Execution."
            ),
        }

    def generate_docx(self, access: AccessContext, payload: object) -> dict[str, Any]:
        if not isinstance(access, AccessContext):
            raise CompanyMaterialsError("server-authorized AccessContext is required")
        if not isinstance(payload, dict) or set(payload) != {"material_id", "version_id", "title", "body", "date"}:
            raise CompanyMaterialsInputError("generation payload is invalid")
        material_id = _bounded(payload.get("material_id"), "material_id", maximum=96)
        version_id = _bounded(payload.get("version_id"), "version_id", maximum=96)
        title = _bounded(payload.get("title"), "title", maximum=320)
        body = _bounded(payload.get("body"), "body", maximum=6000)
        date = _bounded(payload.get("date"), "date", maximum=80)
        version = self._version(material_id, version_id)
        if version.get("media_type") != "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            raise CompanyMaterialsInputError("template-aware generation currently requires an exact DOCX version")
        blob = self.blobs / str(version["content_sha256"])
        try:
            source = blob.read_bytes()
        except OSError as exc:
            raise CompanyMaterialUnavailable("exact template bytes unavailable") from exc
        if _content_sha256(source) != version["content_sha256"]:
            raise CompanyMaterialsError("exact template integrity mismatch")
        output = self._render_docx(source, {"{{TITLE}}": title, "{{BODY}}": body, "{{DATE}}": date})
        output_sha = _content_sha256(output)
        output_id = f"OUT-{secrets.token_hex(16)}"
        self.transient.mkdir(parents=True, exist_ok=True)
        output_path = self.transient / f"{output_id}.docx"
        output_path.write_bytes(output)
        output_manifest = {
            "schema": "arvectum.company.transient-output/1",
            "output_id": output_id,
            "state": "TransientOutput",
            "created_at": _utc_now(),
            "created_by": _identity_text(access.actor),
            "source_material_id": material_id,
            "source_version_id": version_id,
            "source_sha256": version["content_sha256"],
            "output_sha256": output_sha,
            "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "filename": f"generated-{output_id}.docx",
            "canonical_authority": False,
            "validated_knowledge": False,
        }
        _atomic_json(self.transient / f"{output_id}.json", output_manifest)
        return {
            "schema": "arvectum.workspace.company-generated-output/1",
            "output": {**output_manifest, "download_href": f"/api/app/v1/company-materials/outputs/{output_id}/download"},
            "governance": {
                "generated_artifact_state": "TransientOutput",
                "canonical_state_changed": False,
                "exact_source_version_pinned": True,
            },
        }

    def output_path(self, output_id: str) -> tuple[Path, dict[str, Any]]:
        if not _SAFE_ID.fullmatch(output_id) or not output_id.startswith("OUT-"):
            raise CompanyMaterialUnavailable("output identity invalid")
        manifest_path = self.transient / f"{output_id}.json"
        output_path = self.transient / f"{output_id}.docx"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            content = output_path.read_bytes()
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise CompanyMaterialUnavailable("transient output unavailable") from exc
        if manifest.get("schema") != "arvectum.company.transient-output/1" or manifest.get("output_id") != output_id:
            raise CompanyMaterialUnavailable("transient output manifest invalid")
        if _content_sha256(content) != manifest.get("output_sha256"):
            raise CompanyMaterialsError("transient output integrity mismatch")
        return output_path, manifest

    @staticmethod
    def _render_docx(source: bytes, replacements: dict[str, str]) -> bytes:
        try:
            with zipfile.ZipFile(io.BytesIO(source), "r") as archive:
                infos = archive.infolist()
                if not infos or "word/document.xml" not in {info.filename for info in infos}:
                    raise CompanyMaterialsInputError("selected DOCX template is structurally invalid")
                total = sum(info.file_size for info in infos)
                if total > MAX_DOCX_EXPANDED_BYTES:
                    raise CompanyMaterialsInputError("selected DOCX template exceeds expanded-size limit")
                for info in infos:
                    if info.flag_bits & 0x1:
                        raise CompanyMaterialsInputError("encrypted DOCX templates are unsupported")
                    parts = Path(info.filename).parts
                    if info.filename.startswith("/") or ".." in parts:
                        raise CompanyMaterialsInputError("selected DOCX template contains unsafe archive paths")
                entries = [(info, archive.read(info.filename)) for info in infos]
        except zipfile.BadZipFile as exc:
            raise CompanyMaterialsInputError("selected DOCX template is not a valid Office package") from exc

        changed: set[str] = set()
        rendered_entries: list[tuple[zipfile.ZipInfo, bytes]] = []
        for info, data in entries:
            if info.filename != "word/document.xml":
                rendered_entries.append((info, data))
                continue
            try:
                root = ET.fromstring(data)
            except ET.ParseError as exc:
                raise CompanyMaterialsInputError("selected DOCX document.xml is invalid") from exc
            for node in root.iter(f"{{{_WORD_NS}}}t"):
                if node.text is None:
                    continue
                value = node.text
                for placeholder, replacement in replacements.items():
                    if placeholder in value:
                        value = value.replace(placeholder, replacement)
                        changed.add(placeholder)
                node.text = value
            rendered_entries.append((info, ET.tostring(root, encoding="utf-8", xml_declaration=True)))
        if not changed:
            raise CompanyMaterialsInputError(
                "DOCX template must contain at least one contiguous placeholder: {{TITLE}}, {{BODY}} or {{DATE}}"
            )
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as target:
            for info, data in rendered_entries:
                clone = zipfile.ZipInfo(info.filename, date_time=info.date_time)
                clone.compress_type = info.compress_type
                clone.comment = info.comment
                clone.extra = info.extra
                clone.internal_attr = info.internal_attr
                clone.external_attr = info.external_attr
                clone.create_system = info.create_system
                target.writestr(clone, data)
        return buffer.getvalue()


__all__ = [
    "CompanyMaterialUnavailable",
    "CompanyMaterialsError",
    "CompanyMaterialsInputError",
    "CompanyMaterialsStore",
    "MAX_MATERIAL_BYTES",
]

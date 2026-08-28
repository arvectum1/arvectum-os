"""Product-local P10.03 bridge from Company staging to CAP-001 admission input.

This module is intentionally Company-owned.  It may understand the F11A staged
material schema, project id and semantic role, while the shared
``arvectum_os_ref.organizational_asset_admission`` module remains domain-neutral.

The bridge only resolves and verifies an exact staged version then constructs an
immutable candidate.  It grants no Authorization, Organizational Authority,
Data Governance decision, Validation or Consequential Approval and it never
changes the staged manifest from ``StagedNonCanonical``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext
from p10_03_company_asset_ref.contract import NATIVE_ASSET_DOCUMENT_SCOPE

from .access import AccessContext
from .company_materials import CompanyMaterialUnavailable, CompanyMaterialsError, CompanyMaterialsStore


@dataclass(frozen=True, slots=True)
class ExactCompanyStagedMaterial:
    """Verified exact Company staged-version evidence, still non-canonical."""

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
    blob_path: Path
    state: str

    def __post_init__(self) -> None:
        if self.state != "StagedNonCanonical":
            raise ValueError("Company admission bridge accepts only exact StagedNonCanonical input")
        if not isinstance(self.blob_path, Path):
            raise ValueError("Company staged material blob_path must be explicit")
        if len(self.content_sha256) != 64:
            raise ValueError("Company staged material must preserve an exact SHA-256 digest")


def resolve_exact_staged_material(
    *,
    store: CompanyMaterialsStore,
    access: AccessContext,
    material_id: str,
    version_id: str,
) -> ExactCompanyStagedMaterial:
    """Resolve one exact F11A version and re-hash its bytes before admission use."""

    if not isinstance(store, CompanyMaterialsStore):
        raise TypeError("Company staged admission requires CompanyMaterialsStore")
    if not isinstance(access, AccessContext):
        raise TypeError("Company staged admission requires server-authorized AccessContext")

    version = store._version(access, material_id, version_id)  # product-local implementation seam
    digest = version.get("content_sha256")
    if not isinstance(digest, str) or len(digest) != 64:
        raise CompanyMaterialsError("exact staged material digest is invalid")
    blob_path = store.blobs / digest
    try:
        if blob_path.is_symlink() or not blob_path.is_file():
            raise CompanyMaterialUnavailable("exact staged material bytes unavailable")
        content = blob_path.read_bytes()
    except OSError as exc:
        raise CompanyMaterialUnavailable("exact staged material bytes unavailable") from exc
    if hashlib.sha256(content).hexdigest() != digest:
        raise CompanyMaterialsError("exact staged material integrity mismatch")
    if len(content) != version.get("size_bytes"):
        raise CompanyMaterialsError("exact staged material size mismatch")

    required_text = (
        "project_id",
        "filename",
        "media_type",
        "semantic_role",
        "classification",
        "purpose",
        "rights",
        "retention_rule",
        "uploader",
        "received_at",
        "state",
    )
    if any(not isinstance(version.get(key), str) or not str(version[key]).strip() for key in required_text):
        raise CompanyMaterialsError("exact staged material metadata is incomplete")

    return ExactCompanyStagedMaterial(
        material_id=material_id,
        version_id=version_id,
        predecessor_version_id=(
            str(version["predecessor_version_id"])
            if version.get("predecessor_version_id") is not None
            else None
        ),
        project_id=str(version["project_id"]),
        filename=str(version["filename"]),
        media_type=str(version["media_type"]),
        semantic_role=str(version["semantic_role"]),
        classification=str(version["classification"]),
        purpose=str(version["purpose"]),
        rights=str(version["rights"]),
        retention_rule=str(version["retention_rule"]),
        uploader=str(version["uploader"]),
        received_at=str(version["received_at"]),
        content_sha256=digest,
        size_bytes=int(version["size_bytes"]),
        blob_path=blob_path,
        state=str(version["state"]),
    )


def build_staged_document_candidate(
    *,
    staged: ExactCompanyStagedMaterial,
    access: AccessContext,
    actor: ActorContext,
    candidate_created_at: datetime,
) -> DocumentVersionCandidate:
    """Map exact product-local staging into a domain-neutral CAP-001 candidate."""

    if not isinstance(staged, ExactCompanyStagedMaterial):
        raise TypeError("staged input must be ExactCompanyStagedMaterial")
    if not isinstance(access, AccessContext):
        raise TypeError("candidate construction requires AccessContext")
    if not isinstance(actor, ActorContext):
        raise TypeError("candidate construction requires attributable ActorContext")
    if not isinstance(candidate_created_at, datetime) or candidate_created_at.tzinfo is None or candidate_created_at.utcoffset() is None:
        raise ValueError("candidate_created_at must be timezone-aware")
    if access.organization != actor.organization.organization_id:
        raise PermissionError("Workspace access and Governed Execution Organization must match exactly")
    if access.actor != actor.actual_principal.principal_id:
        raise PermissionError("Workspace access Actor and Governed Execution actual principal must match exactly")

    scope = actor.organization.organization_id.value
    source_subject = Identity("staged-material", staged.material_id, scope)
    source_version = Identity("staged-material-version", staged.version_id, scope)
    document_subject = Identity("document", f"organizational-asset-{staged.material_id}", scope)
    document_version = Identity("document-version", f"organizational-asset-{staged.version_id}", scope)
    predecessor = (
        Identity(
            "document-version",
            f"organizational-asset-{staged.predecessor_version_id}",
            scope,
        )
        if staged.predecessor_version_id is not None
        else None
    )
    artifact_id = Identity("artifact", f"company-staged-{staged.content_sha256[:32]}", scope)
    handling = HandlingConstraints(
        classification=staged.classification,
        purpose=staged.purpose,
        rights=(staged.rights,),
        retention_rule=staged.retention_rule,
    )
    artifact = ArtifactContent(
        artifact_id=artifact_id,
        organization=actor.organization,
        content_ref=f"sha256:{staged.content_sha256}",
        media_type=staged.media_type,
        integrity_ref=staged.content_sha256,
        rendition_role="original",
        handling=handling,
        storage_locator="owner-local-company-materials",
    )
    record = CanonicalRecord(
        subject_id=document_subject,
        version_id=document_version,
        semantic_type="platform.document",
        schema_version="p10.03-company-staged-1",
        organization=actor.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=NATIVE_ASSET_DOCUMENT_SCOPE,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=candidate_created_at,
        provenance_refs=(
            actor.actual_principal.principal_id,
            source_subject,
            source_version,
        ),
        integrity_metadata=(
            ("representation", "p10.03-exact-company-staged-version"),
            ("source_sha256", staged.content_sha256),
            ("source_state", staged.state),
        ),
        payload=(
            ("project_id", staged.project_id),
            ("filename", staged.filename),
            ("semantic_role", staged.semantic_role),
            ("source_material_id", staged.material_id),
            ("source_version_id", staged.version_id),
        ),
        lifecycle_status="AdmissionCandidate",
        predecessor_version_id=predecessor,
    )
    return DocumentVersionCandidate(
        canonical_record=record,
        artifacts=(artifact,),
        designated_rendition_role="original",
    )


def exact_staged_source_identities(
    *, staged: ExactCompanyStagedMaterial, actor: ActorContext
) -> tuple[Identity, Identity, Identity]:
    """Return exact staged Subject, Version and candidate Artifact identities."""

    if not isinstance(staged, ExactCompanyStagedMaterial) or not isinstance(actor, ActorContext):
        raise TypeError("exact staged identities require verified staged input and ActorContext")
    scope = actor.organization.organization_id.value
    return (
        Identity("staged-material", staged.material_id, scope),
        Identity("staged-material-version", staged.version_id, scope),
        Identity("artifact", f"company-staged-{staged.content_sha256[:32]}", scope),
    )


__all__ = [
    "ExactCompanyStagedMaterial",
    "build_staged_document_candidate",
    "exact_staged_source_identities",
    "resolve_exact_staged_material",
]

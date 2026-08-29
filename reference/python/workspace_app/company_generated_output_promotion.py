"""Product-local P10.05 bridge from Company TransientOutput to promotion input.

The bridge understands Company generation/staging metadata and therefore stays
outside the shared platform semantic owner.  It resolves one exact transient
output, re-hashes its bytes, proves the exact generating input was already an
admitted Company Asset version, inherits that source handling without widening
it, and constructs an immutable CAP-001 promotion candidate.

It grants no Authorization, Organizational Authority, Data Governance decision,
Validation or Consequential Approval and never changes the transient manifest's
``TransientOutput`` state.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.organizational_asset_admission import (
    CommittedOrganizationalAssetAdmission,
    OrganizationalAssetHandlingPolicy,
)
from arvectum_os_ref.security import ActorContext
from p10_05_company_output_ref.contract import PROMOTED_OUTPUT_DOCUMENT_SCOPE

from .access import AccessContext
from .company_asset_library import CompanyAssetAdmissionUnavailable, P1003CompanyAssetAdmissionExecutor
from .company_materials import CompanyMaterialUnavailable, CompanyMaterialsError, CompanyMaterialsStore


@dataclass(frozen=True, slots=True)
class ExactCompanyGeneratedOutput:
    output_id: str
    project_id: str
    filename: str
    media_type: str
    created_at: str
    created_by: str
    output_sha256: str
    source_material_id: str
    source_version_id: str
    source_sha256: str
    generation_profile: str
    generation_input_digest: str
    source_admission: CommittedOrganizationalAssetAdmission
    handling: OrganizationalAssetHandlingPolicy

    def __post_init__(self) -> None:
        if len(self.output_sha256) != 64 or len(self.source_sha256) != 64:
            raise ValueError("generated output must preserve exact SHA-256 digests")
        if not self.generation_profile or len(self.generation_input_digest) != 64:
            raise ValueError("generated output must preserve bounded generation evidence")


def _designation_handling(
    admission: CommittedOrganizationalAssetAdmission,
) -> OrganizationalAssetHandlingPolicy:
    payload = dict(admission.designation.payload)
    required = (
        "classification",
        "purpose",
        "rights",
        "retention_rule",
        "deletion_rule",
        "permitted_reuse",
    )
    if any(not isinstance(payload.get(key), str) or not str(payload[key]).strip() for key in required):
        raise CompanyAssetAdmissionUnavailable("admitted source handling evidence is incomplete")
    rights = tuple(part.strip() for part in str(payload["rights"]).split("|") if part.strip())
    reuse = tuple(part.strip() for part in str(payload["permitted_reuse"]).split("|") if part.strip())
    policy = OrganizationalAssetHandlingPolicy(
        classification=str(payload["classification"]),
        purpose=str(payload["purpose"]),
        rights=rights,
        retention_rule=str(payload["retention_rule"]),
        deletion_rule=str(payload["deletion_rule"]),
        permitted_reuse=reuse,
    )
    artifacts = admission.admitted_document.artifacts
    if len(artifacts) != 1 or artifacts[0].handling != policy.cap001_constraints:
        raise CompanyAssetAdmissionUnavailable("source designation handling differs from admitted Artifact")
    return policy


def resolve_exact_generated_output(
    *,
    store: CompanyMaterialsStore,
    asset_admission: P1003CompanyAssetAdmissionExecutor,
    access: AccessContext,
    output_id: str,
) -> ExactCompanyGeneratedOutput:
    """Resolve exact output bytes and exact already-admitted generating source."""

    if not isinstance(store, CompanyMaterialsStore):
        raise TypeError("generated-output promotion requires CompanyMaterialsStore")
    if not isinstance(asset_admission, P1003CompanyAssetAdmissionExecutor):
        raise TypeError("generated-output promotion requires the current P10.04 admission executor")
    if not isinstance(access, AccessContext):
        raise TypeError("generated-output promotion requires server-authorized AccessContext")

    path, manifest = store.output_path(access, output_id)
    try:
        content = path.read_bytes()
    except OSError as exc:
        raise CompanyMaterialUnavailable("exact transient output bytes unavailable") from exc
    digest = hashlib.sha256(content).hexdigest()
    if digest != manifest.get("output_sha256"):
        raise CompanyMaterialsError("exact transient output integrity mismatch")
    if manifest.get("state") != "TransientOutput" or manifest.get("canonical_authority") is not False:
        raise CompanyMaterialUnavailable("promotion source must remain an explicit TransientOutput")

    required_text = (
        "project_id",
        "filename",
        "media_type",
        "created_at",
        "created_by",
        "source_material_id",
        "source_version_id",
        "source_sha256",
        "generation_profile",
        "generation_input_digest",
    )
    if any(not isinstance(manifest.get(key), str) or not str(manifest[key]).strip() for key in required_text):
        raise CompanyMaterialUnavailable(
            "transient output lacks exact P10.05 generation evidence; regenerate it before promotion"
        )
    if len(str(manifest["generation_input_digest"])) != 64:
        raise CompanyMaterialUnavailable("transient output generation input digest is invalid")

    source_material_id = str(manifest["source_material_id"])
    source_version_id = str(manifest["source_version_id"])
    matches = tuple(
        item
        for item in asset_admission.state.committed
        if dict(item.admitted_document.canonical_record.payload).get("source_material_id") == source_material_id
        and dict(item.admitted_document.canonical_record.payload).get("source_version_id") == source_version_id
        and item.admitted_document.canonical_record.organization.organization_id == access.organization
    )
    if len(matches) != 1:
        raise CompanyAssetAdmissionUnavailable(
            "exact admitted source asset version is unavailable in the current bounded canonical state"
        )
    source = matches[0]
    source_artifacts = source.admitted_document.artifacts
    if len(source_artifacts) != 1:
        raise CompanyAssetAdmissionUnavailable("exact admitted source Artifact is ambiguous")
    if source_artifacts[0].integrity_ref != manifest["source_sha256"]:
        raise CompanyAssetAdmissionUnavailable("generated output source digest differs from admitted source")

    return ExactCompanyGeneratedOutput(
        output_id=output_id,
        project_id=str(manifest["project_id"]),
        filename=str(manifest["filename"]),
        media_type=str(manifest["media_type"]),
        created_at=str(manifest["created_at"]),
        created_by=str(manifest["created_by"]),
        output_sha256=digest,
        source_material_id=source_material_id,
        source_version_id=source_version_id,
        source_sha256=str(manifest["source_sha256"]),
        generation_profile=str(manifest["generation_profile"]),
        generation_input_digest=str(manifest["generation_input_digest"]),
        source_admission=source,
        handling=_designation_handling(source),
    )


def exact_generated_output_source_identities(
    *, output: ExactCompanyGeneratedOutput, actor: ActorContext
) -> tuple[Identity, Identity, Identity]:
    if not isinstance(output, ExactCompanyGeneratedOutput) or not isinstance(actor, ActorContext):
        raise TypeError("exact output identities require verified output and ActorContext")
    scope = actor.organization.organization_id.value
    return (
        Identity("transient-output", output.output_id, scope),
        Identity(
            "transient-output-version",
            f"{output.output_id}-{output.output_sha256[:24]}",
            scope,
        ),
        Identity("artifact", f"company-generated-{output.output_sha256[:32]}", scope),
    )


def build_generated_output_document_candidate(
    *,
    output: ExactCompanyGeneratedOutput,
    access: AccessContext,
    actor: ActorContext,
    candidate_created_at: datetime,
    document_title: str,
    semantic_role: str,
) -> DocumentVersionCandidate:
    """Map one exact transient Company output to a new Native Document candidate."""

    if not isinstance(output, ExactCompanyGeneratedOutput):
        raise TypeError("output must be ExactCompanyGeneratedOutput")
    if not isinstance(access, AccessContext) or not isinstance(actor, ActorContext):
        raise TypeError("candidate construction requires current AccessContext and ActorContext")
    if access.organization != actor.organization.organization_id or access.actor != actor.actual_principal.principal_id:
        raise PermissionError("Workspace access and governed promotion Actor/Organization must match")
    if not isinstance(candidate_created_at, datetime) or candidate_created_at.tzinfo is None or candidate_created_at.utcoffset() is None:
        raise ValueError("candidate_created_at must be timezone-aware")
    for label, value, maximum in (
        ("document_title", document_title, 320),
        ("semantic_role", semantic_role, 96),
    ):
        if not isinstance(value, str) or not value.strip() or len(" ".join(value.split())) > maximum:
            raise ValueError(f"{label} is outside the bounded Company promotion contract")

    scope = actor.organization.organization_id.value
    source_subject, source_version, artifact_id = exact_generated_output_source_identities(
        output=output, actor=actor
    )
    source_admission = output.source_admission
    source_record = source_admission.admitted_document.canonical_record
    source_artifact = source_admission.admitted_document.artifacts[0]
    document_subject = Identity("document", f"generated-output-{output.output_id}", scope)
    document_version = Identity(
        "document-version", f"generated-output-{output.output_id}-{output.output_sha256[:24]}", scope
    )
    handling = HandlingConstraints(
        classification=output.handling.classification,
        purpose=output.handling.purpose,
        rights=output.handling.rights,
        retention_rule=output.handling.retention_rule,
    )
    artifact = ArtifactContent(
        artifact_id=artifact_id,
        organization=actor.organization,
        content_ref=f"sha256:{output.output_sha256}",
        media_type=output.media_type,
        integrity_ref=output.output_sha256,
        rendition_role="original",
        handling=handling,
        source_artifact_ids=(source_artifact.artifact_id,),
        transformation=output.generation_profile,
        storage_locator="owner-local-company-materials/transient",
    )
    provenance = tuple(
        dict.fromkeys(
            (
                actor.actual_principal.principal_id,
                source_subject,
                source_version,
                source_record.subject_id,
                source_record.version_id,
                source_artifact.artifact_id,
                source_admission.designation.subject_id,
                source_admission.designation.version_id,
            )
        )
    )
    record = CanonicalRecord(
        subject_id=document_subject,
        version_id=document_version,
        semantic_type="platform.document",
        schema_version="p10.05-company-generated-output-1",
        organization=actor.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=PROMOTED_OUTPUT_DOCUMENT_SCOPE,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=candidate_created_at,
        provenance_refs=provenance,
        integrity_metadata=(
            ("representation", "p10.05-exact-reviewed-transient-output"),
            ("source_output_sha256", output.output_sha256),
            ("generation_profile", output.generation_profile),
            ("generation_input_digest", output.generation_input_digest),
            ("source_state", "TransientOutput"),
        ),
        payload=(
            ("project_id", output.project_id),
            ("filename", output.filename),
            ("document_title", " ".join(document_title.split())),
            ("semantic_role", " ".join(semantic_role.split())),
            ("source_output_id", output.output_id),
            ("source_material_id", output.source_material_id),
            ("source_version_id", output.source_version_id),
        ),
        lifecycle_status="PromotionCandidate",
        predecessor_version_id=None,
    )
    return DocumentVersionCandidate(
        canonical_record=record,
        artifacts=(artifact,),
        designated_rendition_role="original",
    )


__all__ = [
    "ExactCompanyGeneratedOutput",
    "build_generated_output_document_candidate",
    "exact_generated_output_source_identities",
    "resolve_exact_generated_output",
]

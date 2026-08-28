"""Executable projection of canonical P10.02 Product Contract 0.2.0 for P10.03.

The canonical Product Contract already authorizes bounded real reliance for
``company.asset.admit-staged-version`` and ``company.asset.admit-external-reference``.
This module does not create Product Contract 0.2.1.  It creates a distinct
non-authoritative executable projection while pinning the exact immutable P10.02
publication and keeps all Company-specific operation names at the product edge.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Final

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAPABILITY_CONTRACT_VERSION,
    CAP_001_DOCUMENT_ARTIFACT,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessDeclaration,
    CanonicalAccessMode,
    PlatformDependencyDeclaration,
    ProductContract,
    ProductContractLifecycle,
    ProductOperationDeclaration,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope
from arvectum_os_ref.workflow import OperationSideEffectClass

P10_02_CANONICAL_CONTRACT_PATH: Final = (
    "docs/contracts/P10-02-ARVECTUM-COMPANY-WORKSPACE-PRODUCT-CONTRACT-PROVISIONAL-v0.2.0.md"
)
P10_02_CANONICAL_BLOB_SHA: Final = "ad0553aff1e17954215c16261b2c8cc3efe404d3"
P10_02_APPROVED_DRAFT_BLOB_SHA: Final = "a92c1d1aac54d565d3d32ce746925620c9d1fd12"
P10_02_CONTRACT_SUBJECT_VALUE: Final = "p9-11-f11-arvectum-company-workspace"
P10_02_CONTRACT_VERSION_VALUE: Final = "p10-02-arvectum-company-workspace-v0.2.0"
P10_03_PROJECTION_SUBJECT_VALUE: Final = "p10-03-p10-02-executable-projection"

PRODUCT_ID_VALUE: Final = "arvectum-company-workspace"
PRODUCT_VERSION: Final = "0.2"

OP_ADMIT_STAGED_VERSION: Final = "company.asset.admit-staged-version"
OP_ADMIT_EXTERNAL_REFERENCE: Final = "company.asset.admit-external-reference"

# The exact Document authority scopes are product-boundary declarations.  They
# do not create a platform-wide taxonomy or force any physical storage model.
NATIVE_ASSET_DOCUMENT_SCOPE: Final = "company.asset/document-native"
EXTERNAL_ASSET_DOCUMENT_SCOPE: Final = "company.asset/document-external-reference"
DOCUMENT_SEMANTIC_TYPE: Final = "platform.document"

REQUIRED_ADMISSION_GATES: Final = (
    GovernedGateKind.ACTOR_ASSURANCE,
    GovernedGateKind.AUTHORIZATION,
    GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
    GovernedGateKind.DATA_GOVERNANCE,
    GovernedGateKind.VALIDATION,
    GovernedGateKind.CONSEQUENTIAL_APPROVAL,
)


def p10_02_canonical_version_pin(*, organization: OrganizationScope) -> GovernedVersionPin:
    """Return the exact governed runtime pin for canonical P10.02 0.2.0.

    The Subject value follows the explicit P10.02 statement that the P9.11-F11
    subject lineage remains unchanged.  The Version value is the internal runtime
    identity for this immutable 0.2.0 publication and is additionally anchored to
    its Git blob SHA by the executable projection record below.
    """

    if not isinstance(organization, OrganizationScope):
        raise ValueError("organization must be an OrganizationScope")
    scope = organization.organization_id.value
    return GovernedVersionPin(
        subject_id=Identity("product-contract-subject", P10_02_CONTRACT_SUBJECT_VALUE, scope),
        version_id=Identity("product-contract-version", P10_02_CONTRACT_VERSION_VALUE, scope),
        semantic_type="platform.product-contract",
        authority_scope="platform.product-contract/boundary",
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )


@dataclass(frozen=True, slots=True)
class P1003ExecutableProductContractProjection(ProductContract):
    """Distinct executable projection pinned to canonical P10.02 0.2.0."""

    canonical_source_pin: GovernedVersionPin
    canonical_source_path: str
    canonical_source_blob_sha: str
    approved_draft_blob_sha: str

    def __post_init__(self) -> None:
        ProductContract.__post_init__(self)
        if self.canonical_source_path != P10_02_CANONICAL_CONTRACT_PATH:
            raise ValueError("canonical_source_path mismatch")
        if self.canonical_source_blob_sha != P10_02_CANONICAL_BLOB_SHA:
            raise ValueError("canonical_source_blob_sha mismatch")
        if self.approved_draft_blob_sha != P10_02_APPROVED_DRAFT_BLOB_SHA:
            raise ValueError("approved_draft_blob_sha mismatch")
        if self.canonical_source_pin != p10_02_canonical_version_pin(organization=self.organization):
            raise ValueError("canonical_source_pin mismatch")
        if self.record.subject_id == self.canonical_source_pin.subject_id:
            raise ValueError("executable projection must not reuse canonical Product Contract Subject identity")
        if self.record.version_id == self.canonical_source_pin.version_id:
            raise ValueError("executable projection must not reuse canonical Product Contract Version identity")
        if (
            self.canonical_source_pin.subject_id not in self.record.provenance_refs
            or self.canonical_source_pin.version_id not in self.record.provenance_refs
        ):
            raise ValueError("projection provenance must preserve canonical P10.02 Subject/Version")

    @property
    def version_pin(self) -> GovernedVersionPin:
        # Runtime reliance is pinned to the canonical Product Contract, not to
        # this implementation projection.
        return self.canonical_source_pin


def _access(*, authority_mode: AuthorityMode, authority_scope: str, source: str) -> CanonicalAccessDeclaration:
    return CanonicalAccessDeclaration(
        semantic_type=DOCUMENT_SEMANTIC_TYPE,
        authority_mode=authority_mode,
        authority_scope=authority_scope,
        access_modes=(CanonicalAccessMode.READ, CanonicalAccessMode.WRITE),
        authoritative_source=source,
        failure_behavior=(
            "Fail closed if exact version, authority mapping, Organization scope, current governance "
            "or integrity evidence cannot be resolved."
        ),
    )


def build_p10_03_product_contract_projection(
    *, actor: ActorContext, created_at: datetime
) -> P1003ExecutableProductContractProjection:
    """Build the smallest executable projection admitted by canonical P10.02."""

    if not isinstance(actor, ActorContext):
        raise ValueError("actor must be an attributable ActorContext")
    if not isinstance(created_at, datetime) or created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")

    organization = actor.organization
    scope = organization.organization_id.value
    owner = actor.actual_principal.principal_id
    product_id = Identity("product", PRODUCT_ID_VALUE, scope)
    canonical_pin = p10_02_canonical_version_pin(organization=organization)

    native_access = _access(
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=NATIVE_ASSET_DOCUMENT_SCOPE,
        source="ООО «Арвектум» within the declared Company-held asset scope",
    )
    external_access = _access(
        authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
        authority_scope=EXTERNAL_ASSET_DOCUMENT_SCOPE,
        source="declared external authoritative system; Arvectum OS stores governed reference only",
    )

    dependency = PlatformDependencyDeclaration(
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        contract_version=CAPABILITY_CONTRACT_VERSION,
        allowed_operations=(OP_ADMIT_STAGED_VERSION, OP_ADMIT_EXTERNAL_REFERENCE),
        provider_responsibility=(
            "Provide domain-neutral Document/Artifact identity, exact-version admission and immutable "
            "governed representation semantics without Company taxonomy."
        ),
        consumer_responsibility=(
            "Resolve Company business meaning plus current Authorization, Organizational Authority, "
            "Data Governance, Validation and Consequential Approval before admission."
        ),
        failure_behavior=(
            "No canonical Document/Asset state is admitted when exact source/version/integrity, authority, "
            "handling or execution evidence is unresolved."
        ),
        provisional=True,
    )

    staged_operation = ProductOperationDeclaration(
        operation_name=OP_ADMIT_STAGED_VERSION,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
        required_gates=REQUIRED_ADMISSION_GATES,
        canonical_accesses=(native_access,),
        failure_behavior=(
            "Admit only the exact staged Company material version under Native authority within the declared "
            "Company-held scope; staging itself remains StagedNonCanonical."
        ),
    )
    external_operation = ProductOperationDeclaration(
        operation_name=OP_ADMIT_EXTERNAL_REFERENCE,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
        required_gates=REQUIRED_ADMISSION_GATES,
        canonical_accesses=(external_access,),
        failure_behavior=(
            "Admit only a governed External Reference after current freshness/conflict/availability resolution; "
            "the external system remains authoritative and is not mutated."
        ),
    )

    digest_input = (
        f"{scope}:{owner.value}:{created_at.isoformat()}:{P10_02_CANONICAL_BLOB_SHA}:"
        f"{P10_02_APPROVED_DRAFT_BLOB_SHA}"
    ).encode("utf-8")
    projection_digest = hashlib.sha256(digest_input).hexdigest()[:16]
    projection_subject = Identity(
        "product-contract-projection-subject", P10_03_PROJECTION_SUBJECT_VALUE, scope
    )
    projection_version = Identity(
        "product-contract-projection-version",
        f"p10-03-p10-02-projection-{projection_digest}",
        scope,
    )

    record = CanonicalRecord(
        subject_id=projection_subject,
        version_id=projection_version,
        semantic_type="platform.product-contract",
        schema_version="p10.03-projection-1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.product-contract/boundary",
        accountable_owner_id=owner,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(owner, product_id, canonical_pin.subject_id, canonical_pin.version_id),
        integrity_metadata=(
            ("representation", "p10.03-non-authoritative-executable-projection"),
            ("canonical_source_path", P10_02_CANONICAL_CONTRACT_PATH),
            ("canonical_source_blob_sha", P10_02_CANONICAL_BLOB_SHA),
            ("approved_draft_blob_sha", P10_02_APPROVED_DRAFT_BLOB_SHA),
        ),
        payload=(
            ("canonical_contract", P10_02_CANONICAL_CONTRACT_PATH),
            ("contract_version", "0.2.0"),
            ("projection", "P10.03 Organizational Asset admission executable projection"),
        ),
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )

    return P1003ExecutableProductContractProjection(
        record=record,
        product_id=product_id,
        product_version=PRODUCT_VERSION,
        bounded_scope=(
            "P10.02 bounded Company Organizational Asset admission for exact staged versions and governed "
            "External References only. Generated-output promotion remains outside P10.03."
        ),
        compatibility_assumptions=(
            "CAP-001 1.0.0 reference semantics remain compatible with the P10.02 bounded reliance.",
            "RFC-0005 Governed Execution remains the only path for this consequential canonical mutation.",
            "No approved decision-authority delegation exists; residual owner authority remains explicit.",
        ),
        dependencies=(dependency,),
        operations=(staged_operation, external_operation),
        portability_responsibility=(
            "Product preserves Company-owned taxonomy outside shared semantics and keeps source/version/provenance "
            "references exportable without depending on hidden platform state."
        ),
        retention_deletion_responsibility=(
            "Product resolves purpose, classification, rights, retention, deletion and permitted reuse before each "
            "admission; CAP-001 preserves the resulting governed evidence without inventing Company policy."
        ),
        review_condition=(
            "Review on material P10.02 boundary change, CAP-001/RFC-0005 incompatibility, approved authority "
            "delegation, or before introducing any new durable mechanism."
        ),
        exit_path=(
            "Stop new admissions, preserve admitted immutable history/evidence, keep external authority mapping, "
            "and migrate through a new governed Product Contract/version if the boundary changes."
        ),
        canonical_source_pin=canonical_pin,
        canonical_source_path=P10_02_CANONICAL_CONTRACT_PATH,
        canonical_source_blob_sha=P10_02_CANONICAL_BLOB_SHA,
        approved_draft_blob_sha=P10_02_APPROVED_DRAFT_BLOB_SHA,
    )


__all__ = [
    "DOCUMENT_SEMANTIC_TYPE",
    "EXTERNAL_ASSET_DOCUMENT_SCOPE",
    "NATIVE_ASSET_DOCUMENT_SCOPE",
    "OP_ADMIT_EXTERNAL_REFERENCE",
    "OP_ADMIT_STAGED_VERSION",
    "P10_02_APPROVED_DRAFT_BLOB_SHA",
    "P10_02_CANONICAL_BLOB_SHA",
    "P10_02_CANONICAL_CONTRACT_PATH",
    "P1003ExecutableProductContractProjection",
    "PRODUCT_ID_VALUE",
    "PRODUCT_VERSION",
    "REQUIRED_ADMISSION_GATES",
    "build_p10_03_product_contract_projection",
    "p10_02_canonical_version_pin",
]

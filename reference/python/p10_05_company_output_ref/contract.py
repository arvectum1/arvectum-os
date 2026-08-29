"""Executable projection of canonical P10.02 Product Contract 0.2.0 for P10.05.

Canonical P10.02 already admits ``company.generated-output.promote-reviewed``
but explicitly withheld real reliance until P10.05 implementation/review.  This
module creates only a non-authoritative executable projection pinned to that
same immutable Provisional 0.2.0 publication.  It does not create Product
Contract 0.2.1 or broaden the approved boundary.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from typing import Final

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.organizational_asset_admission import (
    ORGANIZATIONAL_ASSET_DESIGNATION_AUTHORITY_SCOPE,
    ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE,
)
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
from arvectum_os_ref.security import ActorContext
from arvectum_os_ref.workflow import OperationSideEffectClass
from p10_03_company_asset_ref.contract import (
    DOCUMENT_SEMANTIC_TYPE,
    NATIVE_ASSET_DOCUMENT_SCOPE,
    P10_02_APPROVED_DRAFT_BLOB_SHA,
    P10_02_CANONICAL_BLOB_SHA,
    P10_02_CANONICAL_CONTRACT_PATH,
    PRODUCT_ID_VALUE,
    PRODUCT_VERSION,
    REQUIRED_ADMISSION_GATES,
    p10_02_canonical_version_pin,
)


OP_PROMOTE_REVIEWED_OUTPUT: Final = "company.generated-output.promote-reviewed"
PROMOTED_OUTPUT_DOCUMENT_SCOPE: Final = "company.generated-output/document-native"
P10_05_PROJECTION_SUBJECT_VALUE: Final = "p10-05-p10-02-generated-output-promotion-projection"


@dataclass(frozen=True, slots=True)
class P1005ExecutableProductContractProjection(ProductContract):
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
            raise ValueError("executable projection must not reuse canonical Product Contract Subject")
        if self.record.version_id == self.canonical_source_pin.version_id:
            raise ValueError("executable projection must not reuse canonical Product Contract Version")
        if (
            self.canonical_source_pin.subject_id not in self.record.provenance_refs
            or self.canonical_source_pin.version_id not in self.record.provenance_refs
        ):
            raise ValueError("projection provenance must preserve canonical P10.02 Subject/Version")

    @property
    def version_pin(self) -> GovernedVersionPin:
        return self.canonical_source_pin


def _document_access(
    *, authority_scope: str, modes: tuple[CanonicalAccessMode, ...]
) -> CanonicalAccessDeclaration:
    return CanonicalAccessDeclaration(
        semantic_type=DOCUMENT_SEMANTIC_TYPE,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=authority_scope,
        access_modes=modes,
        authoritative_source="ООО «Арвектум» within the exact reviewed Company-held document scope",
        failure_behavior=(
            "Fail closed if exact version, Organization scope, provenance, reviewed handling or integrity "
            "cannot be resolved for the promotion command."
        ),
    )


def _designation_access() -> CanonicalAccessDeclaration:
    return CanonicalAccessDeclaration(
        semantic_type=ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=ORGANIZATIONAL_ASSET_DESIGNATION_AUTHORITY_SCOPE,
        access_modes=(CanonicalAccessMode.WRITE,),
        authoritative_source="Arvectum OS governed Organizational Asset designation",
        failure_behavior=(
            "No designation may be written outside the exact reviewed-output Product Contract, Workflow, "
            "authority, approval and source-version evidence."
        ),
    )


def build_p10_05_product_contract_projection(
    *, actor: ActorContext, created_at: datetime
) -> P1005ExecutableProductContractProjection:
    if not isinstance(actor, ActorContext):
        raise ValueError("actor must be an attributable ActorContext")
    if not isinstance(created_at, datetime) or created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")

    organization = actor.organization
    scope = organization.organization_id.value
    owner = actor.actual_principal.principal_id
    product_id = Identity("product", PRODUCT_ID_VALUE, scope)
    canonical_pin = p10_02_canonical_version_pin(organization=organization)

    dependency = PlatformDependencyDeclaration(
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        contract_version=CAPABILITY_CONTRACT_VERSION,
        allowed_operations=(OP_PROMOTE_REVIEWED_OUTPUT,),
        provider_responsibility=(
            "Provide domain-neutral exact Document/Artifact admission and immutable governed representation "
            "semantics without Company document taxonomy."
        ),
        consumer_responsibility=(
            "Resolve exact transient output/input provenance plus current Authorization, Organizational Authority, "
            "Data Governance, Validation and Consequential Approval before promotion."
        ),
        failure_behavior=(
            "No canonical Document/Asset state is created when output bytes/digest, admitted input version, "
            "review disposition, handling or execution evidence is unresolved."
        ),
        provisional=True,
    )

    operation = ProductOperationDeclaration(
        operation_name=OP_PROMOTE_REVIEWED_OUTPUT,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
        required_gates=REQUIRED_ADMISSION_GATES,
        canonical_accesses=(
            _document_access(
                authority_scope=PROMOTED_OUTPUT_DOCUMENT_SCOPE,
                modes=(CanonicalAccessMode.READ, CanonicalAccessMode.WRITE),
            ),
            _document_access(
                authority_scope=NATIVE_ASSET_DOCUMENT_SCOPE,
                modes=(CanonicalAccessMode.READ,),
            ),
            _designation_access(),
        ),
        failure_behavior=(
            "Promote only one exact owner-reviewed TransientOutput. The transient source remains non-canonical; "
            "a new immutable Native Document/Artifact version and explicit asset designation are written only "
            "inside the same admitted Governed Execution."
        ),
    )

    digest = hashlib.sha256(
        (
            f"{scope}:{owner.value}:{created_at.isoformat()}:{P10_02_CANONICAL_BLOB_SHA}:"
            f"{P10_02_APPROVED_DRAFT_BLOB_SHA}:{OP_PROMOTE_REVIEWED_OUTPUT}"
        ).encode("utf-8")
    ).hexdigest()[:16]
    projection_subject = Identity(
        "product-contract-projection-subject", P10_05_PROJECTION_SUBJECT_VALUE, scope
    )
    projection_version = Identity(
        "product-contract-projection-version", f"p10-05-p10-02-projection-{digest}", scope
    )
    record = CanonicalRecord(
        subject_id=projection_subject,
        version_id=projection_version,
        semantic_type="platform.product-contract",
        schema_version="p10.05-projection-1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.product-contract/boundary",
        accountable_owner_id=owner,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(owner, product_id, canonical_pin.subject_id, canonical_pin.version_id),
        integrity_metadata=(
            ("representation", "p10.05-non-authoritative-executable-projection"),
            ("canonical_source_path", P10_02_CANONICAL_CONTRACT_PATH),
            ("canonical_source_blob_sha", P10_02_CANONICAL_BLOB_SHA),
            ("approved_draft_blob_sha", P10_02_APPROVED_DRAFT_BLOB_SHA),
        ),
        payload=(
            ("canonical_contract", P10_02_CANONICAL_CONTRACT_PATH),
            ("contract_version", "0.2.0"),
            ("projection", "P10.05 reviewed generated-output promotion executable projection"),
        ),
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )

    return P1005ExecutableProductContractProjection(
        record=record,
        product_id=product_id,
        product_version=PRODUCT_VERSION,
        bounded_scope=(
            "P10.02 exact reviewed generated TransientOutput promotion only. External send/sign/publish and "
            "Knowledge promotion remain excluded."
        ),
        compatibility_assumptions=(
            "CAP-001 1.0.0 reference semantics remain compatible with the P10.02 bounded reliance.",
            "RFC-0005 Governed Execution remains the only path for this canonical mutation.",
            "Residual owner authority remains explicit because no exact approved delegation applies.",
            "The P10.04 in-memory/reference canonical asset foundation remains the current bounded state model.",
        ),
        dependencies=(dependency,),
        operations=(operation,),
        portability_responsibility=(
            "Product preserves exact output/input identities, digests and provenance without hidden platform state."
        ),
        retention_deletion_responsibility=(
            "Product resolves and confirms classification, purpose, rights, retention, deletion and permitted reuse "
            "before promotion; derived output handling may not silently broaden source constraints."
        ),
        review_condition=(
            "Review on material P10.02 boundary change, CAP-001/RFC-0005 incompatibility, authority delegation, "
            "handling-policy expansion or before selecting a new durable mechanism."
        ),
        exit_path=(
            "Stop new promotions, preserve admitted immutable history/evidence and migrate through a governed "
            "Product Contract version if the boundary changes."
        ),
        canonical_source_pin=canonical_pin,
        canonical_source_path=P10_02_CANONICAL_CONTRACT_PATH,
        canonical_source_blob_sha=P10_02_CANONICAL_BLOB_SHA,
        approved_draft_blob_sha=P10_02_APPROVED_DRAFT_BLOB_SHA,
    )


__all__ = [
    "OP_PROMOTE_REVIEWED_OUTPUT",
    "PROMOTED_OUTPUT_DOCUMENT_SCOPE",
    "P1005ExecutableProductContractProjection",
    "build_p10_05_product_contract_projection",
]

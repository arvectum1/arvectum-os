"""P10.05 productive owner-operated provider for reviewed output promotion.

The provider composes the exact operation already admitted by P10.02 0.2.0. It
does not make review state, button visibility, Workspace access or Product
Contract possession into authority. One promotion command independently
revalidates the owner credential and exact least-privilege Authorization grant,
then constructs all six RFC-0005 gate decisions from exact output/input/review
and inherited handling evidence before the canonical semantic owner may run.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

import p7_04_persistent_access as p704
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.governed_execution import (
    GovernedGateKind,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import compose_integration_adapters
from arvectum_os_ref.organizational_asset_admission import AssetAdmissionAuthorityEvidence
from arvectum_os_ref.product_capability_consumption import (
    CAPABILITY_CONTRACT_VERSION,
    CAP_001_DOCUMENT_ARTIFACT,
)
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowLifecycle,
    WorkflowOperation,
)
from p10_03_company_asset_ref.contract import P10_02_CANONICAL_CONTRACT_PATH
from p10_05_company_output_ref.contract import (
    OP_PROMOTE_REVIEWED_OUTPUT,
    build_p10_05_product_contract_projection,
)

from .access import AccessContext, P704AccessResolver
from .company_generated_output_promotion import ExactCompanyGeneratedOutput
from .company_generated_outputs import (
    CompanyGeneratedOutputGovernedProvider,
    CompanyGeneratedOutputPromotionUnavailable,
    CompanyGeneratedOutputReviewEvidence,
    PreparedCompanyGeneratedOutputPromotion,
)


COMPANY_GENERATED_OUTPUT_PROMOTION_RESOURCE = "company-generated-outputs"
P10_01_AUTHORITY_MATRIX_PATH = "docs/reviews/P10-01-asset-admission-real-work-authority-matrix.md"
CAP001_SUPPORT_EVIDENCE = "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"


def _identity_payload(value: Identity) -> dict[str, str]:
    return {"namespace": value.namespace, "value": value.value, "scope": value.scope}


def _digest(*parts: object) -> str:
    raw = "\x1f".join(str(part) for part in parts).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:24]


def _governed_versions() -> tuple[GovernedDependencyVersionEvidence, ...]:
    return (
        GovernedDependencyVersionEvidence(
            CAP_001_DOCUMENT_ARTIFACT,
            CAPABILITY_CONTRACT_VERSION,
            DependencySupportDisposition.SUPPORTED,
            CAP001_SUPPORT_EVIDENCE,
        ),
    )


class P1005OwnerCompanyGeneratedOutputPromotionProvider(CompanyGeneratedOutputGovernedProvider):
    """Compose one exact owner promotion command without manufacturing authority."""

    def __init__(self, runtime_root: Path) -> None:
        self.runtime_root = runtime_root.expanduser()

    def _require_owner_operated_actor(self, access: AccessContext) -> None:
        if not isinstance(access, AccessContext) or access.principal_kind != "human":
            raise CompanyGeneratedOutputPromotionUnavailable(
                "reviewed-output promotion requires an attributable human owner"
            )
        try:
            state = p704.load_access_store(self.runtime_root)
        except p704.P704Error as exc:
            raise CompanyGeneratedOutputPromotionUnavailable(
                "current P7.04 access state is unavailable"
            ) from exc
        humans = tuple(
            record
            for record in state["principals"].values()
            if record["kind"] == "human" and record["status"] == "enabled"
        )
        if len(humans) != 1 or humans[0]["identity"] != _identity_payload(access.actor):
            raise CompanyGeneratedOutputPromotionUnavailable(
                "current residual-owner scope cannot be attributed to exactly one enabled human principal"
            )
        if state["organization"] != _identity_payload(access.organization):
            raise CompanyGeneratedOutputPromotionUnavailable("promotion Organization scope changed")

    def _authorize(self, access: AccessContext):
        self._require_owner_operated_actor(access)
        credential_file = self.runtime_root / "secrets" / "p7-04" / f"{access.credential_id}.secret"
        decision = p704.authorize_from_credential_file(
            self.runtime_root,
            organization=access.organization,
            principal=access.actor,
            credential_id=access.credential_id,
            credential_file=credential_file,
            operation=OP_PROMOTE_REVIEWED_OUTPUT,
            resource=COMPANY_GENERATED_OUTPUT_PROMOTION_RESOURCE,
            access_path="local",
        )
        if (
            not decision.allowed
            or decision.principal_kind != "human"
            or not decision.grant_id
            or decision.organizational_authority_satisfied
            or decision.consequential_approval_satisfied
        ):
            raise CompanyGeneratedOutputPromotionUnavailable(
                "exact reviewed-output promotion Authorization grant is absent or invalid"
            )
        return decision

    def available(self, access: AccessContext) -> bool:
        try:
            self._authorize(access)
        except (CompanyGeneratedOutputPromotionUnavailable, p704.P704Error, OSError):
            return False
        return True

    def actor_for(self, access: AccessContext) -> ActorContext:
        self._require_owner_operated_actor(access)
        scope = access.organization.value
        return ActorContext(
            Principal(access.actor),
            OrganizationScope(access.organization),
            authentication_evidence_refs=(Identity("credential-evidence", access.credential_id, scope),),
        )

    def _workflow(
        self,
        *,
        actor: ActorContext,
        candidate,
        contract,
        intent: str,
        created_at: datetime,
    ) -> WorkflowDefinition:
        record = candidate.canonical_record
        scope = actor.organization.organization_id.value
        authority_matrix = Identity("governance-source", "p10-01-owner-output-promotion-matrix", scope)
        workflow_record = CanonicalRecord(
            subject_id=Identity("workflow-subject", f"p10-05-output-promotion-{intent}", scope),
            version_id=Identity("workflow-version", f"p10-05-output-promotion-{intent}-v1", scope),
            semantic_type="platform.workflow",
            schema_version="p10.05-owner-command-1",
            organization=actor.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.workflow/definition",
            accountable_owner_id=actor.actual_principal.principal_id,
            creation_actor=actor,
            created_at=created_at,
            provenance_refs=(
                actor.actual_principal.principal_id,
                record.subject_id,
                record.version_id,
                contract.version_pin.subject_id,
                contract.version_pin.version_id,
                authority_matrix,
            ),
            integrity_metadata=(
                ("representation", "p10.05-exact-owner-command-workflow"),
                ("authority_matrix", P10_01_AUTHORITY_MATRIX_PATH),
                ("product_contract", P10_02_CANONICAL_CONTRACT_PATH),
            ),
            payload=(("operation", OP_PROMOTE_REVIEWED_OUTPUT), ("intent", intent)),
            lifecycle_status=WorkflowLifecycle.APPROVED.value,
            predecessor_version_id=None,
        )
        return WorkflowDefinition(
            record=workflow_record,
            operations=(
                WorkflowOperation(
                    semantic_name=OP_PROMOTE_REVIEWED_OUTPUT,
                    target_subject_id=record.subject_id,
                    target_semantic_type=record.semantic_type,
                    side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
                ),
            ),
        )

    def _basis_refs(
        self,
        *,
        access: AccessContext,
        output: ExactCompanyGeneratedOutput,
        review: CompanyGeneratedOutputReviewEvidence,
        intent: str,
        grant_id: str,
    ) -> dict[GovernedGateKind, Identity]:
        scope = access.organization.value
        handling = _digest(
            output.handling.classification,
            output.handling.purpose,
            *output.handling.rights,
            output.handling.retention_rule,
            output.handling.deletion_rule,
            *output.handling.permitted_reuse,
            review.handling_digest,
        )
        validation = _digest(
            output.output_id,
            output.output_sha256,
            review.updated_at,
            review.review_digest,
            review.source_document_version,
            review.source_artifact_id,
            review.source_designation_version,
        )
        return {
            GovernedGateKind.ACTOR_ASSURANCE: Identity(
                "credential-evidence", access.credential_id, scope
            ),
            GovernedGateKind.AUTHORIZATION: Identity("authorization-grant", grant_id, scope),
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY: Identity(
                "governance-basis", "p10-01-current-residual-owner-authority", scope
            ),
            GovernedGateKind.DATA_GOVERNANCE: Identity(
                "company-generated-output-handling-basis", f"{output.output_id}-{handling}", scope
            ),
            GovernedGateKind.VALIDATION: Identity(
                "company-generated-output-validation-basis", f"{output.output_id}-{validation}", scope
            ),
            GovernedGateKind.CONSEQUENTIAL_APPROVAL: Identity(
                "owner-command-approval", f"company-generated-output-promote-{intent}", scope
            ),
        }

    def prepare(
        self,
        *,
        access: AccessContext,
        candidate,
        output: ExactCompanyGeneratedOutput,
        review: CompanyGeneratedOutputReviewEvidence,
    ) -> PreparedCompanyGeneratedOutputPromotion:
        decision = self._authorize(access)
        actor = self.actor_for(access)
        record = candidate.canonical_record
        if record.organization != actor.organization or record.creation_actor != actor:
            raise CompanyGeneratedOutputPromotionUnavailable(
                "promotion candidate Actor/Organization changed before command"
            )
        if dict(record.integrity_metadata).get("source_output_sha256") != output.output_sha256:
            raise CompanyGeneratedOutputPromotionUnavailable(
                "promotion candidate digest no longer matches exact transient output"
            )
        expected_actor = f"{access.actor.namespace}:{access.actor.value}@{access.actor.scope}"
        if review.actor != expected_actor:
            raise CompanyGeneratedOutputPromotionUnavailable("review Actor changed before promotion")

        command_at = record.created_at.astimezone(timezone.utc)
        intent = _digest(
            access.actor.value,
            output.output_id,
            output.output_sha256,
            review.review_digest,
            command_at.isoformat(),
            OP_PROMOTE_REVIEWED_OUTPUT,
        )
        contract = build_p10_05_product_contract_projection(actor=actor, created_at=command_at)
        governed_versions = _governed_versions()
        adapters = compose_integration_adapters(
            contract=contract,
            actor=actor,
            effective_product_contract=contract.version_pin,
            governed_versions=governed_versions,
        )
        workflow = self._workflow(
            actor=actor,
            candidate=candidate,
            contract=contract,
            intent=intent,
            created_at=command_at,
        )
        source_record = output.source_admission.admitted_document.canonical_record
        interaction = ProductRuntimeInteraction(
            organization=actor.organization,
            product_id=contract.product_id,
            product_version=contract.product_version,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            workflow=workflow,
            operation_name=OP_PROMOTE_REVIEWED_OUTPUT,
            material_inputs=(record, source_record),
            required_gates=tuple(review_kind for review_kind in GovernedGateKind),
        )
        scope = actor.organization.organization_id.value
        created = adapters.facade.start_governed_execution(
            interaction=interaction,
            execution_id=Identity("execution-subject", f"p10-05-output-promotion-{intent}", scope),
            version_id=Identity("execution-version", f"p10-05-output-promotion-{intent}-v1", scope),
            created_at=command_at + timedelta(seconds=1),
            governed_versions=governed_versions,
        )
        awaiting = await_required_gates(
            created,
            version_id=Identity("execution-version", f"p10-05-output-promotion-{intent}-v2", scope),
            actor=actor,
            created_at=command_at + timedelta(seconds=2),
        )
        bases = self._basis_refs(
            access=access,
            output=output,
            review=review,
            intent=intent,
            grant_id=str(decision.grant_id),
        )
        decisions = tuple(
            build_governed_gate_decision(
                execution=awaiting,
                kind=kind,
                outcome=GovernedGateOutcome.ALLOW,
                decision_actor=actor,
                basis_ref=bases[kind],
                decision_id=Identity(
                    "gate-decision-subject", f"p10-05-{intent}-{kind.value.lower()}", scope
                ),
                version_id=Identity(
                    "gate-decision-version", f"p10-05-{intent}-{kind.value.lower()}-v1", scope
                ),
                created_at=command_at + timedelta(seconds=3 + index),
            )
            for index, kind in enumerate(awaiting.required_gates)
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=decisions,
            version_id=Identity("execution-version", f"p10-05-output-promotion-{intent}-v3", scope),
            actor=actor,
            created_at=command_at + timedelta(seconds=10),
        )
        by_kind = {item.kind: item for item in ready.gate_decisions}
        authority = AssetAdmissionAuthorityEvidence(
            decision_authority_id=actor.actual_principal.principal_id,
            organizational_authority_basis_ref=by_kind[
                GovernedGateKind.ORGANIZATIONAL_AUTHORITY
            ].basis_ref,
            consequential_approval_basis_ref=by_kind[
                GovernedGateKind.CONSEQUENTIAL_APPROVAL
            ].basis_ref,
        )
        return PreparedCompanyGeneratedOutputPromotion(
            actor=actor,
            capability_adapter=adapters.capabilities,
            execution=ready,
            authority=authority,
            occurred_at=command_at + timedelta(seconds=11),
            recorded_at=command_at + timedelta(seconds=12),
        )


def provision_company_generated_output_promotion_grant(runtime_root: Path) -> str:
    """Explicitly provision only the exact local reviewed-output promotion grant."""

    root = runtime_root.expanduser()
    access = P704AccessResolver(root).authorize()
    if access.principal_kind != "human":
        raise CompanyGeneratedOutputPromotionUnavailable(
            "only the current human owner may receive the promotion grant"
        )
    grant_id = p704.grant_access(
        root,
        access.actor,
        operation=OP_PROMOTE_REVIEWED_OUTPUT,
        resource=COMPANY_GENERATED_OUTPUT_PROMOTION_RESOURCE,
        access_paths=("local",),
    )
    provider = P1005OwnerCompanyGeneratedOutputPromotionProvider(root)
    if not provider.available(access):
        raise CompanyGeneratedOutputPromotionUnavailable(
            "provisioned promotion grant failed current revalidation"
        )
    return grant_id


__all__ = [
    "COMPANY_GENERATED_OUTPUT_PROMOTION_RESOURCE",
    "P1005OwnerCompanyGeneratedOutputPromotionProvider",
    "provision_company_generated_output_promotion_grant",
]

"""P10.04 productive owner-operated provider for staged Company Asset admission.

The provider composes the already-governed P10.03 admission path. It does not
make Workspace access, a browser button, AI output, or Product Contract
possession into authority. Before one admission command it independently:

* re-authenticates the current owner-operated P7.04 credential;
* requires an exact least-privilege grant for ``company.asset.admit-staged-version``;
* preserves current residual owner Organizational Authority from the canonical
  P10.01 matrix as a separate governed gate basis;
* binds data-governance and validation bases to the exact staged version,
  reviewed handling policy and review evidence;
* records the explicit owner admission command as a distinct Consequential
  Approval basis; and
* constructs an exact Product Contract-pinned RFC-0005 execution with all six
  required gates ALLOW before P10.03 may mutate canonical state.

The current reference runtime remains bounded/in-memory exactly as P10.03
closed it. This module selects no database, object store, durable ledger,
transaction manager, public API or new authority mechanism.
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
from p10_03_company_asset_ref.contract import (
    OP_ADMIT_STAGED_VERSION,
    P10_02_CANONICAL_CONTRACT_PATH,
    REQUIRED_ADMISSION_GATES,
    build_p10_03_product_contract_projection,
)

from .access import AccessContext, P704AccessResolver
from .company_asset_admission import ExactCompanyStagedMaterial
from .company_asset_library import (
    CompanyAssetAdmissionUnavailable,
    CompanyAssetGovernedAdmissionProvider,
    CompanyAssetReviewEvidence,
    CompanyAssetReviewPolicy,
    PreparedCompanyAssetAdmission,
)


COMPANY_ASSET_ADMISSION_RESOURCE = "company-assets"
P10_01_AUTHORITY_MATRIX_PATH = "docs/reviews/P10-01-asset-admission-real-work-authority-matrix.md"
CAP001_SUPPORT_EVIDENCE = "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"


def _identity_payload(value: Identity) -> dict[str, str]:
    return {"namespace": value.namespace, "value": value.value, "scope": value.scope}


def _aware(value: datetime, *, label: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise CompanyAssetAdmissionUnavailable(f"{label} must be timezone-aware")
    return value


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


class P1004OwnerCompanyAssetAdmissionProvider(CompanyAssetGovernedAdmissionProvider):
    """Compose one exact owner-command admission without manufacturing authority."""

    def __init__(self, runtime_root: Path) -> None:
        self.runtime_root = runtime_root.expanduser()

    def _require_owner_operated_actor(self, access: AccessContext) -> None:
        if not isinstance(access, AccessContext) or access.principal_kind != "human":
            raise CompanyAssetAdmissionUnavailable(
                "Company Asset admission requires an attributable human owner"
            )
        try:
            state = p704.load_access_store(self.runtime_root)
        except p704.P704Error as exc:
            raise CompanyAssetAdmissionUnavailable("current P7.04 access state is unavailable") from exc
        humans = tuple(
            record
            for record in state["principals"].values()
            if record["kind"] == "human" and record["status"] == "enabled"
        )
        if len(humans) != 1 or humans[0]["identity"] != _identity_payload(access.actor):
            raise CompanyAssetAdmissionUnavailable(
                "current residual-owner scope cannot be attributed to exactly one enabled human principal"
            )
        if state["organization"] != _identity_payload(access.organization):
            raise CompanyAssetAdmissionUnavailable("Company Asset admission Organization scope changed")

    def _authorize(self, access: AccessContext):
        self._require_owner_operated_actor(access)
        credential_file = self.runtime_root / "secrets" / "p7-04" / f"{access.credential_id}.secret"
        decision = p704.authorize_from_credential_file(
            self.runtime_root,
            organization=access.organization,
            principal=access.actor,
            credential_id=access.credential_id,
            credential_file=credential_file,
            operation=OP_ADMIT_STAGED_VERSION,
            resource=COMPANY_ASSET_ADMISSION_RESOURCE,
            access_path="local",
        )
        if (
            not decision.allowed
            or decision.principal_kind != "human"
            or not decision.grant_id
            or decision.organizational_authority_satisfied
            or decision.consequential_approval_satisfied
        ):
            raise CompanyAssetAdmissionUnavailable(
                "exact Company Asset admission authorization grant is absent or invalid"
            )
        return decision

    def available(self, access: AccessContext) -> bool:
        try:
            self._authorize(access)
        except (CompanyAssetAdmissionUnavailable, p704.P704Error, OSError):
            return False
        return True

    def actor_for(self, access: AccessContext) -> ActorContext:
        self._require_owner_operated_actor(access)
        scope = access.organization.value
        return ActorContext(
            Principal(access.actor),
            OrganizationScope(access.organization),
            authentication_evidence_refs=(
                Identity("credential-evidence", access.credential_id, scope),
            ),
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
        workflow_subject = Identity(
            "workflow-subject", f"p10-04-company-asset-admission-{intent}", scope
        )
        workflow_version = Identity(
            "workflow-version", f"p10-04-company-asset-admission-{intent}-v1", scope
        )
        authority_matrix = Identity(
            "governance-source", "p10-01-owner-asset-admission-matrix", scope
        )
        workflow_record = CanonicalRecord(
            subject_id=workflow_subject,
            version_id=workflow_version,
            semantic_type="platform.workflow",
            schema_version="p10.04-owner-command-1",
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
                ("representation", "p10.04-exact-owner-command-workflow"),
                ("authority_matrix", P10_01_AUTHORITY_MATRIX_PATH),
                ("product_contract", P10_02_CANONICAL_CONTRACT_PATH),
            ),
            payload=(("operation", OP_ADMIT_STAGED_VERSION), ("intent", intent)),
            lifecycle_status=WorkflowLifecycle.APPROVED.value,
            predecessor_version_id=None,
        )
        return WorkflowDefinition(
            record=workflow_record,
            operations=(
                WorkflowOperation(
                    semantic_name=OP_ADMIT_STAGED_VERSION,
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
        staged: ExactCompanyStagedMaterial,
        policy: CompanyAssetReviewPolicy,
        review: CompanyAssetReviewEvidence,
        intent: str,
        grant_id: str,
    ) -> dict[GovernedGateKind, Identity]:
        scope = access.organization.value
        handling = _digest(
            staged.classification,
            staged.purpose,
            staged.rights,
            staged.retention_rule,
            staged.semantic_role,
            policy.deletion_rule,
            *policy.permitted_reuse,
            review.policy_digest,
        )
        validation = _digest(
            staged.version_id,
            staged.content_sha256,
            review.updated_at,
            review.actor,
            review.policy_digest,
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
                "company-asset-handling-basis", f"{staged.version_id}-{handling}", scope
            ),
            GovernedGateKind.VALIDATION: Identity(
                "company-asset-validation-basis", f"{staged.version_id}-{validation}", scope
            ),
            GovernedGateKind.CONSEQUENTIAL_APPROVAL: Identity(
                "owner-command-approval", f"company-asset-admit-{intent}", scope
            ),
        }

    def prepare(
        self,
        *,
        access: AccessContext,
        candidate,
        staged: ExactCompanyStagedMaterial,
        policy: CompanyAssetReviewPolicy,
        review: CompanyAssetReviewEvidence,
    ) -> PreparedCompanyAssetAdmission:
        decision = self._authorize(access)
        actor = self.actor_for(access)
        record = candidate.canonical_record
        if record.organization != actor.organization:
            raise CompanyAssetAdmissionUnavailable(
                "candidate Organization changed before governed admission"
            )
        if record.creation_actor != actor:
            raise CompanyAssetAdmissionUnavailable(
                "candidate Actor changed before governed admission"
            )
        if dict(record.integrity_metadata).get("source_sha256") != staged.content_sha256:
            raise CompanyAssetAdmissionUnavailable(
                "candidate digest no longer matches exact staged source"
            )
        if review.actor != f"{access.actor.namespace}:{access.actor.value}@{access.actor.scope}":
            raise CompanyAssetAdmissionUnavailable("review evidence Actor changed before admission")

        command_at = _aware(record.created_at, label="owner admission command time").astimezone(
            timezone.utc
        )
        intent = _digest(
            access.actor.value,
            staged.material_id,
            staged.version_id,
            staged.content_sha256,
            review.updated_at,
            review.policy_digest,
            command_at.isoformat(),
            OP_ADMIT_STAGED_VERSION,
        )
        contract = build_p10_03_product_contract_projection(actor=actor, created_at=command_at)
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
        interaction = ProductRuntimeInteraction(
            organization=actor.organization,
            product_id=contract.product_id,
            product_version=contract.product_version,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            workflow=workflow,
            operation_name=OP_ADMIT_STAGED_VERSION,
            material_inputs=(record,),
            required_gates=REQUIRED_ADMISSION_GATES,
        )
        scope = actor.organization.organization_id.value
        created = adapters.facade.start_governed_execution(
            interaction=interaction,
            execution_id=Identity(
                "execution-subject", f"p10-04-asset-admission-{intent}", scope
            ),
            version_id=Identity(
                "execution-version", f"p10-04-asset-admission-{intent}-v1", scope
            ),
            created_at=command_at + timedelta(seconds=1),
            governed_versions=governed_versions,
        )
        awaiting = await_required_gates(
            created,
            version_id=Identity(
                "execution-version", f"p10-04-asset-admission-{intent}-v2", scope
            ),
            actor=actor,
            created_at=command_at + timedelta(seconds=2),
        )
        bases = self._basis_refs(
            access=access,
            staged=staged,
            policy=policy,
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
                    "gate-decision-subject",
                    f"p10-04-{intent}-{kind.value.lower()}",
                    scope,
                ),
                version_id=Identity(
                    "gate-decision-version",
                    f"p10-04-{intent}-{kind.value.lower()}-v1",
                    scope,
                ),
                created_at=command_at + timedelta(seconds=3 + index),
            )
            for index, kind in enumerate(awaiting.required_gates)
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=decisions,
            version_id=Identity(
                "execution-version", f"p10-04-asset-admission-{intent}-v3", scope
            ),
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
        return PreparedCompanyAssetAdmission(
            actor=actor,
            capability_adapter=adapters.capabilities,
            execution=ready,
            authority=authority,
            occurred_at=command_at + timedelta(seconds=11),
            recorded_at=command_at + timedelta(seconds=12),
        )


def provision_company_asset_admission_grant(runtime_root: Path) -> str:
    """Explicitly provision only the exact local staged-asset admission grant.

    The grant is Authorization evidence only. It deliberately supplies neither
    Organizational Authority nor Consequential Approval; both are re-evaluated
    for each exact owner admission command.
    """

    root = runtime_root.expanduser()
    access = P704AccessResolver(root).authorize()
    if access.principal_kind != "human":
        raise CompanyAssetAdmissionUnavailable(
            "only the current human owner may receive the admission grant"
        )
    grant_id = p704.grant_access(
        root,
        access.actor,
        operation=OP_ADMIT_STAGED_VERSION,
        resource=COMPANY_ASSET_ADMISSION_RESOURCE,
        access_paths=("local",),
    )
    provider = P1004OwnerCompanyAssetAdmissionProvider(root)
    if not provider.available(access):
        raise CompanyAssetAdmissionUnavailable(
            "provisioned admission grant failed current revalidation"
        )
    return grant_id


__all__ = [
    "COMPANY_ASSET_ADMISSION_RESOURCE",
    "P1004OwnerCompanyAssetAdmissionProvider",
    "provision_company_asset_admission_grant",
]

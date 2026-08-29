"""P10.05 — bounded governed promotion of one exact reviewed Transient Output.

This domain-neutral semantic owner composes existing Accepted-RFC mechanics.  It
promotes one exact reviewed transient Artifact into an immutable governed
Document Version plus an explicit Organizational Asset designation only inside
an admitted RFC-0005 Governed Execution with all six independent current gates.

The source transient representation is never relabelled or mutated into
canonical history.  The implementation is deliberately bounded/in-memory and
selects no database, object store, durable transaction/idempotency ledger,
public API/SDK, queue or service topology.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Final

from .canonical import AuthorityMode, CanonicalRecord
from .document_artifact_governance import AdmittedDocumentVersion, ArtifactState, DocumentVersionCandidate
from .event_provenance import CanonicalEvent, EventReceipt, admit_event
from .governed_execution import (
    GovernedExecutionContext,
    GovernedGateKind,
    GovernedGateOutcome,
    require_consequential_operation_admission,
)
from .identity import Identity
from .integration_adapters import IntegrationCapabilityAdapter
from .organizational_asset_admission import (
    AdmissionAuthorityError,
    AdmissionControlContinuityError,
    AdmissionDataGovernanceError,
    AssetAdmissionAuthorityEvidence,
    AssetAdmissionControlPins,
    ExactAdmissionSourceError,
    ORGANIZATIONAL_ASSET_DESIGNATION_AUTHORITY_SCOPE,
    ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE,
    OrganizationalAssetHandlingPolicy,
)
from .runtime_consistency import (
    ConsequentialAttempt,
    ConsequentialOutcome,
    IdempotencyKeyConflictError,
    ReconciliationRequiredError,
    RetrySemantics,
)
from .workflow import OperationSideEffectClass


GENERATED_OUTPUT_PROMOTION_EVENT_TYPE: Final = "platform.generated-output.promoted"
GENERATED_OUTPUT_PROMOTION_EVENT_AUTHORITY_SCOPE: Final = "platform.event/generated-output-promotion"
REQUIRED_GENERATED_OUTPUT_PROMOTION_GATES: Final = (
    GovernedGateKind.ACTOR_ASSURANCE,
    GovernedGateKind.AUTHORIZATION,
    GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
    GovernedGateKind.DATA_GOVERNANCE,
    GovernedGateKind.VALIDATION,
    GovernedGateKind.CONSEQUENTIAL_APPROVAL,
)


class ReviewedGeneratedOutputPromotionError(RuntimeError):
    """The reviewed-output promotion path cannot prove one required invariant."""


@dataclass(frozen=True, slots=True)
class ExactGeneratedOutputSource:
    """Exact non-canonical transient source plus retained generation lineage."""

    source_subject_id: Identity
    source_version_id: Identity
    artifact_id: Identity
    integrity_ref: str
    generation_provenance_refs: tuple[Identity, ...]

    def __post_init__(self) -> None:
        for label, value in (
            ("source_subject_id", self.source_subject_id),
            ("source_version_id", self.source_version_id),
            ("artifact_id", self.artifact_id),
        ):
            if not isinstance(value, Identity):
                raise ValueError(f"{label} must be an Identity")
        if self.source_subject_id == self.source_version_id:
            raise ValueError("transient source Subject and Version identities are distinct roles")
        if not isinstance(self.integrity_ref, str) or not self.integrity_ref.strip():
            raise ValueError("transient source integrity_ref must be explicit")
        if not isinstance(self.generation_provenance_refs, tuple) or not self.generation_provenance_refs:
            raise ValueError("generation provenance references must be explicit")
        if any(not isinstance(item, Identity) for item in self.generation_provenance_refs):
            raise ValueError("generation provenance references must contain Identity values")
        if len(set(self.generation_provenance_refs)) != len(self.generation_provenance_refs):
            raise ValueError("generation provenance references must not contain duplicates")


@dataclass(frozen=True, slots=True)
class ReviewedGeneratedOutputPromotionRequest:
    candidate: DocumentVersionCandidate
    source: ExactGeneratedOutputSource
    handling: OrganizationalAssetHandlingPolicy
    authority: AssetAdmissionAuthorityEvidence
    controls: AssetAdmissionControlPins
    designation_subject_id: Identity
    designation_version_id: Identity
    retry_token: str
    event_id: Identity
    event_version_id: Identity
    occurred_at: datetime
    recorded_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.candidate, DocumentVersionCandidate):
            raise ValueError("promotion candidate must be a DocumentVersionCandidate")
        if not isinstance(self.source, ExactGeneratedOutputSource):
            raise ValueError("promotion exact source must be explicit")
        if not isinstance(self.handling, OrganizationalAssetHandlingPolicy):
            raise ValueError("promotion handling policy must be explicit")
        if not isinstance(self.authority, AssetAdmissionAuthorityEvidence):
            raise ValueError("promotion authority evidence must be explicit")
        if not isinstance(self.controls, AssetAdmissionControlPins):
            raise ValueError("promotion control pins must be explicit")
        for label, value in (
            ("designation_subject_id", self.designation_subject_id),
            ("designation_version_id", self.designation_version_id),
            ("event_id", self.event_id),
            ("event_version_id", self.event_version_id),
        ):
            if not isinstance(value, Identity):
                raise ValueError(f"{label} must be an Identity")
        if self.designation_subject_id == self.designation_version_id:
            raise ValueError("designation Subject and Version identities are distinct roles")
        if not isinstance(self.retry_token, str) or not self.retry_token.strip():
            raise ValueError("promotion retry_token must be explicit")
        for label, value in (("occurred_at", self.occurred_at), ("recorded_at", self.recorded_at)):
            if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{label} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class CommittedReviewedGeneratedOutputPromotion:
    admitted_document: AdmittedDocumentVersion
    designation: CanonicalRecord
    event: CanonicalEvent
    source: ExactGeneratedOutputSource
    retry_token: str
    fingerprint: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReviewedGeneratedOutputPromotionState:
    """Bounded immutable logical state; not a durable persistence contract."""

    committed: tuple[CommittedReviewedGeneratedOutputPromotion, ...] = ()
    admitted_events: tuple[CanonicalEvent, ...] = ()
    attempts: tuple[ConsequentialAttempt, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.committed, tuple) or any(
            not isinstance(item, CommittedReviewedGeneratedOutputPromotion) for item in self.committed
        ):
            raise ValueError("committed promotions must be an immutable typed tuple")
        if not isinstance(self.admitted_events, tuple) or any(
            not isinstance(item, CanonicalEvent) for item in self.admitted_events
        ):
            raise ValueError("promotion Events must be an immutable CanonicalEvent tuple")
        if not isinstance(self.attempts, tuple) or any(
            not isinstance(item, ConsequentialAttempt) for item in self.attempts
        ):
            raise ValueError("promotion attempts must be an immutable ConsequentialAttempt tuple")


@dataclass(frozen=True, slots=True)
class ReviewedGeneratedOutputPromotionResult:
    state: ReviewedGeneratedOutputPromotionState
    promotion: CommittedReviewedGeneratedOutputPromotion
    duplicate: bool


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.scope}:{identity.value}"


def _fingerprint(
    *, execution: GovernedExecutionContext, request: ReviewedGeneratedOutputPromotionRequest
) -> tuple[str, ...]:
    return (
        _identity_text(execution.execution_subject_id),
        _identity_text(execution.execution_version_id),
        execution.operation_name,
        repr(request.candidate),
        repr(request.source),
        repr(request.handling),
        repr(request.authority),
        repr(request.controls),
        _identity_text(request.designation_subject_id),
        _identity_text(request.designation_version_id),
        _identity_text(request.event_id),
        _identity_text(request.event_version_id),
        request.occurred_at.isoformat(),
        request.recorded_at.isoformat(),
    )


def _validate_scope(
    execution: GovernedExecutionContext, request: ReviewedGeneratedOutputPromotionRequest
) -> None:
    organization = execution.organization
    scope = organization.organization_id.value
    candidate = request.candidate.canonical_record
    if candidate.organization != organization:
        raise ExactAdmissionSourceError("promotion candidate and execution must share Organization scope")
    identities = (
        request.source.source_subject_id,
        request.source.source_version_id,
        request.source.artifact_id,
        *request.source.generation_provenance_refs,
        request.authority.decision_authority_id,
        request.authority.organizational_authority_basis_ref,
        request.authority.consequential_approval_basis_ref,
        request.designation_subject_id,
        request.designation_version_id,
        request.event_id,
        request.event_version_id,
    )
    if any(item.scope != scope for item in identities):
        raise ExactAdmissionSourceError("promotion identities must share Organization scope")


def _validate_control_continuity(
    execution: GovernedExecutionContext, request: ReviewedGeneratedOutputPromotionRequest
) -> None:
    if execution.product_contract != request.controls.product_contract:
        raise AdmissionControlContinuityError("exact Product Contract Version continuity was lost")
    if execution.workflow != request.controls.workflow:
        raise AdmissionControlContinuityError("exact Workflow Version continuity was lost")
    if execution.operation_name != request.controls.operation_name:
        raise AdmissionControlContinuityError("exact promotion operation continuity was lost")
    candidate = request.candidate.canonical_record
    matches = tuple(
        pin
        for pin in execution.material_inputs
        if pin.subject_id == candidate.subject_id
        and pin.version_id == candidate.version_id
        and pin.semantic_type == candidate.semantic_type
        and pin.authority_scope == candidate.authority_scope
    )
    if len(matches) != 1:
        raise AdmissionControlContinuityError("execution must pin the exact promotion candidate exactly once")


def _validate_gates(
    execution: GovernedExecutionContext, request: ReviewedGeneratedOutputPromotionRequest
) -> None:
    expected = set(REQUIRED_GENERATED_OUTPUT_PROMOTION_GATES)
    if set(execution.required_gates) != expected:
        raise AdmissionAuthorityError("reviewed-output promotion requires all six independent current gates")
    if set(item.kind for item in execution.gate_decisions) != expected:
        raise AdmissionAuthorityError("reviewed-output promotion gate evidence is incomplete")
    if any(item.outcome is not GovernedGateOutcome.ALLOW for item in execution.gate_decisions):
        raise AdmissionAuthorityError("reviewed-output promotion requires every current gate to ALLOW")
    decisions = {item.kind: item for item in execution.gate_decisions}
    org = decisions[GovernedGateKind.ORGANIZATIONAL_AUTHORITY]
    approval = decisions[GovernedGateKind.CONSEQUENTIAL_APPROVAL]
    if org.basis_ref != request.authority.organizational_authority_basis_ref:
        raise AdmissionAuthorityError("Organizational Authority basis is stale or mismatched")
    if approval.basis_ref != request.authority.consequential_approval_basis_ref:
        raise AdmissionAuthorityError("Consequential Approval basis is stale or mismatched")
    if (
        org.record.accountable_owner_id != request.authority.decision_authority_id
        or approval.record.accountable_owner_id != request.authority.decision_authority_id
    ):
        raise AdmissionAuthorityError("promotion authority and approval must be attributable to decision authority")


def _validate_source_and_handling(request: ReviewedGeneratedOutputPromotionRequest) -> None:
    candidate = request.candidate.canonical_record
    source = request.source
    if candidate.authority_mode is not AuthorityMode.NATIVE or candidate.external_authority is not None:
        raise ExactAdmissionSourceError("first-slice reviewed-output promotion must create Native Company-held state")
    if source.source_subject_id not in candidate.provenance_refs or source.source_version_id not in candidate.provenance_refs:
        raise ExactAdmissionSourceError("candidate provenance must preserve exact transient Subject and Version")
    if not set(source.generation_provenance_refs).issubset(set(candidate.provenance_refs)):
        raise ExactAdmissionSourceError("candidate provenance lost retained generation/input lineage")
    matching = tuple(item for item in request.candidate.artifacts if item.artifact_id == source.artifact_id)
    if len(matching) != 1:
        raise ExactAdmissionSourceError("exact transient Artifact identity is not uniquely present")
    artifact = matching[0]
    if artifact.state is not ArtifactState.TRANSIENT:
        raise ExactAdmissionSourceError("promotion source Artifact must remain transient before admission")
    if artifact.integrity_ref != source.integrity_ref:
        raise ExactAdmissionSourceError("promotion candidate digest differs from exact transient output digest")
    expected = request.handling.cap001_constraints
    if any(item.handling != expected for item in request.candidate.artifacts):
        raise AdmissionDataGovernanceError("candidate handling differs from reviewed Data Governance semantics")


def _build_designation(
    execution: GovernedExecutionContext, request: ReviewedGeneratedOutputPromotionRequest
) -> CanonicalRecord:
    candidate = request.candidate.canonical_record
    gates = tuple(item.record.version_id for item in execution.gate_decisions)
    provenance = tuple(
        dict.fromkeys(
            (
                execution.record.creation_actor.actual_principal.principal_id,
                execution.execution_subject_id,
                execution.execution_version_id,
                candidate.subject_id,
                candidate.version_id,
                request.source.source_subject_id,
                request.source.source_version_id,
                *request.source.generation_provenance_refs,
                request.authority.decision_authority_id,
                request.authority.organizational_authority_basis_ref,
                request.authority.consequential_approval_basis_ref,
                *gates,
                request.controls.product_contract.subject_id,
                request.controls.product_contract.version_id,
                request.controls.workflow.subject_id,
                request.controls.workflow.version_id,
            )
        )
    )
    return CanonicalRecord(
        subject_id=request.designation_subject_id,
        version_id=request.designation_version_id,
        semantic_type=ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE,
        schema_version="p10.05-reviewed-output-1",
        organization=execution.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=ORGANIZATIONAL_ASSET_DESIGNATION_AUTHORITY_SCOPE,
        accountable_owner_id=candidate.accountable_owner_id,
        creation_actor=execution.record.creation_actor,
        created_at=request.recorded_at,
        provenance_refs=provenance,
        integrity_metadata=(
            ("representation", "immutable-reviewed-generated-output-designation"),
            ("source_integrity_ref", request.source.integrity_ref),
        ),
        payload=(
            ("document_subject", _identity_text(candidate.subject_id)),
            ("document_version", _identity_text(candidate.version_id)),
            ("source_kind", "TransientOutput"),
            ("source_subject", _identity_text(request.source.source_subject_id)),
            ("source_version", _identity_text(request.source.source_version_id)),
            ("classification", request.handling.classification),
            ("purpose", request.handling.purpose),
            ("rights", " | ".join(request.handling.rights)),
            ("retention_rule", request.handling.retention_rule),
            ("deletion_rule", request.handling.deletion_rule),
            ("permitted_reuse", " | ".join(request.handling.permitted_reuse)),
        ),
        lifecycle_status="Admitted",
        predecessor_version_id=None,
    )


def _build_event(
    execution: GovernedExecutionContext,
    request: ReviewedGeneratedOutputPromotionRequest,
    designation: CanonicalRecord,
) -> EventReceipt:
    candidate = request.candidate.canonical_record
    actor = execution.record.creation_actor.actual_principal.principal_id
    gate_versions = tuple(item.record.version_id for item in execution.gate_decisions)
    provenance = tuple(
        dict.fromkeys(
            (
                actor,
                execution.execution_subject_id,
                execution.execution_version_id,
                candidate.subject_id,
                candidate.version_id,
                designation.subject_id,
                designation.version_id,
                request.source.source_subject_id,
                request.source.source_version_id,
                *request.source.generation_provenance_refs,
                request.controls.product_contract.subject_id,
                request.controls.product_contract.version_id,
                request.controls.workflow.subject_id,
                request.controls.workflow.version_id,
                *gate_versions,
            )
        )
    )
    return EventReceipt(
        event_id=request.event_id,
        version_id=request.event_version_id,
        event_type=GENERATED_OUTPUT_PROMOTION_EVENT_TYPE,
        event_schema_version="1",
        organization=execution.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=GENERATED_OUTPUT_PROMOTION_EVENT_AUTHORITY_SCOPE,
        authoritative_source="Arvectum OS Governed Execution",
        occurred_at=request.occurred_at,
        recorded_at=request.recorded_at,
        producer_id=actor,
        initiating_actor_id=actor,
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        related_subject_ids=(candidate.subject_id, designation.subject_id),
        related_version_ids=(candidate.version_id, designation.version_id),
        correlation_refs=(execution.execution_subject_id, request.source.source_subject_id),
        causation_refs=(execution.execution_version_id, request.source.source_version_id),
        classification=request.handling.classification,
        access_scope=candidate.authority_scope,
        provenance_refs=provenance,
        integrity_metadata=(
            ("representation", "reviewed-generated-output-promotion-event"),
            ("source_integrity_ref", request.source.integrity_ref),
        ),
        payload=(
            ("operation", execution.operation_name),
            ("source_kind", "TransientOutput"),
            ("retry_token", request.retry_token),
        ),
    )


def _duplicate_or_block(
    state: ReviewedGeneratedOutputPromotionState,
    *,
    retry_token: str,
    fingerprint: tuple[str, ...],
) -> CommittedReviewedGeneratedOutputPromotion | None:
    same = tuple(item for item in state.attempts if item.retry_token == retry_token)
    if any(item.fingerprint != fingerprint for item in same):
        raise IdempotencyKeyConflictError("promotion retry token was bound to different immutable content")
    if any(item.outcome is ConsequentialOutcome.UNCERTAIN for item in same):
        raise ReconciliationRequiredError("promotion has uncertain prior outcome; reconcile before retry")
    succeeded = tuple(item for item in same if item.outcome is ConsequentialOutcome.SUCCEEDED)
    if not succeeded:
        return None
    matches = tuple(
        item for item in state.committed if item.retry_token == retry_token and item.fingerprint == fingerprint
    )
    if len(matches) != 1:
        raise ReviewedGeneratedOutputPromotionError("successful retry evidence does not resolve one promotion")
    attempt = succeeded[-1]
    if attempt.result_version_id != matches[0].designation.version_id:
        raise ReviewedGeneratedOutputPromotionError("promotion designation differs from retry evidence")
    if attempt.event_version_id != matches[0].event.version_id:
        raise ReviewedGeneratedOutputPromotionError("promotion Event differs from retry evidence")
    return matches[0]


def promote_reviewed_generated_output(
    *,
    state: ReviewedGeneratedOutputPromotionState,
    capability_adapter: IntegrationCapabilityAdapter,
    execution: GovernedExecutionContext,
    request: ReviewedGeneratedOutputPromotionRequest,
) -> ReviewedGeneratedOutputPromotionResult:
    """Promote one exact reviewed Transient Output through the admitted operation."""

    if not isinstance(state, ReviewedGeneratedOutputPromotionState):
        raise TypeError("promotion state must be ReviewedGeneratedOutputPromotionState")
    if not isinstance(capability_adapter, IntegrationCapabilityAdapter):
        raise TypeError("promotion requires the typed CAP-001 integration adapter")
    if not isinstance(execution, GovernedExecutionContext):
        raise TypeError("promotion requires GovernedExecutionContext")
    if not isinstance(request, ReviewedGeneratedOutputPromotionRequest):
        raise TypeError("promotion request must be explicit")

    require_consequential_operation_admission(
        execution, side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION
    )
    _validate_scope(execution, request)
    _validate_control_continuity(execution, request)
    _validate_gates(execution, request)
    _validate_source_and_handling(request)
    if request.candidate.canonical_record.creation_actor != execution.record.creation_actor:
        raise AdmissionAuthorityError("promotion candidate actor must match current governed Actor")

    fingerprint = _fingerprint(execution=execution, request=request)
    duplicate = _duplicate_or_block(
        state, retry_token=request.retry_token, fingerprint=fingerprint
    )
    if duplicate is not None:
        return ReviewedGeneratedOutputPromotionResult(state=state, promotion=duplicate, duplicate=True)

    admitted = capability_adapter.admit_document_version(
        execution=execution, candidate=request.candidate
    )
    designation = _build_designation(execution, request)
    receipt = _build_event(execution, request, designation)
    event_result = admit_event(
        receipt=receipt,
        execution=execution,
        related_records=(admitted.canonical_record, designation),
        admitted_events=state.admitted_events,
    )
    committed = CommittedReviewedGeneratedOutputPromotion(
        admitted_document=admitted,
        designation=designation,
        event=event_result.event,
        source=request.source,
        retry_token=request.retry_token,
        fingerprint=fingerprint,
    )
    attempt = ConsequentialAttempt(
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        operation_name=execution.operation_name,
        side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
        retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
        retry_token=request.retry_token,
        fingerprint=fingerprint,
        outcome=ConsequentialOutcome.SUCCEEDED,
        result_version_id=designation.version_id,
        event_version_id=event_result.event.version_id,
    )
    new_state = ReviewedGeneratedOutputPromotionState(
        committed=state.committed + (committed,),
        admitted_events=event_result.admitted_events,
        attempts=state.attempts + (attempt,),
    )
    return ReviewedGeneratedOutputPromotionResult(
        state=new_state, promotion=committed, duplicate=False
    )


__all__ = [
    "CommittedReviewedGeneratedOutputPromotion",
    "ExactGeneratedOutputSource",
    "GENERATED_OUTPUT_PROMOTION_EVENT_TYPE",
    "REQUIRED_GENERATED_OUTPUT_PROMOTION_GATES",
    "ReviewedGeneratedOutputPromotionError",
    "ReviewedGeneratedOutputPromotionRequest",
    "ReviewedGeneratedOutputPromotionResult",
    "ReviewedGeneratedOutputPromotionState",
    "promote_reviewed_generated_output",
]

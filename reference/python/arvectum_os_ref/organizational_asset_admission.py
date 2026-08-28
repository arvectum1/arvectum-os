"""P10.03 — domain-neutral Organizational Asset admission execution path.

This module composes existing Accepted-RFC semantic owners rather than creating a
new persistence or workflow mechanism.  An exact Document Version candidate may
be designated as an Organizational Asset only when:

* the exact source identity/version/integrity is preserved;
* the exact Product Contract, Workflow, operation and candidate version remain
  pinned by one admitted RFC-0005 Governed Execution;
* Actor Assurance, Authorization, Organizational Authority, Data Governance,
  Validation and Consequential Approval remain separate current ALLOW decisions;
* the supplied decision-authority basis remains exact for Organizational
  Authority and Consequential Approval;
* handling, rights, retention/deletion and permitted-reuse semantics are
  explicit and consistent with the CAP-001 Artifact manifest;
* Native versus External Reference authority is preserved without creating a
  competing source of truth;
* retry/idempotency evidence is explicit and an uncertain prior attempt blocks
  blind retry;
* the admitted Document Version, separate Organizational Asset designation and
  canonical admission Event are returned as one immutable logical result.

The implementation is deliberately in-memory/reference semantics.  It does not
select a database, object store, durable idempotency ledger, transaction manager,
serialization contract, public API/SDK, queue or service topology.  Any such
materially constraining mechanism remains behind the applicable ADR gate.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Final

from .canonical import AuthorityMode, CanonicalRecord
from .document_artifact_governance import (
    AdmittedDocumentVersion,
    DocumentVersionCandidate,
    HandlingConstraints,
)
from .event_provenance import CanonicalEvent, EventReceipt, admit_event
from .execution import GovernedVersionPin
from .governed_execution import (
    GovernedExecutionContext,
    GovernedGateKind,
    GovernedGateOutcome,
    require_consequential_operation_admission,
)
from .identity import Identity
from .integration_adapters import IntegrationCapabilityAdapter
from .runtime_consistency import (
    ConsequentialAttempt,
    ConsequentialOutcome,
    IdempotencyKeyConflictError,
    ReconciliationRequiredError,
    RetrySemantics,
)
from .workflow import OperationSideEffectClass


ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE: Final = (
    "platform.organizational-asset-designation"
)
ORGANIZATIONAL_ASSET_DESIGNATION_AUTHORITY_SCOPE: Final = (
    "platform.document/organizational-asset-designation"
)
ORGANIZATIONAL_ASSET_ADMISSION_EVENT_TYPE: Final = (
    "platform.organizational-asset.admitted"
)
ORGANIZATIONAL_ASSET_ADMISSION_EVENT_AUTHORITY_SCOPE: Final = (
    "platform.event/organizational-asset-admission"
)

REQUIRED_ORGANIZATIONAL_ASSET_ADMISSION_GATES: Final = (
    GovernedGateKind.ACTOR_ASSURANCE,
    GovernedGateKind.AUTHORIZATION,
    GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
    GovernedGateKind.DATA_GOVERNANCE,
    GovernedGateKind.VALIDATION,
    GovernedGateKind.CONSEQUENTIAL_APPROVAL,
)


class OrganizationalAssetAdmissionError(RuntimeError):
    """The bounded admission path cannot prove one required invariant."""


class ExactAdmissionSourceError(OrganizationalAssetAdmissionError):
    """The exact source/version/integrity relationship is unresolved or stale."""


class AdmissionAuthorityError(PermissionError, OrganizationalAssetAdmissionError):
    """Current authority/approval evidence is absent, stale or attributed incorrectly."""


class AdmissionDataGovernanceError(OrganizationalAssetAdmissionError):
    """Required handling/rights/retention/deletion/reuse semantics are unresolved."""


class AdmissionControlContinuityError(OrganizationalAssetAdmissionError):
    """Product Contract / Workflow / operation control continuity was lost."""


class AssetAdmissionSourceKind(str, Enum):
    STAGED_VERSION = "StagedVersion"
    EXTERNAL_REFERENCE = "ExternalReference"


@dataclass(frozen=True, slots=True)
class ExternalAuthorityAdmissionState:
    """Resolved current state of an External Reference for this exact admission.

    The booleans/labels record the caller's governed resolution; they do not grant
    authority by themselves.  The exact Data Governance and Validation gate
    decisions remain the authority-bearing admission evidence.
    """

    authoritative_system: str
    external_object_ref: str
    source_version_semantics: str
    freshness_state: str
    conflict_state: str
    availability_state: str
    resolution_basis_ref: Identity
    admission_allowed: bool

    def __post_init__(self) -> None:
        for label, value in (
            ("authoritative_system", self.authoritative_system),
            ("external_object_ref", self.external_object_ref),
            ("source_version_semantics", self.source_version_semantics),
            ("freshness_state", self.freshness_state),
            ("conflict_state", self.conflict_state),
            ("availability_state", self.availability_state),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"external authority {label} must be explicit")
        if not isinstance(self.resolution_basis_ref, Identity):
            raise ValueError("external authority resolution_basis_ref must be an Identity")
        if not isinstance(self.admission_allowed, bool):
            raise ValueError("external authority admission_allowed must be explicit")


@dataclass(frozen=True, slots=True)
class ExactAssetAdmissionSource:
    """Exact non-authoritative source evidence used to build one candidate version."""

    kind: AssetAdmissionSourceKind
    source_subject_id: Identity
    source_version_id: Identity
    artifact_id: Identity
    integrity_ref: str
    authority_mode: AuthorityMode
    external_state: ExternalAuthorityAdmissionState | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, AssetAdmissionSourceKind):
            raise ValueError("admission source kind must be explicit")
        for label, value in (
            ("source_subject_id", self.source_subject_id),
            ("source_version_id", self.source_version_id),
            ("artifact_id", self.artifact_id),
        ):
            if not isinstance(value, Identity):
                raise ValueError(f"{label} must be an Identity")
        if self.source_subject_id == self.source_version_id:
            raise ValueError("source Subject and Version identities are distinct roles")
        if not isinstance(self.integrity_ref, str) or not self.integrity_ref.strip():
            raise ValueError("source integrity_ref must be explicit")
        if not isinstance(self.authority_mode, AuthorityMode):
            raise ValueError("source authority_mode must be explicit")
        if self.kind is AssetAdmissionSourceKind.STAGED_VERSION:
            if self.authority_mode is not AuthorityMode.NATIVE:
                raise ValueError("bounded staged-version admission is Native organizational authority")
            if self.external_state is not None:
                raise ValueError("Native staged-version source must not carry external authority state")
        elif self.kind is AssetAdmissionSourceKind.EXTERNAL_REFERENCE:
            if self.authority_mode is not AuthorityMode.EXTERNAL_REFERENCE:
                raise ValueError("external-reference source must preserve External Reference authority")
            if not isinstance(self.external_state, ExternalAuthorityAdmissionState):
                raise ValueError("External Reference admission requires resolved external authority state")


@dataclass(frozen=True, slots=True)
class OrganizationalAssetHandlingPolicy:
    """Explicit admission-time handling semantics not inferred from visibility."""

    classification: str
    purpose: str
    rights: tuple[str, ...]
    retention_rule: str
    deletion_rule: str
    permitted_reuse: tuple[str, ...]

    def __post_init__(self) -> None:
        for label, value in (
            ("classification", self.classification),
            ("purpose", self.purpose),
            ("retention_rule", self.retention_rule),
            ("deletion_rule", self.deletion_rule),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"asset handling {label} must be explicit")
        for label, values in (("rights", self.rights), ("permitted_reuse", self.permitted_reuse)):
            if not isinstance(values, tuple) or not values or any(
                not isinstance(value, str) or not value.strip() for value in values
            ):
                raise ValueError(f"asset handling {label} must contain explicit values")

    @property
    def cap001_constraints(self) -> HandlingConstraints:
        return HandlingConstraints(
            classification=self.classification,
            purpose=self.purpose,
            rights=self.rights,
            retention_rule=self.retention_rule,
        )


@dataclass(frozen=True, slots=True)
class AssetAdmissionAuthorityEvidence:
    """Exact current decision-authority attribution for the two authority gates."""

    decision_authority_id: Identity
    organizational_authority_basis_ref: Identity
    consequential_approval_basis_ref: Identity

    def __post_init__(self) -> None:
        for label, value in (
            ("decision_authority_id", self.decision_authority_id),
            ("organizational_authority_basis_ref", self.organizational_authority_basis_ref),
            ("consequential_approval_basis_ref", self.consequential_approval_basis_ref),
        ):
            if not isinstance(value, Identity):
                raise ValueError(f"{label} must be an Identity")


@dataclass(frozen=True, slots=True)
class AssetAdmissionControlPins:
    """Exact Product Contract / Workflow / operation controls for one admission."""

    product_contract: GovernedVersionPin
    workflow: GovernedVersionPin
    operation_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.product_contract, GovernedVersionPin):
            raise ValueError("asset admission requires an exact Product Contract version pin")
        if not isinstance(self.workflow, GovernedVersionPin):
            raise ValueError("asset admission requires an exact Workflow version pin")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ValueError("asset admission operation_name must be explicit")


@dataclass(frozen=True, slots=True)
class OrganizationalAssetAdmissionRequest:
    """All immutable inputs required to attempt one admission invocation."""

    candidate: DocumentVersionCandidate
    source: ExactAssetAdmissionSource
    handling: OrganizationalAssetHandlingPolicy
    authority: AssetAdmissionAuthorityEvidence
    controls: AssetAdmissionControlPins
    designation_subject_id: Identity
    designation_version_id: Identity
    designation_predecessor_version_id: Identity | None
    retry_token: str
    event_id: Identity
    event_version_id: Identity
    occurred_at: datetime
    recorded_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.candidate, DocumentVersionCandidate):
            raise ValueError("asset admission candidate must be a DocumentVersionCandidate")
        if not isinstance(self.source, ExactAssetAdmissionSource):
            raise ValueError("asset admission exact source must be explicit")
        if not isinstance(self.handling, OrganizationalAssetHandlingPolicy):
            raise ValueError("asset admission handling policy must be explicit")
        if not isinstance(self.authority, AssetAdmissionAuthorityEvidence):
            raise ValueError("asset admission authority evidence must be explicit")
        if not isinstance(self.controls, AssetAdmissionControlPins):
            raise ValueError("asset admission control pins must be explicit")
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
        if self.designation_predecessor_version_id is not None and not isinstance(
            self.designation_predecessor_version_id, Identity
        ):
            raise ValueError("designation predecessor must be an Identity when supplied")
        if not isinstance(self.retry_token, str) or not self.retry_token.strip():
            raise ValueError("asset admission retry_token must be explicit")
        for label, value in (("occurred_at", self.occurred_at), ("recorded_at", self.recorded_at)):
            if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{label} must be timezone-aware")


@dataclass(frozen=True, slots=True)
class CommittedOrganizationalAssetAdmission:
    admitted_document: AdmittedDocumentVersion
    designation: CanonicalRecord
    event: CanonicalEvent
    retry_token: str
    fingerprint: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OrganizationalAssetAdmissionState:
    """Bounded immutable logical state; not a durable store/transaction contract."""

    committed: tuple[CommittedOrganizationalAssetAdmission, ...] = ()
    admitted_events: tuple[CanonicalEvent, ...] = ()
    attempts: tuple[ConsequentialAttempt, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.committed, tuple) or any(
            not isinstance(item, CommittedOrganizationalAssetAdmission) for item in self.committed
        ):
            raise ValueError("committed admissions must be an immutable typed tuple")
        if not isinstance(self.admitted_events, tuple) or any(
            not isinstance(item, CanonicalEvent) for item in self.admitted_events
        ):
            raise ValueError("admitted_events must be an immutable CanonicalEvent tuple")
        if not isinstance(self.attempts, tuple) or any(
            not isinstance(item, ConsequentialAttempt) for item in self.attempts
        ):
            raise ValueError("attempts must be an immutable ConsequentialAttempt tuple")


@dataclass(frozen=True, slots=True)
class OrganizationalAssetAdmissionResult:
    state: OrganizationalAssetAdmissionState
    admission: CommittedOrganizationalAssetAdmission
    duplicate: bool


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.scope}:{identity.value}"


def _request_fingerprint(
    *, execution: GovernedExecutionContext, request: OrganizationalAssetAdmissionRequest
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
        repr(request.designation_predecessor_version_id),
        _identity_text(request.event_id),
        _identity_text(request.event_version_id),
        request.occurred_at.isoformat(),
        request.recorded_at.isoformat(),
    )


def _validate_scope(execution: GovernedExecutionContext, request: OrganizationalAssetAdmissionRequest) -> None:
    organization = execution.organization
    scope = organization.organization_id.value
    candidate = request.candidate.canonical_record
    if candidate.organization != organization:
        raise ExactAdmissionSourceError("candidate and execution must share Organization scope")
    identities = (
        request.source.source_subject_id,
        request.source.source_version_id,
        request.source.artifact_id,
        request.authority.decision_authority_id,
        request.authority.organizational_authority_basis_ref,
        request.authority.consequential_approval_basis_ref,
        request.designation_subject_id,
        request.designation_version_id,
        request.event_id,
        request.event_version_id,
        *((request.designation_predecessor_version_id,) if request.designation_predecessor_version_id else ()),
    )
    if any(identity.scope != scope for identity in identities):
        raise ExactAdmissionSourceError("asset admission identities must share Organization scope")
    if request.source.external_state is not None and request.source.external_state.resolution_basis_ref.scope != scope:
        raise ExactAdmissionSourceError("external authority resolution basis must share Organization scope")


def _validate_control_continuity(
    *, execution: GovernedExecutionContext, request: OrganizationalAssetAdmissionRequest
) -> None:
    controls = request.controls
    if execution.product_contract != controls.product_contract:
        raise AdmissionControlContinuityError("exact Product Contract Version continuity was lost")
    if execution.workflow != controls.workflow:
        raise AdmissionControlContinuityError("exact Workflow Version continuity was lost")
    if execution.operation_name != controls.operation_name:
        raise AdmissionControlContinuityError("exact admission operation continuity was lost")
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
        raise AdmissionControlContinuityError(
            "execution must pin the exact candidate Document Version exactly once"
        )


def _validate_required_gates(
    *, execution: GovernedExecutionContext, request: OrganizationalAssetAdmissionRequest
) -> None:
    expected = set(REQUIRED_ORGANIZATIONAL_ASSET_ADMISSION_GATES)
    if set(execution.required_gates) != expected:
        raise AdmissionAuthorityError(
            "organizational-asset admission requires all six independent current governance gates"
        )
    if set(decision.kind for decision in execution.gate_decisions) != expected:
        raise AdmissionAuthorityError("organizational-asset admission gate evidence is incomplete")
    if any(decision.outcome is not GovernedGateOutcome.ALLOW for decision in execution.gate_decisions):
        raise AdmissionAuthorityError("organizational-asset admission requires every current gate to ALLOW")

    decisions = {decision.kind: decision for decision in execution.gate_decisions}
    org_decision = decisions[GovernedGateKind.ORGANIZATIONAL_AUTHORITY]
    approval_decision = decisions[GovernedGateKind.CONSEQUENTIAL_APPROVAL]
    authority = request.authority
    if org_decision.basis_ref != authority.organizational_authority_basis_ref:
        raise AdmissionAuthorityError("Organizational Authority basis reference is stale or mismatched")
    if approval_decision.basis_ref != authority.consequential_approval_basis_ref:
        raise AdmissionAuthorityError("Consequential Approval basis reference is stale or mismatched")
    if (
        org_decision.record.accountable_owner_id != authority.decision_authority_id
        or approval_decision.record.accountable_owner_id != authority.decision_authority_id
    ):
        raise AdmissionAuthorityError(
            "Organizational Authority and Consequential Approval must be attributable to the declared decision authority"
        )


def _validate_source_and_handling(request: OrganizationalAssetAdmissionRequest) -> None:
    candidate = request.candidate.canonical_record
    source = request.source
    if candidate.authority_mode is not source.authority_mode:
        raise ExactAdmissionSourceError("candidate authority mode differs from exact admission source")
    if source.source_subject_id not in candidate.provenance_refs or source.source_version_id not in candidate.provenance_refs:
        raise ExactAdmissionSourceError(
            "candidate provenance must preserve exact source Subject and Version identities"
        )
    matching_artifacts = tuple(
        artifact for artifact in request.candidate.artifacts if artifact.artifact_id == source.artifact_id
    )
    if len(matching_artifacts) != 1:
        raise ExactAdmissionSourceError("exact source Artifact identity is not uniquely present in candidate")
    artifact = matching_artifacts[0]
    if artifact.integrity_ref != source.integrity_ref:
        raise ExactAdmissionSourceError("candidate Artifact integrity differs from exact source digest")

    expected_handling = request.handling.cap001_constraints
    if any(item.handling != expected_handling for item in request.candidate.artifacts):
        raise AdmissionDataGovernanceError(
            "candidate Artifact handling differs from explicit admission-time Data Governance semantics"
        )

    if source.kind is AssetAdmissionSourceKind.STAGED_VERSION:
        if candidate.authority_mode is not AuthorityMode.NATIVE or candidate.external_authority is not None:
            raise ExactAdmissionSourceError("staged Native admission cannot carry external authority semantics")
        return

    external = candidate.external_authority
    state = source.external_state
    if candidate.authority_mode is not AuthorityMode.EXTERNAL_REFERENCE or external is None or state is None:
        raise ExactAdmissionSourceError("External Reference admission requires complete authority mapping")
    if (
        external.authoritative_system != state.authoritative_system
        or external.external_object_ref != state.external_object_ref
        or external.source_version_semantics != state.source_version_semantics
    ):
        raise ExactAdmissionSourceError("current external authority state does not match candidate authority contract")
    if not state.admission_allowed:
        raise ExactAdmissionSourceError(
            "current external freshness/conflict/availability resolution does not admit canonical reference admission"
        )


def _build_designation(
    *, execution: GovernedExecutionContext, request: OrganizationalAssetAdmissionRequest
) -> CanonicalRecord:
    candidate = request.candidate.canonical_record
    source = request.source
    authority = request.authority
    gate_versions = tuple(decision.record.version_id for decision in execution.gate_decisions)
    provenance = tuple(
        dict.fromkeys(
            (
                execution.record.creation_actor.actual_principal.principal_id,
                execution.execution_subject_id,
                execution.execution_version_id,
                candidate.subject_id,
                candidate.version_id,
                source.source_subject_id,
                source.source_version_id,
                authority.decision_authority_id,
                authority.organizational_authority_basis_ref,
                authority.consequential_approval_basis_ref,
                *gate_versions,
                request.controls.product_contract.subject_id,
                request.controls.product_contract.version_id,
                request.controls.workflow.subject_id,
                request.controls.workflow.version_id,
            )
        )
    )
    payload = (
        ("document_subject", _identity_text(candidate.subject_id)),
        ("document_version", _identity_text(candidate.version_id)),
        ("source_kind", source.kind.value),
        ("source_subject", _identity_text(source.source_subject_id)),
        ("source_version", _identity_text(source.source_version_id)),
        ("classification", request.handling.classification),
        ("purpose", request.handling.purpose),
        ("rights", " | ".join(request.handling.rights)),
        ("retention_rule", request.handling.retention_rule),
        ("deletion_rule", request.handling.deletion_rule),
        ("permitted_reuse", " | ".join(request.handling.permitted_reuse)),
    )
    return CanonicalRecord(
        subject_id=request.designation_subject_id,
        version_id=request.designation_version_id,
        semantic_type=ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE,
        schema_version="1",
        organization=execution.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=ORGANIZATIONAL_ASSET_DESIGNATION_AUTHORITY_SCOPE,
        accountable_owner_id=candidate.accountable_owner_id,
        creation_actor=execution.record.creation_actor,
        created_at=request.recorded_at,
        provenance_refs=provenance,
        integrity_metadata=(
            ("representation", "immutable-organizational-asset-designation"),
            ("source_integrity_ref", source.integrity_ref),
        ),
        payload=payload,
        lifecycle_status="Admitted",
        predecessor_version_id=request.designation_predecessor_version_id,
    )


def _build_event_receipt(
    *,
    execution: GovernedExecutionContext,
    request: OrganizationalAssetAdmissionRequest,
    designation: CanonicalRecord,
) -> EventReceipt:
    candidate = request.candidate.canonical_record
    actor_id = execution.record.creation_actor.actual_principal.principal_id
    gate_versions = tuple(decision.record.version_id for decision in execution.gate_decisions)
    provenance = tuple(
        dict.fromkeys(
            (
                actor_id,
                execution.execution_subject_id,
                execution.execution_version_id,
                candidate.subject_id,
                candidate.version_id,
                designation.subject_id,
                designation.version_id,
                request.source.source_subject_id,
                request.source.source_version_id,
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
        event_type=ORGANIZATIONAL_ASSET_ADMISSION_EVENT_TYPE,
        event_schema_version="1",
        organization=execution.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=ORGANIZATIONAL_ASSET_ADMISSION_EVENT_AUTHORITY_SCOPE,
        authoritative_source="Arvectum OS Governed Execution",
        occurred_at=request.occurred_at,
        recorded_at=request.recorded_at,
        producer_id=actor_id,
        initiating_actor_id=actor_id,
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
            ("representation", "organizational-asset-admission-event"),
            ("source_integrity_ref", request.source.integrity_ref),
        ),
        payload=(
            ("operation", execution.operation_name),
            ("source_kind", request.source.kind.value),
            ("retry_token", request.retry_token),
        ),
    )


def _duplicate_or_block(
    *,
    state: OrganizationalAssetAdmissionState,
    retry_token: str,
    fingerprint: tuple[str, ...],
) -> CommittedOrganizationalAssetAdmission | None:
    same_token = tuple(item for item in state.attempts if item.retry_token == retry_token)
    if any(item.fingerprint != fingerprint for item in same_token):
        raise IdempotencyKeyConflictError(
            "organizational-asset admission retry token was bound to different immutable invocation content"
        )
    if any(item.outcome is ConsequentialOutcome.UNCERTAIN for item in same_token):
        raise ReconciliationRequiredError(
            "organizational-asset admission has uncertain prior outcome; reconcile before retry"
        )
    succeeded = tuple(item for item in same_token if item.outcome is ConsequentialOutcome.SUCCEEDED)
    if not succeeded:
        return None
    attempt = succeeded[-1]
    matches = tuple(
        item
        for item in state.committed
        if item.retry_token == retry_token and item.fingerprint == fingerprint
    )
    if len(matches) != 1:
        raise OrganizationalAssetAdmissionError(
            "successful idempotency evidence does not resolve one committed admission"
        )
    if attempt.result_version_id != matches[0].designation.version_id:
        raise OrganizationalAssetAdmissionError("committed designation version differs from retry evidence")
    if attempt.event_version_id != matches[0].event.version_id:
        raise OrganizationalAssetAdmissionError("committed Event version differs from retry evidence")
    return matches[0]


def admit_organizational_asset(
    *,
    state: OrganizationalAssetAdmissionState,
    capability_adapter: IntegrationCapabilityAdapter,
    execution: GovernedExecutionContext,
    request: OrganizationalAssetAdmissionRequest,
) -> OrganizationalAssetAdmissionResult:
    """Admit one exact Document Version + separate Organizational Asset designation.

    The function is pure over the supplied bounded state except for delegation to
    the already-pure CAP-001 reference adapter.  It therefore demonstrates one
    logical all-or-nothing admission result, not durable atomicity.
    """

    if not isinstance(state, OrganizationalAssetAdmissionState):
        raise TypeError("asset admission state must be OrganizationalAssetAdmissionState")
    if not isinstance(capability_adapter, IntegrationCapabilityAdapter):
        raise TypeError("asset admission requires the typed CAP-001 integration adapter")
    if not isinstance(execution, GovernedExecutionContext):
        raise TypeError("asset admission requires GovernedExecutionContext")
    if not isinstance(request, OrganizationalAssetAdmissionRequest):
        raise TypeError("asset admission request must be explicit")

    require_consequential_operation_admission(
        execution,
        side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
    )
    _validate_scope(execution, request)
    _validate_control_continuity(execution=execution, request=request)
    _validate_required_gates(execution=execution, request=request)
    _validate_source_and_handling(request)

    if request.candidate.canonical_record.creation_actor != execution.record.creation_actor:
        raise AdmissionAuthorityError(
            "candidate admission actor must be the current attributable Governed Execution actor"
        )

    fingerprint = _request_fingerprint(execution=execution, request=request)
    duplicate = _duplicate_or_block(
        state=state,
        retry_token=request.retry_token,
        fingerprint=fingerprint,
    )
    if duplicate is not None:
        return OrganizationalAssetAdmissionResult(state=state, admission=duplicate, duplicate=True)

    admitted_document = capability_adapter.admit_document_version(
        execution=execution,
        candidate=request.candidate,
    )
    designation = _build_designation(execution=execution, request=request)
    event_receipt = _build_event_receipt(
        execution=execution,
        request=request,
        designation=designation,
    )
    event_result = admit_event(
        receipt=event_receipt,
        execution=execution,
        related_records=(admitted_document.canonical_record, designation),
        admitted_events=state.admitted_events,
    )
    committed = CommittedOrganizationalAssetAdmission(
        admitted_document=admitted_document,
        designation=designation,
        event=event_result.event,
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
    new_state = OrganizationalAssetAdmissionState(
        committed=state.committed + (committed,),
        admitted_events=event_result.admitted_events,
        attempts=state.attempts + (attempt,),
    )
    return OrganizationalAssetAdmissionResult(
        state=new_state,
        admission=committed,
        duplicate=False,
    )


def record_organizational_asset_admission_uncertainty(
    *,
    state: OrganizationalAssetAdmissionState,
    execution: GovernedExecutionContext,
    request: OrganizationalAssetAdmissionRequest,
) -> OrganizationalAssetAdmissionState:
    """Record unresolved outcome evidence so a later blind retry fails closed.

    This is bounded semantic evidence only.  It does not manufacture a durable
    recovery/reconciliation system and never claims a canonical admission/Event.
    """

    if not isinstance(state, OrganizationalAssetAdmissionState):
        raise TypeError("asset admission state must be OrganizationalAssetAdmissionState")
    if not isinstance(execution, GovernedExecutionContext):
        raise TypeError("asset admission uncertainty requires GovernedExecutionContext")
    if not isinstance(request, OrganizationalAssetAdmissionRequest):
        raise TypeError("asset admission request must be explicit")
    fingerprint = _request_fingerprint(execution=execution, request=request)
    existing = tuple(item for item in state.attempts if item.retry_token == request.retry_token)
    if any(item.fingerprint != fingerprint for item in existing):
        raise IdempotencyKeyConflictError(
            "asset admission retry token was already bound to different immutable invocation content"
        )
    if any(item.outcome is ConsequentialOutcome.SUCCEEDED for item in existing):
        raise OrganizationalAssetAdmissionError(
            "cannot mark a committed organizational-asset admission as uncertain"
        )
    if any(item.outcome is ConsequentialOutcome.UNCERTAIN for item in existing):
        return state
    attempt = ConsequentialAttempt(
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        operation_name=execution.operation_name,
        side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
        retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
        retry_token=request.retry_token,
        fingerprint=fingerprint,
        outcome=ConsequentialOutcome.UNCERTAIN,
    )
    return OrganizationalAssetAdmissionState(
        committed=state.committed,
        admitted_events=state.admitted_events,
        attempts=state.attempts + (attempt,),
    )


__all__ = [
    "AdmissionAuthorityError",
    "AdmissionControlContinuityError",
    "AdmissionDataGovernanceError",
    "AssetAdmissionAuthorityEvidence",
    "AssetAdmissionControlPins",
    "AssetAdmissionSourceKind",
    "CommittedOrganizationalAssetAdmission",
    "ExactAdmissionSourceError",
    "ExactAssetAdmissionSource",
    "ExternalAuthorityAdmissionState",
    "ORGANIZATIONAL_ASSET_ADMISSION_EVENT_TYPE",
    "ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE",
    "OrganizationalAssetAdmissionError",
    "OrganizationalAssetAdmissionRequest",
    "OrganizationalAssetAdmissionResult",
    "OrganizationalAssetAdmissionState",
    "OrganizationalAssetHandlingPolicy",
    "REQUIRED_ORGANIZATIONAL_ASSET_ADMISSION_GATES",
    "admit_organizational_asset",
    "record_organizational_asset_admission_uncertainty",
]

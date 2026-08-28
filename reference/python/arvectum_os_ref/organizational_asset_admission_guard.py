"""P10.03 governed entry guard for Organizational Asset admission.

The lower-level admission semantic owner already requires the six independent
RFC-0005 gates and preserves every exact gate-decision Version in designation
and Event provenance.  This guard binds External Reference freshness/conflict/
availability resolution to the current immutable Validation gate basis before
delegating to that owner.

This avoids inventing a second freshness authority or duplicating opaque basis
identifiers into product payload.  The resulting provenance chain is:

admission designation/Event -> exact Validation gate decision Version -> exact
resolution ``basis_ref`` recorded in that immutable gate-decision provenance.
"""

from __future__ import annotations

from .governed_execution import GovernedExecutionContext, GovernedGateKind
from .integration_adapters import IntegrationCapabilityAdapter
from .organizational_asset_admission import (
    AssetAdmissionSourceKind,
    ExactAdmissionSourceError,
    OrganizationalAssetAdmissionRequest,
    OrganizationalAssetAdmissionResult,
    OrganizationalAssetAdmissionState,
    admit_organizational_asset,
)


def _require_external_resolution_gate_binding(
    *, execution: GovernedExecutionContext, request: OrganizationalAssetAdmissionRequest
) -> None:
    if request.source.kind is not AssetAdmissionSourceKind.EXTERNAL_REFERENCE:
        return
    external_state = request.source.external_state
    if external_state is None:
        raise ExactAdmissionSourceError(
            "External Reference admission requires explicit current external resolution state"
        )
    validation = tuple(
        decision
        for decision in execution.gate_decisions
        if decision.kind is GovernedGateKind.VALIDATION
    )
    if len(validation) != 1:
        raise ExactAdmissionSourceError(
            "External Reference admission requires exactly one current Validation gate decision"
        )
    decision = validation[0]
    if decision.basis_ref != external_state.resolution_basis_ref:
        raise ExactAdmissionSourceError(
            "External Reference freshness/conflict/availability resolution basis must equal the exact current Validation gate basis"
        )
    if external_state.resolution_basis_ref not in decision.record.provenance_refs:
        raise ExactAdmissionSourceError(
            "Validation gate decision must preserve the external resolution basis in immutable provenance"
        )


def admit_governed_organizational_asset(
    *,
    state: OrganizationalAssetAdmissionState,
    capability_adapter: IntegrationCapabilityAdapter,
    execution: GovernedExecutionContext,
    request: OrganizationalAssetAdmissionRequest,
) -> OrganizationalAssetAdmissionResult:
    """Canonical P10.03 admission entrypoint with external-resolution continuity."""

    if not isinstance(execution, GovernedExecutionContext):
        raise TypeError("governed asset admission requires GovernedExecutionContext")
    if not isinstance(request, OrganizationalAssetAdmissionRequest):
        raise TypeError("governed asset admission request must be explicit")
    _require_external_resolution_gate_binding(execution=execution, request=request)
    return admit_organizational_asset(
        state=state,
        capability_adapter=capability_adapter,
        execution=execution,
        request=request,
    )


__all__ = ["admit_governed_organizational_asset"]

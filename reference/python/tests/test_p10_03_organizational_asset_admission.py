from __future__ import annotations

import base64
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    ArtifactState,
    DocumentVersionCandidate,
    HandlingConstraints,
)
from arvectum_os_ref.governed_execution import (
    GovernedGateKind,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import compose_integration_adapters
from arvectum_os_ref.organizational_asset_admission import (
    AdmissionAuthorityError,
    AssetAdmissionAuthorityEvidence,
    AssetAdmissionControlPins,
    AssetAdmissionSourceKind,
    ExactAdmissionSourceError,
    ExactAssetAdmissionSource,
    ExternalAuthorityAdmissionState,
    ORGANIZATIONAL_ASSET_ADMISSION_EVENT_TYPE,
    ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE,
    OrganizationalAssetAdmissionRequest,
    OrganizationalAssetAdmissionState,
    OrganizationalAssetHandlingPolicy,
    admit_organizational_asset,
    record_organizational_asset_admission_uncertainty,
)
from arvectum_os_ref.product_capability_consumption import (
    CAPABILITY_CONTRACT_VERSION,
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_003_SEARCH_PROJECTION,
    CAP_004_AUDIT_RECONSTRUCTION,
)
from arvectum_os_ref.product_contract import (
    ProductContractSecurityBoundaryError,
    ProductRuntimeInteraction,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.runtime_consistency import (
    IdempotencyKeyConflictError,
    ReconciliationRequiredError,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowOperation,
)
from p10_03_company_asset_ref.contract import (
    EXTERNAL_ASSET_DOCUMENT_SCOPE,
    NATIVE_ASSET_DOCUMENT_SCOPE,
    OP_ADMIT_EXTERNAL_REFERENCE,
    OP_ADMIT_STAGED_VERSION,
    P10_02_CANONICAL_BLOB_SHA,
    P10_02_CONTRACT_VERSION_VALUE,
    REQUIRED_ADMISSION_GATES,
    build_p10_03_product_contract_projection,
)
from workspace_app.access import AccessContext
from workspace_app.company_asset_admission import (
    build_staged_document_candidate,
    exact_staged_source_identities,
    resolve_exact_staged_material,
)
from workspace_app.company_materials import CompanyMaterialsStore


UTC = timezone.utc


class P1003OrganizationalAssetAdmissionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = "p10-03-org-a"
        self.organization_id = Identity("organization", self.scope, "platform")
        self.organization = OrganizationScope(self.organization_id)
        self.owner_id = Identity("principal", "p10-03-owner", self.scope)
        self.actor = ActorContext(Principal(self.owner_id), self.organization)
        self.access = AccessContext(
            organization=self.organization_id,
            actor=self.owner_id,
            principal_kind="human",
            credential_id="cred-p10-03-owner",
            grant_id="grant-p10-03-workspace",
        )
        self.base_time = datetime(2026, 8, 28, 9, 0, tzinfo=UTC)
        self.contract = build_p10_03_product_contract_projection(
            actor=self.actor,
            created_at=self.base_time,
        )
        self.governed_versions = (
            GovernedDependencyVersionEvidence(
                CAP_001_DOCUMENT_ARTIFACT,
                CAPABILITY_CONTRACT_VERSION,
                DependencySupportDisposition.SUPPORTED,
                "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0",
            ),
        )
        self.adapters = compose_integration_adapters(
            contract=self.contract,
            actor=self.actor,
            effective_product_contract=self.contract.version_pin,
            governed_versions=self.governed_versions,
        )

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.scope)

    def _workflow_and_interaction(
        self,
        *,
        candidate: DocumentVersionCandidate,
        operation_name: str,
        required_gates: tuple[GovernedGateKind, ...] = REQUIRED_ADMISSION_GATES,
    ) -> ProductRuntimeInteraction:
        record = candidate.canonical_record
        workflow_record = CanonicalRecord(
            subject_id=self._id("workflow-subject", f"{operation_name}-workflow"),
            version_id=self._id("workflow-version", f"{operation_name}-workflow-v1"),
            semantic_type="platform.workflow",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.workflow/definition",
            accountable_owner_id=self.owner_id,
            creation_actor=self.actor,
            created_at=self.base_time + timedelta(minutes=1),
            provenance_refs=(self.owner_id, record.subject_id, record.version_id),
            integrity_metadata=(("representation", "p10.03-test-workflow"),),
            lifecycle_status="Approved",
        )
        workflow = WorkflowDefinition(
            record=workflow_record,
            operations=(
                WorkflowOperation(
                    semantic_name=operation_name,
                    target_subject_id=record.subject_id,
                    target_semantic_type=record.semantic_type,
                    side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
                ),
            ),
        )
        return ProductRuntimeInteraction(
            organization=self.organization,
            product_id=self.contract.product_id,
            product_version=self.contract.product_version,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            workflow=workflow,
            operation_name=operation_name,
            material_inputs=(record,),
            required_gates=required_gates,
        )

    def _ready_execution(self, interaction: ProductRuntimeInteraction, *, suffix: str):
        created = self.adapters.facade.start_governed_execution(
            interaction=interaction,
            execution_id=self._id("execution-subject", f"p10-03-{suffix}"),
            version_id=self._id("execution-version", f"p10-03-{suffix}-v1"),
            created_at=self.base_time + timedelta(minutes=2),
            governed_versions=self.governed_versions,
        )
        awaiting = await_required_gates(
            created,
            version_id=self._id("execution-version", f"p10-03-{suffix}-v2"),
            actor=self.actor,
            created_at=self.base_time + timedelta(minutes=3),
        )
        decisions = []
        for index, kind in enumerate(awaiting.required_gates, start=1):
            decisions.append(
                build_governed_gate_decision(
                    execution=awaiting,
                    kind=kind,
                    outcome=GovernedGateOutcome.ALLOW,
                    decision_actor=self.actor,
                    basis_ref=self._id("governed-basis", f"{suffix}-{kind.value.lower()}-basis"),
                    decision_id=self._id("gate-decision-subject", f"{suffix}-{index}"),
                    version_id=self._id("gate-decision-version", f"{suffix}-{index}-v1"),
                    created_at=self.base_time + timedelta(minutes=3 + index),
                )
            )
        return admit_ready_execution(
            awaiting,
            decisions=tuple(decisions),
            version_id=self._id("execution-version", f"p10-03-{suffix}-v3"),
            actor=self.actor,
            created_at=self.base_time + timedelta(minutes=12),
        )

    def _authority(self, execution) -> AssetAdmissionAuthorityEvidence:
        by_kind = {decision.kind: decision for decision in execution.gate_decisions}
        return AssetAdmissionAuthorityEvidence(
            decision_authority_id=self.owner_id,
            organizational_authority_basis_ref=by_kind[
                GovernedGateKind.ORGANIZATIONAL_AUTHORITY
            ].basis_ref,
            consequential_approval_basis_ref=by_kind[
                GovernedGateKind.CONSEQUENTIAL_APPROVAL
            ].basis_ref,
        )

    def _request(
        self,
        *,
        candidate: DocumentVersionCandidate,
        source: ExactAssetAdmissionSource,
        execution,
        suffix: str,
        handling: OrganizationalAssetHandlingPolicy,
    ) -> OrganizationalAssetAdmissionRequest:
        return OrganizationalAssetAdmissionRequest(
            candidate=candidate,
            source=source,
            handling=handling,
            authority=self._authority(execution),
            controls=AssetAdmissionControlPins(
                product_contract=execution.product_contract,
                workflow=execution.workflow,
                operation_name=execution.operation_name,
            ),
            designation_subject_id=self._id("organizational-asset-subject", f"asset-{suffix}"),
            designation_version_id=self._id("organizational-asset-version", f"asset-{suffix}-v1"),
            designation_predecessor_version_id=None,
            retry_token=f"asset-admission-{suffix}",
            event_id=self._id("event-subject", f"asset-admitted-{suffix}"),
            event_version_id=self._id("event-version", f"asset-admitted-{suffix}-v1"),
            occurred_at=self.base_time + timedelta(minutes=13),
            recorded_at=self.base_time + timedelta(minutes=14),
        )

    def _stage_native_fixture(self, runtime_root: Path):
        store = CompanyMaterialsStore(runtime_root)
        staged_result = store.stage(
            self.access,
            {
                "project_id": "COMPANY",
                "filename": "standard.txt",
                "media_type": "text/plain",
                "semantic_role": "company-standard-source",
                "classification": "internal",
                "purpose": "governed-company-operational-use",
                "rights": "company-internal-use",
                "retention_rule": "retain-while-current-plus-governed-history",
                "content_base64": base64.b64encode(b"Arvectum Company standard v1\n").decode("ascii"),
            },
        )
        version = staged_result["material"]
        exact = resolve_exact_staged_material(
            store=store,
            access=self.access,
            material_id=version["material_id"],
            version_id=version["version_id"],
        )
        candidate = build_staged_document_candidate(
            staged=exact,
            access=self.access,
            actor=self.actor,
            candidate_created_at=self.base_time + timedelta(minutes=1),
        )
        source_subject, source_version, artifact_id = exact_staged_source_identities(
            staged=exact,
            actor=self.actor,
        )
        source = ExactAssetAdmissionSource(
            kind=AssetAdmissionSourceKind.STAGED_VERSION,
            source_subject_id=source_subject,
            source_version_id=source_version,
            artifact_id=artifact_id,
            integrity_ref=exact.content_sha256,
            authority_mode=AuthorityMode.NATIVE,
        )
        handling = OrganizationalAssetHandlingPolicy(
            classification=exact.classification,
            purpose=exact.purpose,
            rights=(exact.rights,),
            retention_rule=exact.retention_rule,
            deletion_rule="owner-governed deletion only; immutable admission evidence retained as required",
            permitted_reuse=("approved-company-operational-document-use",),
        )
        return store, exact, candidate, source, handling

    def test_contract_projection_is_exact_p10_02_cap001_only_boundary(self) -> None:
        self.assertEqual(self.contract.canonical_source_blob_sha, P10_02_CANONICAL_BLOB_SHA)
        self.assertEqual(self.contract.version_pin.version_id.value, P10_02_CONTRACT_VERSION_VALUE)
        self.assertNotEqual(self.contract.record.subject_id, self.contract.version_pin.subject_id)
        self.assertNotEqual(self.contract.record.version_id, self.contract.version_pin.version_id)
        dependencies = {item.dependency_id for item in self.contract.dependencies}
        self.assertEqual(dependencies, {CAP_001_DOCUMENT_ARTIFACT})
        self.assertNotIn(CAP_002_MEMORY_KNOWLEDGE, dependencies)
        self.assertNotIn(CAP_003_SEARCH_PROJECTION, dependencies)
        self.assertNotIn(CAP_004_AUDIT_RECONSTRUCTION, dependencies)
        self.assertEqual(
            {item.operation_name for item in self.contract.operations},
            {OP_ADMIT_STAGED_VERSION, OP_ADMIT_EXTERNAL_REFERENCE},
        )
        for operation in self.contract.operations:
            self.assertEqual(operation.required_gates, REQUIRED_ADMISSION_GATES)

    def test_shared_module_contains_no_company_taxonomy_or_operation_names(self) -> None:
        shared = (
            Path(__file__).resolve().parents[1]
            / "arvectum_os_ref"
            / "organizational_asset_admission.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("company.asset.", shared)
        self.assertNotIn("project_id", shared)
        self.assertNotIn("semantic_role", shared)

    def test_exact_staged_version_enters_canonical_history_only_through_ready_execution(self) -> None:
        with TemporaryDirectory() as temp:
            store, exact, candidate, source, handling = self._stage_native_fixture(Path(temp))
            interaction = self._workflow_and_interaction(
                candidate=candidate,
                operation_name=OP_ADMIT_STAGED_VERSION,
            )
            execution = self._ready_execution(interaction, suffix="native")
            request = self._request(
                candidate=candidate,
                source=source,
                execution=execution,
                suffix="native",
                handling=handling,
            )
            result = admit_organizational_asset(
                state=OrganizationalAssetAdmissionState(),
                capability_adapter=self.adapters.capabilities,
                execution=execution,
                request=request,
            )

            self.assertFalse(result.duplicate)
            self.assertIs(
                result.admission.admitted_document.artifacts[0].state,
                ArtifactState.GOVERNED,
            )
            self.assertEqual(
                result.admission.admitted_document.canonical_record.version_id,
                candidate.canonical_record.version_id,
            )
            self.assertEqual(
                result.admission.designation.semantic_type,
                ORGANIZATIONAL_ASSET_DESIGNATION_SEMANTIC_TYPE,
            )
            self.assertEqual(
                result.admission.event.event_type,
                ORGANIZATIONAL_ASSET_ADMISSION_EVENT_TYPE,
            )
            self.assertEqual(len(result.state.committed), 1)
            self.assertEqual(len(result.state.admitted_events), 1)
            self.assertEqual(len(result.state.attempts), 1)

            # Admission never relabels or mutates the product-local staging source.
            projection = store.project(self.access)
            matching = [
                version
                for material in projection["materials"]
                if material["material_id"] == exact.material_id
                for version in material["versions"]
                if version["version_id"] == exact.version_id
            ]
            self.assertEqual(len(matching), 1)
            self.assertEqual(matching[0]["state"], "StagedNonCanonical")
            self.assertFalse(matching[0]["canonical_authority"])

            duplicate = admit_organizational_asset(
                state=result.state,
                capability_adapter=self.adapters.capabilities,
                execution=execution,
                request=request,
            )
            self.assertTrue(duplicate.duplicate)
            self.assertIs(duplicate.state, result.state)
            self.assertEqual(len(duplicate.state.committed), 1)
            self.assertEqual(len(duplicate.state.admitted_events), 1)

    def test_stale_or_mismatched_digest_fails_closed_before_admission(self) -> None:
        with TemporaryDirectory() as temp:
            _store, _exact, candidate, source, handling = self._stage_native_fixture(Path(temp))
            interaction = self._workflow_and_interaction(
                candidate=candidate,
                operation_name=OP_ADMIT_STAGED_VERSION,
            )
            execution = self._ready_execution(interaction, suffix="digest")
            wrong_source = replace(source, integrity_ref="0" * 64)
            request = self._request(
                candidate=candidate,
                source=wrong_source,
                execution=execution,
                suffix="digest",
                handling=handling,
            )
            with self.assertRaises(ExactAdmissionSourceError):
                admit_organizational_asset(
                    state=OrganizationalAssetAdmissionState(),
                    capability_adapter=self.adapters.capabilities,
                    execution=execution,
                    request=request,
                )

    def test_authority_basis_continuity_is_independent_and_fail_closed(self) -> None:
        with TemporaryDirectory() as temp:
            _store, _exact, candidate, source, handling = self._stage_native_fixture(Path(temp))
            execution = self._ready_execution(
                self._workflow_and_interaction(
                    candidate=candidate,
                    operation_name=OP_ADMIT_STAGED_VERSION,
                ),
                suffix="authority",
            )
            request = self._request(
                candidate=candidate,
                source=source,
                execution=execution,
                suffix="authority",
                handling=handling,
            )
            request = replace(
                request,
                authority=replace(
                    request.authority,
                    organizational_authority_basis_ref=self._id("governed-basis", "stale-owner-basis"),
                ),
            )
            with self.assertRaises(AdmissionAuthorityError):
                admit_organizational_asset(
                    state=OrganizationalAssetAdmissionState(),
                    capability_adapter=self.adapters.capabilities,
                    execution=execution,
                    request=request,
                )

    def test_product_contract_refuses_runtime_that_omits_any_declared_gate(self) -> None:
        with TemporaryDirectory() as temp:
            _store, _exact, candidate, _source, _handling = self._stage_native_fixture(Path(temp))
            missing_validation = tuple(
                gate for gate in REQUIRED_ADMISSION_GATES if gate is not GovernedGateKind.VALIDATION
            )
            interaction = self._workflow_and_interaction(
                candidate=candidate,
                operation_name=OP_ADMIT_STAGED_VERSION,
                required_gates=missing_validation,
            )
            with self.assertRaises(ProductContractSecurityBoundaryError):
                self.adapters.facade.start_governed_execution(
                    interaction=interaction,
                    execution_id=self._id("execution-subject", "missing-gate"),
                    version_id=self._id("execution-version", "missing-gate-v1"),
                    created_at=self.base_time + timedelta(minutes=2),
                    governed_versions=self.governed_versions,
                )

    def test_uncertain_prior_attempt_blocks_blind_retry(self) -> None:
        with TemporaryDirectory() as temp:
            _store, _exact, candidate, source, handling = self._stage_native_fixture(Path(temp))
            execution = self._ready_execution(
                self._workflow_and_interaction(
                    candidate=candidate,
                    operation_name=OP_ADMIT_STAGED_VERSION,
                ),
                suffix="uncertain",
            )
            request = self._request(
                candidate=candidate,
                source=source,
                execution=execution,
                suffix="uncertain",
                handling=handling,
            )
            state = record_organizational_asset_admission_uncertainty(
                state=OrganizationalAssetAdmissionState(),
                execution=execution,
                request=request,
            )
            with self.assertRaises(ReconciliationRequiredError):
                admit_organizational_asset(
                    state=state,
                    capability_adapter=self.adapters.capabilities,
                    execution=execution,
                    request=request,
                )

    def test_retry_token_cannot_be_rebound_to_different_immutable_request(self) -> None:
        with TemporaryDirectory() as temp:
            _store, _exact, candidate, source, handling = self._stage_native_fixture(Path(temp))
            execution = self._ready_execution(
                self._workflow_and_interaction(
                    candidate=candidate,
                    operation_name=OP_ADMIT_STAGED_VERSION,
                ),
                suffix="rebind",
            )
            request = self._request(
                candidate=candidate,
                source=source,
                execution=execution,
                suffix="rebind",
                handling=handling,
            )
            first = admit_organizational_asset(
                state=OrganizationalAssetAdmissionState(),
                capability_adapter=self.adapters.capabilities,
                execution=execution,
                request=request,
            )
            changed = replace(
                request,
                handling=replace(request.handling, deletion_rule="different governed deletion rule"),
            )
            with self.assertRaises(IdempotencyKeyConflictError):
                admit_organizational_asset(
                    state=first.state,
                    capability_adapter=self.adapters.capabilities,
                    execution=execution,
                    request=changed,
                )

    def test_external_reference_admission_preserves_external_authority(self) -> None:
        source_subject = self._id("external-object-subject", "company-source-record")
        source_version = self._id("external-object-version", "company-source-record-v7")
        artifact_id = self._id("artifact", "external-company-source-v7")
        handling = OrganizationalAssetHandlingPolicy(
            classification="internal",
            purpose="governed-reference-use",
            rights=("reference-only",),
            retention_rule="retain-governed-reference-while-relied-upon",
            deletion_rule="delete-local-reference-material per governed source policy",
            permitted_reuse=("approved-reference-resolution",),
        )
        external_contract = ExternalAuthorityContract(
            authoritative_system="external-company-record-system",
            external_object_ref="record:12345",
            authority_scope=EXTERNAL_ASSET_DOCUMENT_SCOPE,
            retrieval_or_sync="read-only exact reference resolution",
            freshness_expectation="resolved current for this admission attempt",
            source_version_semantics="external immutable revision 7",
            conflict_rule="external system wins; conflict blocks admission",
            failure_behavior="unavailable or unresolved freshness blocks admission",
            permitted_transformations=("integrity hashing",),
            retention_deletion="local governed reference follows declared Company policy",
            portability="export external identity/version/provenance without claiming source authority",
        )
        record = CanonicalRecord(
            subject_id=self._id("document", "external-reference-asset"),
            version_id=self._id("document-version", "external-reference-asset-v7"),
            semantic_type="platform.document",
            schema_version="p10.03-external-reference-1",
            organization=self.organization,
            authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
            authority_scope=EXTERNAL_ASSET_DOCUMENT_SCOPE,
            accountable_owner_id=self.owner_id,
            creation_actor=self.actor,
            created_at=self.base_time + timedelta(minutes=1),
            provenance_refs=(self.owner_id, source_subject, source_version),
            integrity_metadata=(("source_integrity", "external-revision-7-digest"),),
            lifecycle_status="AdmissionCandidate",
            external_authority=external_contract,
        )
        artifact = ArtifactContent(
            artifact_id=artifact_id,
            organization=self.organization,
            content_ref="external-reference:record:12345@7",
            media_type="application/octet-stream",
            integrity_ref="external-revision-7-digest",
            rendition_role="external-reference",
            handling=handling.cap001_constraints,
        )
        candidate = DocumentVersionCandidate(record, (artifact,), "external-reference")
        execution = self._ready_execution(
            self._workflow_and_interaction(
                candidate=candidate,
                operation_name=OP_ADMIT_EXTERNAL_REFERENCE,
            ),
            suffix="external",
        )
        source = ExactAssetAdmissionSource(
            kind=AssetAdmissionSourceKind.EXTERNAL_REFERENCE,
            source_subject_id=source_subject,
            source_version_id=source_version,
            artifact_id=artifact_id,
            integrity_ref="external-revision-7-digest",
            authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
            external_state=ExternalAuthorityAdmissionState(
                authoritative_system="external-company-record-system",
                external_object_ref="record:12345",
                source_version_semantics="external immutable revision 7",
                freshness_state="fresh-resolved",
                conflict_state="no-conflict",
                availability_state="available",
                resolution_basis_ref=self._id("external-resolution-basis", "record-12345-v7"),
                admission_allowed=True,
            ),
        )
        request = self._request(
            candidate=candidate,
            source=source,
            execution=execution,
            suffix="external",
            handling=handling,
        )
        result = admit_organizational_asset(
            state=OrganizationalAssetAdmissionState(),
            capability_adapter=self.adapters.capabilities,
            execution=execution,
            request=request,
        )
        admitted = result.admission.admitted_document.canonical_record
        self.assertIs(admitted.authority_mode, AuthorityMode.EXTERNAL_REFERENCE)
        self.assertEqual(admitted.external_authority, external_contract)
        self.assertEqual(admitted.external_authority.authoritative_system, "external-company-record-system")
        self.assertIs(result.admission.designation.authority_mode, AuthorityMode.NATIVE)

        blocked_request = replace(
            request,
            source=replace(
                source,
                external_state=replace(source.external_state, admission_allowed=False),
            ),
            retry_token="asset-admission-external-blocked",
            designation_version_id=self._id("organizational-asset-version", "external-blocked-v1"),
            event_id=self._id("event-subject", "external-blocked"),
            event_version_id=self._id("event-version", "external-blocked-v1"),
        )
        with self.assertRaises(ExactAdmissionSourceError):
            admit_organizational_asset(
                state=OrganizationalAssetAdmissionState(),
                capability_adapter=self.adapters.capabilities,
                execution=execution,
                request=blocked_request,
            )


if __name__ == "__main__":
    unittest.main()

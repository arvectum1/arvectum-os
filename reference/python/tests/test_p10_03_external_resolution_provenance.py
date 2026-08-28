from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timedelta, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.document_artifact_governance import ArtifactContent, DocumentVersionCandidate
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.organizational_asset_admission import (
    AssetAdmissionSourceKind,
    ExactAdmissionSourceError,
    ExactAssetAdmissionSource,
    ExternalAuthorityAdmissionState,
    OrganizationalAssetAdmissionState,
    OrganizationalAssetHandlingPolicy,
)
from arvectum_os_ref.organizational_asset_admission_guard import (
    admit_governed_organizational_asset,
)
from p10_03_company_asset_ref.contract import (
    EXTERNAL_ASSET_DOCUMENT_SCOPE,
    OP_ADMIT_EXTERNAL_REFERENCE,
)
from test_p10_03_organizational_asset_admission import (
    P1003OrganizationalAssetAdmissionTests,
)


UTC = timezone.utc


class P1003ExternalResolutionProvenanceTests(unittest.TestCase):
    def setUp(self) -> None:
        helper = P1003OrganizationalAssetAdmissionTests(
            methodName="test_contract_projection_is_exact_p10_02_cap001_only_boundary"
        )
        helper.setUp()
        self.h = helper

    def _external_fixture(self):
        source_subject = self.h._id("external-object-subject", "guarded-company-source")
        source_version = self.h._id("external-object-version", "guarded-company-source-v9")
        artifact_id = self.h._id("artifact", "guarded-external-company-source-v9")
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
            external_object_ref="record:guarded-9",
            authority_scope=EXTERNAL_ASSET_DOCUMENT_SCOPE,
            retrieval_or_sync="read-only exact reference resolution",
            freshness_expectation="resolved current for this admission attempt",
            source_version_semantics="external immutable revision 9",
            conflict_rule="external system wins; conflict blocks admission",
            failure_behavior="unavailable or unresolved freshness blocks admission",
            permitted_transformations=("integrity hashing",),
            retention_deletion="local governed reference follows declared Company policy",
            portability="export external identity/version/provenance without claiming source authority",
        )
        record = CanonicalRecord(
            subject_id=self.h._id("document", "guarded-external-reference-asset"),
            version_id=self.h._id("document-version", "guarded-external-reference-asset-v9"),
            semantic_type="platform.document",
            schema_version="p10.03-external-reference-1",
            organization=self.h.organization,
            authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
            authority_scope=EXTERNAL_ASSET_DOCUMENT_SCOPE,
            accountable_owner_id=self.h.owner_id,
            creation_actor=self.h.actor,
            created_at=self.h.base_time + timedelta(minutes=1),
            provenance_refs=(self.h.owner_id, source_subject, source_version),
            integrity_metadata=(("source_integrity", "external-revision-9-digest"),),
            lifecycle_status="AdmissionCandidate",
            external_authority=external_contract,
        )
        artifact = ArtifactContent(
            artifact_id=artifact_id,
            organization=self.h.organization,
            content_ref="external-reference:record:guarded-9@9",
            media_type="application/octet-stream",
            integrity_ref="external-revision-9-digest",
            rendition_role="external-reference",
            handling=handling.cap001_constraints,
        )
        candidate = DocumentVersionCandidate(record, (artifact,), "external-reference")
        execution = self.h._ready_execution(
            self.h._workflow_and_interaction(
                candidate=candidate,
                operation_name=OP_ADMIT_EXTERNAL_REFERENCE,
            ),
            suffix="external-provenance",
        )
        validation = next(
            decision
            for decision in execution.gate_decisions
            if decision.kind is GovernedGateKind.VALIDATION
        )
        source = ExactAssetAdmissionSource(
            kind=AssetAdmissionSourceKind.EXTERNAL_REFERENCE,
            source_subject_id=source_subject,
            source_version_id=source_version,
            artifact_id=artifact_id,
            integrity_ref="external-revision-9-digest",
            authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
            external_state=ExternalAuthorityAdmissionState(
                authoritative_system="external-company-record-system",
                external_object_ref="record:guarded-9",
                source_version_semantics="external immutable revision 9",
                freshness_state="fresh-resolved",
                conflict_state="no-conflict",
                availability_state="available",
                resolution_basis_ref=validation.basis_ref,
                admission_allowed=True,
            ),
        )
        request = self.h._request(
            candidate=candidate,
            source=source,
            execution=execution,
            suffix="external-provenance",
            handling=handling,
        )
        return execution, validation, request

    def test_resolution_basis_is_immutably_reconstructable_from_admission(self) -> None:
        execution, validation, request = self._external_fixture()
        result = admit_governed_organizational_asset(
            state=OrganizationalAssetAdmissionState(),
            capability_adapter=self.h.adapters.capabilities,
            execution=execution,
            request=request,
        )

        resolution_basis = request.source.external_state.resolution_basis_ref
        self.assertEqual(validation.basis_ref, resolution_basis)
        self.assertIn(resolution_basis, validation.record.provenance_refs)
        self.assertIn(validation.record.version_id, result.admission.designation.provenance_refs)
        self.assertIn(validation.record.version_id, result.admission.event.provenance_refs)
        self.assertIs(
            result.admission.admitted_document.canonical_record.authority_mode,
            AuthorityMode.EXTERNAL_REFERENCE,
        )

    def test_external_resolution_basis_mismatch_fails_before_admission(self) -> None:
        execution, _validation, request = self._external_fixture()
        changed_source = replace(
            request.source,
            external_state=replace(
                request.source.external_state,
                resolution_basis_ref=self.h._id(
                    "external-resolution-basis", "stale-or-unrelated-resolution"
                ),
            ),
        )
        with self.assertRaises(ExactAdmissionSourceError):
            admit_governed_organizational_asset(
                state=OrganizationalAssetAdmissionState(),
                capability_adapter=self.h.adapters.capabilities,
                execution=execution,
                request=replace(request, source=changed_source),
            )


if __name__ == "__main__":
    unittest.main()

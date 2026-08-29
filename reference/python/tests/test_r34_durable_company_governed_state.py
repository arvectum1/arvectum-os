from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.document_artifact_governance import (
    AdmittedDocumentVersion,
    ArtifactContent,
    ArtifactState,
    HandlingConstraints,
)
from arvectum_os_ref.event_provenance import CanonicalEvent
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.organizational_asset_admission import (
    CommittedOrganizationalAssetAdmission,
    OrganizationalAssetAdmissionState,
)
from arvectum_os_ref.reviewed_generated_output_promotion import (
    CommittedReviewedGeneratedOutputPromotion,
    ExactGeneratedOutputSource,
    ReviewedGeneratedOutputPromotionState,
)
from arvectum_os_ref.runtime_consistency import (
    ConsequentialAttempt,
    ConsequentialOutcome,
    RetrySemantics,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass
from workspace_app.company_governed_state_store import CompanyGovernedStateStore


UTC = timezone.utc


class R34DurableCompanyGovernedStateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = "r34-durable-org"
        self.organization_id = Identity("organization", self.scope, "platform")
        self.organization = OrganizationScope(self.organization_id)
        self.owner_id = Identity("principal", "owner", self.scope)
        self.actor = ActorContext(Principal(self.owner_id), self.organization)
        self.base = datetime(2026, 8, 29, 20, 0, tzinfo=UTC)

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.scope)

    def _document(self, suffix: str) -> AdmittedDocumentVersion:
        record = CanonicalRecord(
            subject_id=self._id("document", f"doc-{suffix}"),
            version_id=self._id("document-version", f"doc-{suffix}-v1"),
            semantic_type="platform.document",
            schema_version="r34-d1-test-1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.document/state",
            accountable_owner_id=self.owner_id,
            creation_actor=self.actor,
            created_at=self.base,
            provenance_refs=(self.owner_id,),
            integrity_metadata=(("representation", "r34-d1-test"),),
            payload=(("source_material_id", f"material-{suffix}"), ("source_version_id", f"version-{suffix}")),
            lifecycle_status="Admitted",
        )
        artifact = ArtifactContent(
            artifact_id=self._id("artifact", f"artifact-{suffix}"),
            organization=self.organization,
            content_ref=f"sha256:{suffix * 8}",
            media_type="text/plain",
            integrity_ref=(suffix * 64)[:64],
            rendition_role="original",
            handling=HandlingConstraints(
                classification="internal",
                purpose="company-use",
                rights=("company-internal-use",),
                retention_rule="retain-while-current",
            ),
            state=ArtifactState.GOVERNED,
            storage_locator="owner-local-company-materials",
        )
        return AdmittedDocumentVersion(record, (artifact,), "original")

    def _designation(self, suffix: str, document: AdmittedDocumentVersion) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self._id("organizational-asset-subject", f"asset-{suffix}"),
            version_id=self._id("organizational-asset-version", f"asset-{suffix}-v1"),
            semantic_type="platform.organizational-asset-designation",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.document/organizational-asset-designation",
            accountable_owner_id=self.owner_id,
            creation_actor=self.actor,
            created_at=self.base + timedelta(seconds=2),
            provenance_refs=(self.owner_id, document.document_id, document.version_id),
            integrity_metadata=(("representation", "r34-d1-designation"),),
            payload=(("document_version", document.version_id.value),),
            lifecycle_status="Admitted",
        )

    def _event(
        self, suffix: str, document: AdmittedDocumentVersion, designation: CanonicalRecord
    ) -> CanonicalEvent:
        execution_subject = self._id("execution-subject", f"exec-{suffix}")
        execution_version = self._id("execution-version", f"exec-{suffix}-v3")
        event_subject = self._id("event-subject", f"event-{suffix}")
        event_version = self._id("event-version", f"event-{suffix}-v1")
        provenance = (
            self.owner_id,
            execution_subject,
            execution_version,
            document.document_id,
            document.version_id,
            designation.subject_id,
            designation.version_id,
        )
        recorded = self.base + timedelta(seconds=4)
        record = CanonicalRecord(
            subject_id=event_subject,
            version_id=event_version,
            semantic_type="platform.event",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/test",
            accountable_owner_id=self.owner_id,
            creation_actor=self.actor,
            created_at=recorded,
            provenance_refs=provenance,
            integrity_metadata=(("representation", "r34-d1-event"),),
            payload=(("operation", f"operation-{suffix}"),),
            lifecycle_status="Admitted",
        )
        return CanonicalEvent(
            record=record,
            event_type=f"platform.r34.{suffix}",
            event_schema_version="1",
            authoritative_source="Arvectum OS Governed Execution",
            occurred_at=self.base + timedelta(seconds=3),
            recorded_at=recorded,
            producer_id=self.owner_id,
            initiating_actor_id=self.owner_id,
            execution_subject_id=execution_subject,
            execution_version_id=execution_version,
            related_subject_ids=(document.document_id, designation.subject_id),
            related_version_ids=(document.version_id, designation.version_id),
            correlation_refs=(execution_subject,),
            causation_refs=(execution_version,),
            classification="internal",
            access_scope="platform.document/state",
        )

    def _attempt(
        self, suffix: str, retry_token: str, fingerprint: tuple[str, ...], designation: CanonicalRecord, event: CanonicalEvent
    ) -> ConsequentialAttempt:
        return ConsequentialAttempt(
            execution_subject_id=self._id("execution-subject", f"exec-{suffix}"),
            execution_version_id=self._id("execution-version", f"exec-{suffix}-v3"),
            operation_name=f"operation-{suffix}",
            side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token=retry_token,
            fingerprint=fingerprint,
            outcome=ConsequentialOutcome.SUCCEEDED,
            result_version_id=designation.version_id,
            event_version_id=event.version_id,
        )

    def test_admission_state_round_trips_across_store_reconstruction(self) -> None:
        with TemporaryDirectory() as raw:
            root = Path(raw)
            document = self._document("a")
            designation = self._designation("a", document)
            event = self._event("a", document, designation)
            fingerprint = ("admission", "exact-input-a")
            retry_token = "company-asset-admission:r34:a"
            committed = CommittedOrganizationalAssetAdmission(
                admitted_document=document,
                designation=designation,
                event=event,
                retry_token=retry_token,
                fingerprint=fingerprint,
            )
            attempt = self._attempt("a", retry_token, fingerprint, designation, event)
            state = OrganizationalAssetAdmissionState(
                committed=(committed,), admitted_events=(event,), attempts=(attempt,)
            )

            first = CompanyGovernedStateStore(root)
            self.assertEqual(first.persist_admission_state(state), state)
            restarted = CompanyGovernedStateStore(root)
            recovered = restarted.load_admission_state()

            self.assertEqual(recovered, state)
            self.assertEqual(recovered.committed[0].designation.version_id, designation.version_id)
            self.assertEqual(recovered.committed[0].event.version_id, event.version_id)
            self.assertEqual(recovered.attempts[0].retry_token, retry_token)

    def test_promotion_state_round_trips_and_keeps_exact_transient_source_lineage(self) -> None:
        with TemporaryDirectory() as raw:
            root = Path(raw)
            document = self._document("p")
            designation = self._designation("p", document)
            event = self._event("p", document, designation)
            source = ExactGeneratedOutputSource(
                source_subject_id=self._id("transient-output", "out-p"),
                source_version_id=self._id("transient-output-version", "out-p-v1"),
                artifact_id=self._id("artifact", "out-p-artifact"),
                integrity_ref="p" * 64,
                generation_provenance_refs=(document.document_id, document.version_id),
            )
            fingerprint = ("promotion", "exact-output-p")
            retry_token = "company-generated-output-promotion:r34:p"
            committed = CommittedReviewedGeneratedOutputPromotion(
                admitted_document=document,
                designation=designation,
                event=event,
                source=source,
                retry_token=retry_token,
                fingerprint=fingerprint,
            )
            attempt = self._attempt("p", retry_token, fingerprint, designation, event)
            state = ReviewedGeneratedOutputPromotionState(
                committed=(committed,), admitted_events=(event,), attempts=(attempt,)
            )

            first = CompanyGovernedStateStore(root)
            self.assertEqual(first.persist_promotion_state(state), state)
            restarted = CompanyGovernedStateStore(root)
            recovered = restarted.load_promotion_state()

            self.assertEqual(recovered, state)
            self.assertEqual(recovered.committed[0].source, source)
            self.assertEqual(recovered.committed[0].event.version_id, event.version_id)

    def test_intent_time_is_stable_across_restart(self) -> None:
        with TemporaryDirectory() as raw:
            root = Path(raw)
            key = (self.scope, "material-a", "version-a", "policy-a")
            first = CompanyGovernedStateStore(root)
            command_at = first.intent_time(kind="admission", key=key, proposed=self.base)
            restarted = CompanyGovernedStateStore(root)
            repeated = restarted.intent_time(
                kind="admission", key=key, proposed=self.base + timedelta(days=1)
            )
            self.assertEqual(repeated, command_at)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from arvectum_os_ref.identity import Identity
from arvectum_os_ref.organizational_asset_admission import OrganizationalAssetAdmissionState
from arvectum_os_ref.runtime_consistency import (
    ConsequentialAttempt,
    ConsequentialOutcome,
    RetrySemantics,
)
from arvectum_os_ref.workflow import OperationSideEffectClass
from workspace_app.company_governed_state_store import (
    CompanyGovernedStateError,
    CompanyGovernedStateStore,
)


UTC = timezone.utc


class R34DurableStateUncertaintyQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.scope = "r34-d2-uncertainty-org"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.scope)

    def test_uncertain_retry_fingerprint_evidence_survives_restart_exactly(self) -> None:
        retry_token = "r34-d2-uncertain-retry-token"
        fingerprint = (
            "execution:r34-d2-uncertain-v1",
            "company.asset.admit-staged-version",
            "material:r34-d2-material-v1",
            "digest:6b285b2cb0caa0c902e22a78f2fb27fe1e5f50ec2f04319a6af4c991053ed31f",
        )
        uncertain = ConsequentialAttempt(
            execution_subject_id=self._id("execution-subject", "r34-d2-uncertain"),
            execution_version_id=self._id("execution-version", "r34-d2-uncertain-v1"),
            operation_name="company.asset.admit-staged-version",
            side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token=retry_token,
            fingerprint=fingerprint,
            outcome=ConsequentialOutcome.UNCERTAIN,
        )
        state = OrganizationalAssetAdmissionState(attempts=(uncertain,))

        persisted = CompanyGovernedStateStore(self.root).persist_admission_state(state)
        restarted = CompanyGovernedStateStore(self.root).load_admission_state()

        self.assertEqual(persisted, state)
        self.assertEqual(restarted, state)
        self.assertEqual(len(restarted.attempts), 1)
        recovered = restarted.attempts[0]
        self.assertEqual(recovered.retry_token, retry_token)
        self.assertEqual(recovered.fingerprint, fingerprint)
        self.assertIs(recovered.outcome, ConsequentialOutcome.UNCERTAIN)
        self.assertIs(recovered.retry_semantics, RetrySemantics.KEYED_IDEMPOTENT)
        self.assertIs(recovered.side_effect_class, OperationSideEffectClass.CANONICAL_MUTATION)
        self.assertIsNone(recovered.result_version_id)
        self.assertIsNone(recovered.event_version_id)
        self.assertEqual(restarted.committed, ())
        self.assertEqual(restarted.admitted_events, ())

    def test_restarted_effect_journal_rejects_blind_retry_and_retry_token_rebinding(self) -> None:
        store = CompanyGovernedStateStore(self.root)
        retry_token = "r34-d2-effect-retry-token"
        original_key = (
            "company.asset.admit-staged-version",
            "r34-material-1",
            "r34-version-1",
        )
        started_at = datetime(2026, 8, 30, 6, 30, tzinfo=UTC)
        attempt_id = store.begin_effect(
            kind="admission",
            key=original_key,
            retry_token=retry_token,
            started_at=started_at,
        )
        marker = (
            self.root
            / "workspace-company-governed-state"
            / "admission"
            / "effects"
            / f"{attempt_id}.started.json"
        )
        self.assertTrue(marker.is_file())

        restarted = CompanyGovernedStateStore(self.root)
        with self.assertRaisesRegex(CompanyGovernedStateError, "reconciliation is required"):
            restarted.begin_effect(
                kind="admission",
                key=original_key,
                retry_token=retry_token,
                started_at=started_at + timedelta(minutes=1),
            )

        rebound_key = (
            "company.asset.admit-staged-version",
            "r34-material-1",
            "DIFFERENT-r34-version",
        )
        with self.assertRaisesRegex(CompanyGovernedStateError, "different product command"):
            restarted.begin_effect(
                kind="admission",
                key=rebound_key,
                retry_token=retry_token,
                started_at=started_at + timedelta(minutes=2),
            )


if __name__ == "__main__":
    unittest.main()

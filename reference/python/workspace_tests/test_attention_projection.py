from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
import p7_05_operational_visibility as p705
from workspace_app.access import AccessContext, WorkspaceAccessError
from workspace_app.attention import (
    AttentionItem,
    AttentionKind,
    AttentionProjection,
    AttentionProjectionError,
    AttentionUrgency,
    ProjectionFreshness,
    ProjectionHealth,
    RuntimeAttentionProvider,
    scenario_item,
)
from workspace_app.config import WorkspaceSettings
from workspace_app.main import RELEASE_HEADER, create_app
from workspace_app.release import load_release


class FakeResolver:
    def __init__(self) -> None:
        self.denied = False
        self.organization = Identity("organization", "org-a", "platform")
        self.actor = Identity("principal", "actor-a", "org-a")

    def authorize(self) -> AccessContext:
        if self.denied:
            raise WorkspaceAccessError("revoked for test")
        return AccessContext(
            organization=self.organization,
            actor=self.actor,
            principal_kind="human",
            credential_id="credential-test",
            grant_id="grant-test",
        )


class FakeProvider:
    def __init__(self, projection: AttentionProjection) -> None:
        self.projection = projection
        self.seen: list[AccessContext] = []

    def project(self, access: AccessContext) -> AttentionProjection:
        self.seen.append(access)
        return self.projection


def _settings(root: Path) -> WorkspaceSettings:
    return WorkspaceSettings(
        runtime_root=root,
        public_origin="http://127.0.0.1:8769",
        bind_host="127.0.0.1",
        bind_port=8769,
        allowed_hosts=("127.0.0.1:8769",),
        organization_label="ООО «Арвектум»",
        actor_label="Owner operator",
        session_idle_seconds=60,
        session_absolute_seconds=300,
        allow_loopback_http=True,
    )


def _fresh_projection(*items: AttentionItem) -> AttentionProjection:
    return AttentionProjection(
        generated_at="2026-08-21T10:00:00Z",
        health=ProjectionHealth(
            ProjectionFreshness.FRESH,
            "OK",
            "Attention sources were evaluated against current governed state.",
            "2026-08-21T10:00:00Z",
            1.5,
        ),
        items=tuple(items),
    )


class AttentionContractTests(unittest.TestCase):
    def test_normalized_attention_kinds_cover_j1_without_implying_authority(self) -> None:
        kinds = (
            AttentionKind.WAITING_APPROVAL,
            AttentionKind.WAITING_INPUT,
            AttentionKind.RECONCILIATION_REQUIRED,
            AttentionKind.GUARDED_ACTION_FAILED,
            AttentionKind.RECOVERABLE_SYSTEM_CONDITION,
            AttentionKind.RECENT_OUTCOME,
            AttentionKind.INFORMATIONAL,
        )
        items = tuple(
            scenario_item(
                source_fingerprint=kind.value,
                kind=kind,
                urgency=AttentionUrgency.MEDIUM,
                title=f"Scenario {kind.value}",
                reason="Controlled acceptance reason.",
                source_label="P9.04 controlled acceptance fixture",
                next_step="Inspect the source context only.",
                observed_at="2026-08-21T10:00:00Z",
            )
            for kind in kinds
        )
        payload = _fresh_projection(*items).to_payload()
        self.assertEqual(len(payload["items"]), len(kinds))
        serialized = json.dumps(payload)
        self.assertIn('"evidence_mode": "scenario"', serialized)
        self.assertIn('"interaction": "inspect-only"', serialized)
        self.assertIn('"canonical_authority": false', serialized)
        self.assertIn('"organizational_authority_provided": false', serialized)
        self.assertIn('"visibility_implies_permission": false', serialized)

    def test_item_deep_link_is_bounded_and_opaque(self) -> None:
        item = scenario_item(
            source_fingerprint="raw/execution/version?secret=1",
            kind=AttentionKind.WAITING_INPUT,
            urgency=AttentionUrgency.HIGH,
            title="Input required",
            reason="A governed input is missing.",
            source_label="Controlled scenario",
            next_step="Inspect the blocker.",
        )
        payload = item.to_payload()
        self.assertRegex(item.attention_id, r"^[0-9a-f]{20}$")
        self.assertEqual(payload["open_href"], f"/my-work?focus={item.attention_id}")
        self.assertNotIn("execution", json.dumps(payload))
        self.assertFalse(payload["authority_provided"])

    def test_duplicate_attention_ids_fail_closed(self) -> None:
        item = scenario_item(
            source_fingerprint="same",
            kind=AttentionKind.INFORMATIONAL,
            urgency=AttentionUrgency.LOW,
            title="Information",
            reason="Informational projection.",
            source_label="Controlled scenario",
            next_step="No action required.",
        )
        with self.assertRaises(AttentionProjectionError):
            _fresh_projection(item, item)


class RuntimeAttentionProviderTests(unittest.TestCase):
    def test_stale_runtime_withholds_work_items_and_surfaces_recoverable_condition(self) -> None:
        def health(_: Path) -> p705.HealthStatus:
            return p705.HealthStatus("down", "HEARTBEAT_STALE", "secret diagnostic", "restart", "sha", 120.0)

        provider = RuntimeAttentionProvider(Path("/tmp/runtime"), health_reader=health)
        access = AccessContext(
            Identity("organization", "org-a", "platform"),
            Identity("principal", "actor-a", "org-a"),
            "human",
            "cred",
            "grant",
        )
        payload = provider.project(access).to_payload()
        self.assertEqual(payload["health"]["state"], "stale")
        self.assertEqual(len(payload["items"]), 1)
        self.assertEqual(payload["items"][0]["kind"], "recoverable-system-condition")
        self.assertNotIn("secret diagnostic", json.dumps(payload))

    def test_healthy_runtime_has_no_owner_work_without_an_actionable_source(self) -> None:
        def health(_: Path) -> p705.HealthStatus:
            return p705.HealthStatus("healthy", "OK", "healthy", "none", "sha", 1.0)

        provider = RuntimeAttentionProvider(Path("/tmp/runtime"), health_reader=health)
        access = AccessContext(
            Identity("organization", "org-a", "platform"),
            Identity("principal", "actor-a", "org-a"),
            "human",
            "cred",
            "grant",
        )
        payload = provider.project(access).to_payload()
        self.assertEqual(payload["health"]["state"], "fresh")
        self.assertEqual(payload["items"], [])
        self.assertNotIn("waiting-input", json.dumps(payload))

    def test_preflight_proof_cannot_create_owner_work_without_a_concrete_outcome(self) -> None:
        def health(_: Path) -> p705.HealthStatus:
            return p705.HealthStatus("healthy", "OK", "healthy", "none", "sha", 1.0)

        provider = RuntimeAttentionProvider(Path("/tmp/runtime"), health_reader=health)
        access = AccessContext(
            Identity("organization", "org-a", "platform"),
            Identity("principal", "actor-a", "org-a"),
            "human",
            "cred",
            "grant",
        )
        payload = provider.project(access).to_payload()
        self.assertEqual(payload["items"], [])
        self.assertNotIn("waiting-input", json.dumps(payload))
        self.assertNotIn('"urgency": "high"', json.dumps(payload))


class MyWorkBffTests(unittest.TestCase):
    def test_endpoint_uses_current_server_authorized_context_and_minimized_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            static = root / "dist"
            static.mkdir()
            (static / "index.html").write_text("<!doctype html><div id='root'></div>", encoding="utf-8")
            (static / "assets").mkdir()
            projection = _fresh_projection(
                scenario_item(
                    source_fingerprint="one",
                    kind=AttentionKind.RECONCILIATION_REQUIRED,
                    urgency=AttentionUrgency.HIGH,
                    title="External outcome is uncertain",
                    reason="Reconciliation is required before any retry.",
                    source_label="Controlled P8.05 scenario",
                    next_step="Reconcile the external outcome; do not retry blindly.",
                )
            )
            provider = FakeProvider(projection)
            resolver = FakeResolver()
            client = TestClient(
                create_app(
                    _settings(root),
                    access_resolver=resolver,
                    attention_provider=provider,
                    static_dir=static,
                ),
                base_url="http://127.0.0.1:8769",
                client=("127.0.0.1", 50000),
            )
            release = load_release().release_id
            headers = {RELEASE_HEADER: release}
            bootstrap = client.post(
                "/api/app/v1/session/bootstrap",
                headers={**headers, "Origin": "http://127.0.0.1:8769"},
            )
            self.assertEqual(bootstrap.status_code, 200)
            response = client.get(
                "/api/app/v1/my-work?organization=foreign&actor=attacker",
                headers={**headers, "X-Organization": "foreign", "X-Actor": "attacker"},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(provider.seen), 1)
            self.assertEqual(provider.seen[0].organization, resolver.organization)
            self.assertEqual(provider.seen[0].actor, resolver.actor)
            payload = response.json()
            self.assertFalse(payload["projection"]["canonical_authority"])
            self.assertFalse(payload["projection"]["visibility_implies_permission"])
            self.assertFalse(payload["scope"]["denied_item_counts_exposed"])
            serialized = json.dumps(payload)
            self.assertNotIn("foreign", serialized)
            self.assertNotIn("attacker", serialized)
            self.assertNotIn("org-a", serialized)
            self.assertNotIn("actor-a", serialized)
            client.close()


if __name__ == "__main__":
    unittest.main()

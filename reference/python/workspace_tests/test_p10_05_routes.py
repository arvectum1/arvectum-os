from __future__ import annotations

import base64
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

import p7_04_persistent_access as p704
from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
from p9_03_workspace import build_workspace_app
from workspace_app.access import P704AccessResolver, provision_workspace_grant
from workspace_app.company_asset_governed_provider import provision_company_asset_admission_grant
from workspace_app.company_generated_output_governed_provider import (
    provision_company_generated_output_promotion_grant,
)
from workspace_app.config import WorkspaceSettings
from workspace_app.main import CSRF_HEADER, RELEASE_HEADER
from workspace_app.release import load_release


DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def docx_template() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr(
            "word/document.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            "<w:body><w:p><w:r><w:t>{{TITLE}} {{BODY}} {{DATE}}</w:t></w:r></w:p></w:body></w:document>",
        )
    return buffer.getvalue()


def settings(root: Path) -> WorkspaceSettings:
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


class P1005ProductiveRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.organization = Identity("organization", "p10-05-route-org", "platform")
        self.owner = Identity("principal", "p10-05-route-owner", self.organization.value)
        p704.initialize_access_store(self.root, self.organization)
        p704.register_principal(self.root, self.owner, kind="human")
        p704.issue_credential(self.root, self.owner)
        provision_workspace_grant(self.root)
        provision_company_asset_admission_grant(self.root)
        self.access = P704AccessResolver(self.root).authorize()

        self.app = build_workspace_app(settings(self.root))
        self.materials = self.app.state.company_materials_store
        self.assets = self.app.state.company_asset_library
        self.outputs = self.app.state.company_generated_outputs

        staged = self.materials.stage(
            self.access,
            {
                "project_id": "COMPANY",
                "filename": "route-template.docx",
                "media_type": DOCX_MEDIA_TYPE,
                "semantic_role": "document-template",
                "classification": "internal",
                "purpose": "company governed document generation",
                "rights": "company-internal-use",
                "retention_rule": "retain-while-current-plus-governed-history",
                "content_base64": base64.b64encode(docx_template()).decode("ascii"),
            },
        )["material"]
        self.material_id = str(staged["material_id"])
        self.version_id = str(staged["version_id"])
        self.assets.submit_review(
            self.access,
            self.material_id,
            self.version_id,
            {
                "deletion_rule": "delete-only-through-governed-retention-process",
                "permitted_reuse": ["company-internal-document-generation"],
            },
        )
        self.assets.admit(self.access, self.material_id, self.version_id)
        generated = self.assets.generate_docx(
            self.access,
            {
                "material_id": self.material_id,
                "version_id": self.version_id,
                "title": "Route reviewed output",
                "body": "P10.05 BFF journey",
                "date": "2026-08-29",
            },
        )
        self.output_id = str(generated["output"]["output_id"])

        self.client = TestClient(
            self.app,
            base_url="http://127.0.0.1:8769",
            client=("127.0.0.1", 50000),
        )
        self.release_headers = {RELEASE_HEADER: load_release().release_id}
        bootstrap = self.client.post(
            "/api/app/v1/session/bootstrap",
            headers={**self.release_headers, "Origin": "http://127.0.0.1:8769"},
        )
        self.assertEqual(bootstrap.status_code, 200)
        self.csrf = bootstrap.json()["session"]["csrf_token"]

    def tearDown(self) -> None:
        self.client.close()
        self.temp.cleanup()

    @property
    def command_headers(self) -> dict[str, str]:
        return {
            **self.release_headers,
            "Origin": "http://127.0.0.1:8769",
            CSRF_HEADER: self.csrf,
        }

    def test_productive_composition_installs_p10_05_without_auto_grant(self) -> None:
        self.assertIs(self.app.state.company_generated_outputs, self.outputs)
        response = self.client.get("/api/app/v1/company-generated-outputs", headers=self.release_headers)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["actions"]["governed_promotion_available"])
        state = p704.load_access_store(self.root)
        self.assertFalse(any(
            grant["operation"] == "company.generated-output.promote-reviewed"
            for grant in state["grants"].values()
        ))

    def test_review_is_csrf_protected_and_never_changes_canonical_state(self) -> None:
        path = f"/api/app/v1/company-generated-outputs/{self.output_id}/review"
        missing = self.client.post(
            path,
            headers={**self.release_headers, "Origin": "http://127.0.0.1:8769"},
            json={"disposition": "KeepTransient"},
        )
        self.assertEqual(missing.status_code, 403)

        kept = self.client.post(
            path,
            headers=self.command_headers,
            json={"disposition": "KeepTransient"},
        )
        self.assertEqual(kept.status_code, 200)
        self.assertFalse(kept.json()["canonical_state_changed"])
        self.assertEqual(kept.json()["source_state"], "TransientOutput")
        _, manifest = self.materials.output_path(self.access, self.output_id)
        self.assertEqual(manifest["state"], "TransientOutput")
        self.assertEqual(len(self.outputs.promotion.state.committed), 0)

    def test_promotion_is_separate_command_and_fail_closed_until_exact_grant_exists(self) -> None:
        review_path = f"/api/app/v1/company-generated-outputs/{self.output_id}/review"
        requested = self.client.post(
            review_path,
            headers=self.command_headers,
            json={
                "disposition": "PromotionRequested",
                "document_title": "Route reviewed output",
                "semantic_role": "company-project-document",
            },
        )
        self.assertEqual(requested.status_code, 200)
        self.assertFalse(requested.json()["canonical_state_changed"])

        promote_path = f"/api/app/v1/company-generated-outputs/{self.output_id}/promote"
        blocked = self.client.post(promote_path, headers=self.command_headers)
        self.assertEqual(blocked.status_code, 503)
        self.assertEqual(blocked.json()["detail"], "COMPANY_OUTPUT_PROMOTION_UNAVAILABLE")
        self.assertEqual(len(self.outputs.promotion.state.committed), 0)

        provision_company_generated_output_promotion_grant(self.root)
        promoted = self.client.post(promote_path, headers=self.command_headers)
        self.assertEqual(promoted.status_code, 200)
        body = promoted.json()
        self.assertTrue(body["canonical_state_changed"])
        self.assertTrue(body["through_governed_execution"])
        self.assertFalse(body["source_relabelled"])
        self.assertFalse(body["validated_knowledge_created"])
        _, manifest = self.materials.output_path(self.access, self.output_id)
        self.assertEqual(manifest["state"], "TransientOutput")

    def test_missing_current_admitted_source_returns_fail_closed_503_not_500(self) -> None:
        self.client.post(
            f"/api/app/v1/company-generated-outputs/{self.output_id}/review",
            headers=self.command_headers,
            json={
                "disposition": "PromotionRequested",
                "document_title": "Route reviewed output",
                "semantic_role": "company-project-document",
            },
        )
        provision_company_generated_output_promotion_grant(self.root)
        self.assets.admission.state = type(self.assets.admission.state)()
        response = self.client.post(
            f"/api/app/v1/company-generated-outputs/{self.output_id}/promote",
            headers=self.command_headers,
        )
        self.assertEqual(response.status_code, 503)
        self.assertNotEqual(response.status_code, 500)
        self.assertEqual(len(self.outputs.promotion.state.committed), 0)


if __name__ == "__main__":
    unittest.main()

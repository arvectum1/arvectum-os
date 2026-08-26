from __future__ import annotations

import base64
import io
import tempfile
import unittest
import zipfile
from pathlib import Path

from fastapi.testclient import TestClient

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.company_materials import CompanyMaterialsStore
from workspace_app.config import WorkspaceSettings
from workspace_app.f11_routes import install_f11_routes
from workspace_app.main import CSRF_HEADER, RELEASE_HEADER, create_app
from workspace_app.release import load_release


DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


class FakeResolver:
    def __init__(self) -> None:
        self.organization = Identity("organization", "org-a", "platform")
        self.actor = Identity("principal", "owner-a", "org-a")

    def authorize(self) -> AccessContext:
        return AccessContext(
            organization=self.organization,
            actor=self.actor,
            principal_kind="human",
            credential_id="credential-f11",
            grant_id="grant-f11",
        )


class FakePortfolio:
    def project(self, access: AccessContext):
        return {
            "schema": "arvectum.workspace.company-portfolio/1",
            "product_contract": {"id": "P9.11-F11", "version": "0.1.0", "lifecycle": "Provisional"},
            "projects": [
                {
                    "id": "PORT-002",
                    "label": "Data Platform",
                    "state": "reconciliation-required",
                    "source": None,
                    "roadmap": {"status": None},
                }
            ],
            "scope": {"actor": access.actor.value},
        }


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


class F11WorkspaceRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.static = self.root / "dist"
        self.static.mkdir()
        (self.static / "index.html").write_text("<!doctype html><div id='root'>SPA</div>", encoding="utf-8")
        (self.static / "assets").mkdir()
        app = create_app(settings(self.root), access_resolver=FakeResolver(), static_dir=self.static)
        install_f11_routes(
            app,
            portfolio_provider=FakePortfolio(),  # type: ignore[arg-type]
            materials_store=CompanyMaterialsStore(self.root),
        )
        self.client = TestClient(app, base_url="http://127.0.0.1:8769", client=("127.0.0.1", 50000))
        self.release = load_release().release_id
        self.release_headers = {RELEASE_HEADER: self.release}
        bootstrap = self.client.post(
            "/api/app/v1/session/bootstrap",
            headers={**self.release_headers, "Origin": "http://127.0.0.1:8769"},
        )
        self.assertEqual(bootstrap.status_code, 200)
        self.csrf = bootstrap.json()["session"]["csrf_token"]

    def tearDown(self) -> None:
        self.client.close()
        self.temp.cleanup()

    def test_portfolio_route_precedes_spa_and_is_session_protected(self) -> None:
        response = self.client.get("/api/app/v1/company/portfolio", headers=self.release_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["projects"][0]["state"], "reconciliation-required")
        self.client.cookies.clear()
        denied = self.client.get("/api/app/v1/company/portfolio", headers=self.release_headers)
        self.assertEqual(denied.status_code, 401)
        self.assertNotIn("SPA", denied.text)

    def test_stage_requires_csrf_and_returns_noncanonical_exact_version(self) -> None:
        payload = {
            "project_id": "COMPANY",
            "filename": "template.docx",
            "media_type": DOCX_MEDIA_TYPE,
            "semantic_role": "document-template",
            "classification": "internal",
            "purpose": "company standard",
            "rights": "company-internal-use",
            "retention_rule": "until-replaced",
            "content_base64": base64.b64encode(docx_template()).decode("ascii"),
        }
        missing = self.client.post(
            "/api/app/v1/company-materials",
            headers={**self.release_headers, "Origin": "http://127.0.0.1:8769"},
            json=payload,
        )
        self.assertEqual(missing.status_code, 403)
        staged = self.client.post(
            "/api/app/v1/company-materials",
            headers={
                **self.release_headers,
                "Origin": "http://127.0.0.1:8769",
                CSRF_HEADER: self.csrf,
            },
            json=payload,
        )
        self.assertEqual(staged.status_code, 200)
        material = staged.json()["material"]
        self.assertEqual(material["state"], "StagedNonCanonical")
        self.assertFalse(staged.json()["governance"]["canonical_state_changed"])

        projection = self.client.get("/api/app/v1/company-materials", headers=self.release_headers)
        self.assertEqual(projection.status_code, 200)
        self.assertEqual(projection.json()["materials"][0]["latest_version_id"], material["version_id"])

    def test_generation_pins_exact_source_and_downloads_transient_docx(self) -> None:
        stage_payload = {
            "project_id": "COMPANY",
            "filename": "template.docx",
            "media_type": DOCX_MEDIA_TYPE,
            "semantic_role": "document-template",
            "classification": "internal",
            "purpose": "company standard",
            "rights": "company-internal-use",
            "retention_rule": "until-replaced",
            "content_base64": base64.b64encode(docx_template()).decode("ascii"),
        }
        headers = {**self.release_headers, "Origin": "http://127.0.0.1:8769", CSRF_HEADER: self.csrf}
        material = self.client.post("/api/app/v1/company-materials", headers=headers, json=stage_payload).json()["material"]
        generated = self.client.post(
            "/api/app/v1/company-materials/generate",
            headers=headers,
            json={
                "material_id": material["material_id"],
                "version_id": material["version_id"],
                "title": "Заголовок",
                "body": "Содержание",
                "date": "26.08.2026",
            },
        )
        self.assertEqual(generated.status_code, 200)
        output = generated.json()["output"]
        self.assertEqual(output["source_version_id"], material["version_id"])
        self.assertEqual(output["state"], "TransientOutput")
        download = self.client.get(output["download_href"], headers=self.release_headers)
        self.assertEqual(download.status_code, 200)
        self.assertEqual(download.headers["content-type"], DOCX_MEDIA_TYPE)
        self.assertGreater(len(download.content), 100)


if __name__ == "__main__":
    unittest.main()

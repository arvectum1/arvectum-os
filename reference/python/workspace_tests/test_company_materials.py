from __future__ import annotations

import base64
import io
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.company_materials import (
    CompanyMaterialUnavailable,
    CompanyMaterialsInputError,
    CompanyMaterialsStore,
    DOCX_MEDIA_TYPE,
)


def _access(org: str = "arvectum", actor: str = "owner") -> AccessContext:
    return AccessContext(
        organization=Identity("organization", org, org),
        actor=Identity("principal", actor, org),
        principal_kind="human",
        credential_id=f"cred-{actor}",
        grant_id="grant-workspace",
    )


def _docx(text: str, *, macro: bool = False) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"></Types>',
        )
        archive.writestr(
            "word/document.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f"<w:body><w:p><w:r><w:t>{text}</w:t></w:r></w:p></w:body></w:document>",
        )
        if macro:
            archive.writestr("word/vbaProject.bin", b"not-executable-test-fixture")
    return buffer.getvalue()


def _payload(content: bytes, *, material_id: str | None = None, purpose: str = "Единый стандарт документов") -> dict[str, object]:
    payload: dict[str, object] = {
        "project_id": "COMPANY",
        "filename": "letter-template.docx",
        "media_type": DOCX_MEDIA_TYPE,
        "semantic_role": "document-template",
        "classification": "internal",
        "purpose": purpose,
        "rights": "company-internal-use",
        "retention_rule": "until-replaced-or-explicit-deletion",
        "content_base64": base64.b64encode(content).decode("ascii"),
    }
    if material_id is not None:
        payload["material_id"] = material_id
    return payload


class CompanyMaterialsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = CompanyMaterialsStore(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_staged_material_preserves_exact_version_lineage_and_governance_boundary(self) -> None:
        first = self.store.stage(_access(), _payload(_docx("{{TITLE}} — {{BODY}}")))
        material = first["material"]

        self.assertEqual(material["state"], "StagedNonCanonical")
        self.assertFalse(material["canonical_authority"])
        self.assertEqual(material["organization"], "organization:arvectum@arvectum")
        self.assertFalse(first["governance"]["canonical_admission_available"])
        self.assertFalse(first["governance"]["canonical_state_changed"])

        second = self.store.stage(
            _access(),
            _payload(_docx("{{TITLE}} / {{DATE}} / {{BODY}}"), material_id=material["material_id"]),
        )
        second_version = second["material"]
        self.assertEqual(second_version["predecessor_version_id"], material["version_id"])
        self.assertNotEqual(second_version["version_id"], material["version_id"])
        self.assertNotEqual(second_version["content_sha256"], material["content_sha256"])

        projection = self.store.project(_access())
        self.assertEqual(
            projection["product_contract"],
            {"id": "P9.11-F11", "version": "0.1.0", "lifecycle": "Provisional"},
        )
        self.assertEqual(projection["materials"][0]["latest_version_id"], second_version["version_id"])
        self.assertEqual(len(projection["materials"][0]["versions"]), 2)

    def test_exact_docx_version_generates_transient_output_with_provenance(self) -> None:
        staged = self.store.stage(_access(), _payload(_docx("{{TITLE}} | {{BODY}} | {{DATE}}")))["material"]
        result = self.store.generate_docx(
            _access(),
            {
                "material_id": staged["material_id"],
                "version_id": staged["version_id"],
                "title": "Коммерческое предложение",
                "body": "Текст документа",
                "date": "26.08.2026",
            },
        )

        output = result["output"]
        self.assertEqual(output["state"], "TransientOutput")
        self.assertFalse(output["canonical_authority"])
        self.assertEqual(output["organization"], staged["organization"])
        self.assertEqual(output["source_version_id"], staged["version_id"])
        self.assertEqual(output["source_sha256"], staged["content_sha256"])
        self.assertFalse(result["governance"]["canonical_state_changed"])
        path, manifest = self.store.output_path(_access(), output["output_id"])
        self.assertTrue(path.is_file())
        self.assertEqual(manifest["output_sha256"], output["output_sha256"])
        with zipfile.ZipFile(path, "r") as archive:
            xml = archive.read("word/document.xml").decode("utf-8")
        self.assertIn("Коммерческое предложение", xml)
        self.assertIn("Текст документа", xml)
        self.assertIn("26.08.2026", xml)

    def test_generation_requires_supported_placeholder_and_exact_version(self) -> None:
        staged = self.store.stage(_access(), _payload(_docx("Обычный текст")))["material"]
        with self.assertRaisesRegex(CompanyMaterialsInputError, "placeholder"):
            self.store.generate_docx(
                _access(),
                {
                    "material_id": staged["material_id"],
                    "version_id": staged["version_id"],
                    "title": "A",
                    "body": "B",
                    "date": "C",
                },
            )

    def test_duplicate_version_and_unsafe_project_fail_closed(self) -> None:
        content = _docx("{{TITLE}}")
        staged = self.store.stage(_access(), _payload(content))["material"]
        with self.assertRaisesRegex(CompanyMaterialsInputError, "must differ"):
            self.store.stage(_access(), _payload(content, material_id=staged["material_id"]))

        invalid = _payload(content)
        invalid["project_id"] = "some-repo-name"
        with self.assertRaisesRegex(CompanyMaterialsInputError, "PORT-nnn"):
            self.store.stage(_access(), invalid)

    def test_actual_content_is_validated_and_active_or_opaque_formats_fail_closed(self) -> None:
        fake_docx = _payload(b"not a zip package")
        with self.assertRaisesRegex(CompanyMaterialsInputError, "Office"):
            self.store.stage(_access(), fake_docx)

        opaque = _payload(b"opaque")
        opaque["media_type"] = "application/octet-stream"
        with self.assertRaisesRegex(CompanyMaterialsInputError, "allowlist"):
            self.store.stage(_access(), opaque)

        svg = _payload(b"<svg><script>alert(1)</script></svg>")
        svg["filename"] = "logo.svg"
        svg["media_type"] = "image/svg+xml"
        with self.assertRaisesRegex(CompanyMaterialsInputError, "allowlist"):
            self.store.stage(_access(), svg)

        macro = _payload(_docx("{{TITLE}}", macro=True))
        with self.assertRaisesRegex(CompanyMaterialsInputError, "macro-enabled"):
            self.store.stage(_access(), macro)

    def test_organization_scope_is_bound_for_projection_generation_and_download(self) -> None:
        owner_a = _access("org-a", "owner-a")
        owner_b = _access("org-b", "owner-b")
        staged = self.store.stage(owner_a, _payload(_docx("{{TITLE}}")))["material"]

        self.assertEqual(self.store.project(owner_b)["materials"], [])
        with self.assertRaises(CompanyMaterialUnavailable):
            self.store.stage(owner_b, _payload(_docx("{{TITLE}} v2"), material_id=staged["material_id"]))
        with self.assertRaises(CompanyMaterialUnavailable):
            self.store.generate_docx(
                owner_b,
                {
                    "material_id": staged["material_id"],
                    "version_id": staged["version_id"],
                    "title": "A",
                    "body": "B",
                    "date": "C",
                },
            )

        generated = self.store.generate_docx(
            owner_a,
            {
                "material_id": staged["material_id"],
                "version_id": staged["version_id"],
                "title": "A",
                "body": "B",
                "date": "C",
            },
        )["output"]
        with self.assertRaises(CompanyMaterialUnavailable):
            self.store.output_path(owner_b, generated["output_id"])

    def test_manifest_contains_no_encoded_content_and_store_permissions_are_owner_only(self) -> None:
        raw = _docx("{{BODY}}")
        staged = self.store.stage(_access(), _payload(raw))["material"]
        manifest_path = self.store.manifests / f"{staged['material_id']}.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        serialized = json.dumps(manifest)
        self.assertNotIn(base64.b64encode(raw).decode("ascii"), serialized)
        self.assertEqual(manifest["organization"], "organization:arvectum@arvectum")
        self.assertIn('"state": "StagedNonCanonical"', serialized)
        self.assertIn('"validated_knowledge": false', serialized)
        if os.name == "posix":
            self.assertEqual(manifest_path.stat().st_mode & 0o777, 0o600)
            blob = self.store.blobs / staged["content_sha256"]
            self.assertEqual(blob.stat().st_mode & 0o777, 0o600)
            self.assertEqual(self.store.manifests.stat().st_mode & 0o777, 0o700)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import base64
import io
import tempfile
import unittest
import zipfile
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.company_asset_library import (
    AdmittedCompanyAssetVersion,
    CompanyAssetLibrary,
    CompanyAssetReviewError,
    CompanyAssetReviewPolicy,
)
from workspace_app.company_materials import CompanyMaterialUnavailable, CompanyMaterialsStore


DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def docx_template(label: str = "v1") -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr(
            "word/document.xml",
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f"<w:body><w:p><w:r><w:t>{{{{TITLE}}}} {{{{BODY}}}} {{{{DATE}}}} {label}</w:t></w:r></w:p></w:body></w:document>",
        )
    return buffer.getvalue()


class RecordingAdmission:
    def __init__(self) -> None:
        self.items: dict[str, list[AdmittedCompanyAssetVersion]] = {}
        self.calls: list[tuple[str, str, CompanyAssetReviewPolicy]] = []

    def _scope(self, access: AccessContext) -> str:
        return access.organization.value

    def available(self, access: AccessContext) -> bool:
        return True

    def admitted_versions(self, access: AccessContext) -> tuple[AdmittedCompanyAssetVersion, ...]:
        return tuple(self.items.get(self._scope(access), ()))

    def admit(
        self,
        *,
        access: AccessContext,
        store: CompanyMaterialsStore,
        material_id: str,
        version_id: str,
        policy: CompanyAssetReviewPolicy,
    ) -> AdmittedCompanyAssetVersion:
        version = store._version(access, material_id, version_id)
        scoped = list(self.items.get(self._scope(access), ()))
        scoped = [
            replace(item, current=False) if item.material_id == material_id and item.current else item
            for item in scoped
        ]
        admitted = AdmittedCompanyAssetVersion(
            material_id=material_id,
            version_id=version_id,
            document_subject=f"document:{material_id}",
            document_version=f"document-version:{version_id}",
            designation_subject=f"organizational-asset:{material_id}",
            designation_version=f"organizational-asset-version:{version_id}",
            event_version=f"event-version:{version_id}",
            admitted_at=datetime.now(timezone.utc).isoformat(),
            provenance_refs=(f"staged:{material_id}", f"staged-version:{version_id}"),
            current=True,
        )
        scoped.append(admitted)
        self.items[self._scope(access)] = scoped
        self.calls.append((material_id, version_id, policy))
        return admitted


class CompanyAssetLibraryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = CompanyMaterialsStore(self.root)
        self.admission = RecordingAdmission()
        self.library = CompanyAssetLibrary(self.store, self.admission)
        self.access = AccessContext(
            organization=Identity("organization", "org-a", "platform"),
            actor=Identity("principal", "owner-a", "org-a"),
            principal_kind="human",
            credential_id="credential-p10-04",
            grant_id="grant-p10-04",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _stage(self, *, material_id: str | None = None, label: str = "v1") -> dict[str, object]:
        payload: dict[str, object] = {
            "project_id": "COMPANY",
            "filename": "company-template.docx",
            "media_type": DOCX_MEDIA_TYPE,
            "semantic_role": "document-template",
            "classification": "internal",
            "purpose": "company standard",
            "rights": "company-internal-use",
            "retention_rule": "retain-while-current-plus-history",
            "content_base64": base64.b64encode(docx_template(label)).decode("ascii"),
        }
        if material_id is not None:
            payload["material_id"] = material_id
        return self.store.stage(self.access, payload)["material"]

    @staticmethod
    def review_payload() -> dict[str, object]:
        return {
            "deletion_rule": "delete-only-through-governed-retention-process",
            "permitted_reuse": ["company-internal-document-generation"],
        }

    def test_four_views_keep_staging_review_noncanonical(self) -> None:
        version = self._stage()
        material_id = str(version["material_id"])
        version_id = str(version["version_id"])

        initial = self.library.project(self.access)
        self.assertEqual([item["version_id"] for item in initial["views"]["drafts"]], [version_id])
        self.assertFalse(initial["governance"]["staging_is_canonical"])
        self.assertFalse(initial["governance"]["review_state_is_canonical"])

        review = self.library.submit_review(self.access, material_id, version_id, self.review_payload())
        self.assertEqual(review["state"], "InReview")
        self.assertFalse(review["canonical_authority"])
        reviewing = self.library.project(self.access)
        self.assertEqual([item["version_id"] for item in reviewing["views"]["review"]], [version_id])
        self.assertEqual(reviewing["views"]["review"][0]["staging_state"], "StagedNonCanonical")

        rejected = self.library.reject(self.access, material_id, version_id, {"reason": "metadata needs correction"})
        self.assertEqual(rejected["state"], "Rejected")
        archived = self.library.project(self.access)
        self.assertEqual([item["version_id"] for item in archived["views"]["archive"]], [version_id])
        self.assertIsNone(archived["views"]["archive"][0]["canonical"])

        reloaded = CompanyAssetLibrary(CompanyMaterialsStore(self.root), self.admission).project(self.access)
        self.assertEqual(reloaded["views"]["archive"][0]["review"]["state"], "Rejected")

    def test_admission_and_new_version_preserve_immutable_history_and_currentness(self) -> None:
        first = self._stage(label="v1")
        material_id = str(first["material_id"])
        first_id = str(first["version_id"])
        self.library.submit_review(self.access, material_id, first_id, self.review_payload())
        admitted_first = self.library.admit(self.access, material_id, first_id)
        self.assertTrue(admitted_first.current)
        self.assertEqual(self.admission.calls[0][2].deletion_rule, self.review_payload()["deletion_rule"])

        second = self._stage(material_id=material_id, label="v2")
        second_id = str(second["version_id"])
        self.assertEqual(second["predecessor_version_id"], first_id)
        before_second_admission = self.library.project(self.access)
        self.assertEqual(before_second_admission["views"]["accepted"][0]["version_id"], first_id)
        self.assertEqual(before_second_admission["views"]["drafts"][0]["version_id"], second_id)

        self.library.submit_review(self.access, material_id, second_id, self.review_payload())
        self.library.admit(self.access, material_id, second_id)
        after = self.library.project(self.access)
        self.assertEqual([item["version_id"] for item in after["views"]["accepted"]], [second_id])
        archived_ids = [item["version_id"] for item in after["views"]["archive"]]
        self.assertIn(first_id, archived_ids)
        self.assertEqual(after["views"]["accepted"][0]["canonical"]["current"], True)
        self.assertEqual(
            next(item for item in after["views"]["archive"] if item["version_id"] == first_id)["canonical"]["current"],
            False,
        )

    def test_generation_requires_exact_admitted_version(self) -> None:
        version = self._stage()
        material_id = str(version["material_id"])
        version_id = str(version["version_id"])
        generation = {
            "material_id": material_id,
            "version_id": version_id,
            "title": "Title",
            "body": "Body",
            "date": "2026-08-28",
        }
        with self.assertRaises(CompanyMaterialUnavailable):
            self.library.generate_docx(self.access, generation)

        self.library.submit_review(self.access, material_id, version_id, self.review_payload())
        self.library.admit(self.access, material_id, version_id)
        generated = self.library.generate_docx(self.access, generation)
        self.assertEqual(generated["output"]["state"], "TransientOutput")
        self.assertTrue(generated["governance"]["source_admitted_company_asset"])
        self.assertFalse(generated["governance"]["canonical_state_changed"])

    def test_review_transition_and_export_fail_closed(self) -> None:
        version = self._stage()
        material_id = str(version["material_id"])
        version_id = str(version["version_id"])
        with self.assertRaises(CompanyAssetReviewError):
            self.library.reject(self.access, material_id, version_id, {"reason": "not reviewed"})
        with self.assertRaises(CompanyAssetReviewError):
            self.library.submit_review(
                self.access,
                material_id,
                version_id,
                {"deletion_rule": "x", "permitted_reuse": []},
            )
        exported = self.library.export(self.access, limit=1)
        self.assertTrue(exported["bounded"])
        self.assertFalse(exported["canonical_authority"])
        self.assertEqual(len(exported["items"]), 1)
        with self.assertRaises(CompanyAssetReviewError):
            self.library.export(self.access, limit=101)


if __name__ == "__main__":
    unittest.main()

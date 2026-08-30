from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import shutil
import stat
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import p7_04_persistent_access as p704
from arvectum_os_ref.identity import Identity
from p9_03_workspace import build_workspace_app
from workspace_app.access import P704AccessResolver, provision_workspace_grant
from workspace_app.company_asset_admission import resolve_exact_staged_material
from workspace_app.company_asset_governed_provider import provision_company_asset_admission_grant
from workspace_app.company_asset_library import CompanyAssetLibrary
from workspace_app.company_durable_executors import (
    DurableP1003CompanyAssetAdmissionExecutor,
    DurableP1005CompanyGeneratedOutputPromotionExecutor,
    build_durable_company_governed_executors,
)
from workspace_app.company_generated_output_governed_provider import (
    provision_company_generated_output_promotion_grant,
)
from workspace_app.company_generated_outputs import CompanyGeneratedOutputs
from workspace_app.company_governed_state_store import (
    CompanyGovernedStateError,
    CompanyGovernedStateStore,
)
from workspace_app.company_materials import CompanyMaterialsStore
from workspace_app.config import WorkspaceSettings


DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
REVIEW_POLICY = {
    "deletion_rule": "delete-only-through-governed-retention-process",
    "permitted_reuse": ["company-internal-document-generation"],
}
RAW_MARKER = "R34-RAW-CONTENT-MUST-NOT-ENTER-GOVERNED-METADATA"


def _docx_template(label: str = "r34") -> bytes:
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


def _canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


class R34DurableStateQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.organization = Identity("organization", "r34-d2-org", "platform")
        self.owner = Identity("principal", "r34-d2-owner", self.organization.value)
        p704.initialize_access_store(self.root, self.organization)
        p704.register_principal(self.root, self.owner, kind="human")
        p704.issue_credential(self.root, self.owner)
        provision_workspace_grant(self.root)
        self.access = P704AccessResolver(self.root).authorize()

        self.materials = CompanyMaterialsStore(self.root)
        self.asset_executor, self.promotion_executor = build_durable_company_governed_executors(
            self.root
        )
        self.assets = CompanyAssetLibrary(self.materials, self.asset_executor)
        self.asset_grant_id = provision_company_asset_admission_grant(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _settings(self) -> WorkspaceSettings:
        return WorkspaceSettings(
            runtime_root=self.root,
            public_origin="http://127.0.0.1:8769",
            bind_host="127.0.0.1",
            bind_port=8769,
            allowed_hosts=("127.0.0.1:8769",),
            organization_label="ООО «Арвектум»",
            actor_label="Owner operator",
            session_idle_seconds=1800,
            session_absolute_seconds=28800,
            allow_loopback_http=True,
        )

    def _stage_text(self, marker: str = RAW_MARKER) -> tuple[str, str, str]:
        raw_text = f"{marker}\nExact governed Company source.\n"
        staged = self.materials.stage(
            self.access,
            {
                "project_id": "COMPANY",
                "filename": "r34-source.txt",
                "media_type": "text/plain",
                "semantic_role": "company-standard-source",
                "classification": "internal",
                "purpose": "governed-company-operational-use",
                "rights": "company-internal-use",
                "retention_rule": "retain-while-current-plus-governed-history",
                "content_base64": base64.b64encode(raw_text.encode("utf-8")).decode("ascii"),
            },
        )["material"]
        material_id = str(staged["material_id"])
        version_id = str(staged["version_id"])
        self.assets.submit_review(
            self.access,
            material_id,
            version_id,
            {
                "deletion_rule": REVIEW_POLICY["deletion_rule"],
                "permitted_reuse": ["company-internal-reference-use"],
            },
        )
        return material_id, version_id, raw_text

    def _admit_text(self) -> tuple[str, str, str, object]:
        material_id, version_id, raw_text = self._stage_text()
        admitted = self.assets.admit(self.access, material_id, version_id)
        return material_id, version_id, raw_text, admitted

    def _stage_docx_and_promote(self) -> tuple[str, str, str, object, object]:
        staged = self.materials.stage(
            self.access,
            {
                "project_id": "COMPANY",
                "filename": "r34-template.docx",
                "media_type": DOCX_MEDIA_TYPE,
                "semantic_role": "document-template",
                "classification": "internal",
                "purpose": "company governed document generation",
                "rights": "company-internal-use",
                "retention_rule": "retain-while-current-plus-governed-history",
                "content_base64": base64.b64encode(_docx_template()).decode("ascii"),
            },
        )["material"]
        material_id = str(staged["material_id"])
        version_id = str(staged["version_id"])
        self.assets.submit_review(self.access, material_id, version_id, REVIEW_POLICY)
        admitted = self.assets.admit(self.access, material_id, version_id)
        generated = self.assets.generate_docx(
            self.access,
            {
                "material_id": material_id,
                "version_id": version_id,
                "title": "R34 reviewed Company document",
                "body": "Durable promotion qualification",
                "date": "2026-08-30",
            },
        )
        output_id = str(generated["output"]["output_id"])
        outputs = CompanyGeneratedOutputs(
            self.root,
            self.materials,
            self.asset_executor,
            self.promotion_executor,
        )
        outputs.review(
            self.access,
            output_id,
            {
                "disposition": "PromotionRequested",
                "document_title": "R34 reviewed Company document",
                "semantic_role": "company-project-document",
            },
        )
        promotion_grant_id = provision_company_generated_output_promotion_grant(self.root)
        promoted = outputs.promote(self.access, output_id)
        return material_id, version_id, output_id, admitted, (promoted, promotion_grant_id)

    def _copy_runtime_parts(self, destination: Path) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        for name in (
            "workspace-company-governed-state",
            "workspace-company-materials",
            "workspace-company-generated-output-reviews",
        ):
            source = self.root / name
            if source.exists():
                shutil.copytree(source, destination / name)

    def test_productive_workspace_uses_adr_0002_durable_pair(self) -> None:
        app = build_workspace_app(self._settings())
        admission = app.state.company_asset_library.admission
        outputs = app.state.company_generated_outputs

        self.assertIsInstance(admission, DurableP1003CompanyAssetAdmissionExecutor)
        self.assertIsInstance(
            outputs.promotion, DurableP1005CompanyGeneratedOutputPromotionExecutor
        )
        self.assertIs(outputs.asset_admission, admission)
        self.assertIs(outputs.promotion.asset_admission, admission)
        self.assertEqual(
            admission.governed_state_store.root,
            self.root / "workspace-company-governed-state",
        )

    def test_admission_survives_restart_and_lost_response_retry_does_not_replay(self) -> None:
        material_id, version_id, _, first = self._admit_text()
        first_state = self.asset_executor.state
        first_event = first_state.admitted_events[0].version_id
        starts_before = tuple(
            (self.root / "workspace-company-governed-state" / "admission" / "effects").glob(
                "*.started.json"
            )
        )
        self.assertEqual(len(starts_before), 1)

        restarted_asset, _ = build_durable_company_governed_executors(self.root)
        self.assertEqual(restarted_asset.state, first_state)
        self.assertEqual(restarted_asset.state.admitted_events[0].version_id, first_event)

        # A recovered committed result is history reconstruction, not a new
        # consequential operation. Removing the admission grant proves the
        # idempotent retry path does not execute the provider again.
        p704.revoke_grant(self.root, self.asset_grant_id)
        self.assertFalse(restarted_asset.available(self.access))
        restarted_library = CompanyAssetLibrary(CompanyMaterialsStore(self.root), restarted_asset)
        second = restarted_library.admit(self.access, material_id, version_id)

        self.assertEqual(second, first)
        self.assertEqual(len(restarted_asset.state.committed), 1)
        self.assertEqual(len(restarted_asset.state.admitted_events), 1)
        self.assertEqual(len(restarted_asset.state.attempts), 1)
        starts_after = tuple(
            (self.root / "workspace-company-governed-state" / "admission" / "effects").glob(
                "*.started.json"
            )
        )
        self.assertEqual(starts_after, starts_before)

        staged = resolve_exact_staged_material(
            store=CompanyMaterialsStore(self.root),
            access=self.access,
            material_id=material_id,
            version_id=version_id,
        )
        committed = restarted_asset.state.committed[0]
        artifact = committed.admitted_document.artifacts[0]
        self.assertEqual(artifact.integrity_ref, staged.content_sha256)
        self.assertEqual(artifact.content_ref, f"sha256:{staged.content_sha256}")
        self.assertIn(
            Identity("staged-material-version", version_id, self.organization.value),
            committed.admitted_document.canonical_record.provenance_refs,
        )

    def test_promotion_survives_restart_source_stays_transient_and_retry_does_not_replay(self) -> None:
        _, _, output_id, _, promotion_result = self._stage_docx_and_promote()
        first, promotion_grant_id = promotion_result
        original_asset_state = self.asset_executor.state
        original_promotion_state = self.promotion_executor.state
        _, source_manifest_before = self.materials.output_path(self.access, output_id)
        self.assertEqual(source_manifest_before["state"], "TransientOutput")
        starts_before = tuple(
            (self.root / "workspace-company-governed-state" / "promotion" / "effects").glob(
                "*.started.json"
            )
        )
        self.assertEqual(len(starts_before), 1)

        restarted_asset, restarted_promotion = build_durable_company_governed_executors(self.root)
        self.assertEqual(restarted_asset.state, original_asset_state)
        self.assertEqual(restarted_promotion.state, original_promotion_state)

        p704.revoke_grant(self.root, promotion_grant_id)
        self.assertFalse(restarted_promotion.available(self.access))
        restarted_materials = CompanyMaterialsStore(self.root)
        restarted_outputs = CompanyGeneratedOutputs(
            self.root,
            restarted_materials,
            restarted_asset,
            restarted_promotion,
        )
        second = restarted_outputs.promote(self.access, output_id)

        self.assertEqual(second, first)
        self.assertEqual(len(restarted_promotion.state.committed), 1)
        self.assertEqual(len(restarted_promotion.state.admitted_events), 1)
        self.assertEqual(len(restarted_promotion.state.attempts), 1)
        self.assertEqual(restarted_asset.state, original_asset_state)
        starts_after = tuple(
            (self.root / "workspace-company-governed-state" / "promotion" / "effects").glob(
                "*.started.json"
            )
        )
        self.assertEqual(starts_after, starts_before)
        _, source_manifest_after = restarted_materials.output_path(self.access, output_id)
        self.assertEqual(source_manifest_after["state"], "TransientOutput")
        self.assertFalse(source_manifest_after["canonical_authority"])

    def test_backup_restore_reconstructs_exact_governed_state_and_retained_bytes(self) -> None:
        material_id, version_id, output_id, _, _ = self._stage_docx_and_promote()
        original_admission = self.asset_executor.state
        original_promotion = self.promotion_executor.state
        original_staged = resolve_exact_staged_material(
            store=self.materials,
            access=self.access,
            material_id=material_id,
            version_id=version_id,
        )
        original_output_path, original_output_manifest = self.materials.output_path(
            self.access, output_id
        )
        original_output_digest = hashlib.sha256(original_output_path.read_bytes()).hexdigest()
        self.assertEqual(original_output_digest, original_output_manifest["output_sha256"])

        with tempfile.TemporaryDirectory() as restored_raw:
            restored_root = Path(restored_raw) / "restored-runtime"
            self._copy_runtime_parts(restored_root)

            restored_governed = CompanyGovernedStateStore(restored_root)
            self.assertEqual(restored_governed.load_admission_state(), original_admission)
            self.assertEqual(restored_governed.load_promotion_state(), original_promotion)

            restored_materials = CompanyMaterialsStore(restored_root)
            restored_staged = resolve_exact_staged_material(
                store=restored_materials,
                access=self.access,
                material_id=material_id,
                version_id=version_id,
            )
            self.assertEqual(restored_staged.content_sha256, original_staged.content_sha256)
            self.assertEqual(
                hashlib.sha256(restored_staged.blob_path.read_bytes()).hexdigest(),
                original_staged.content_sha256,
            )
            restored_output_path, restored_output_manifest = restored_materials.output_path(
                self.access, output_id
            )
            self.assertEqual(restored_output_manifest, original_output_manifest)
            self.assertEqual(
                hashlib.sha256(restored_output_path.read_bytes()).hexdigest(),
                original_output_digest,
            )

    def test_corrupt_partial_and_unknown_schema_records_fail_closed_while_stale_temp_is_ignored(self) -> None:
        self._admit_text()
        original_state = self.asset_executor.state

        with tempfile.TemporaryDirectory() as raw:
            copied = Path(raw) / "corrupt"
            self._copy_runtime_parts(copied)
            committed = next(
                (copied / "workspace-company-governed-state" / "admission" / "committed").glob(
                    "*.json"
                )
            )
            committed.write_bytes(b"not-json\n")
            with self.assertRaises(CompanyGovernedStateError):
                CompanyGovernedStateStore(copied).load_admission_state()

        with tempfile.TemporaryDirectory() as raw:
            copied = Path(raw) / "partial"
            self._copy_runtime_parts(copied)
            attempt = next(
                (copied / "workspace-company-governed-state" / "admission" / "attempts").glob(
                    "*.json"
                )
            )
            attempt.unlink()
            with self.assertRaises(CompanyGovernedStateError):
                CompanyGovernedStateStore(copied).load_admission_state()

        with tempfile.TemporaryDirectory() as raw:
            copied = Path(raw) / "unknown-schema"
            self._copy_runtime_parts(copied)
            directory = copied / "workspace-company-governed-state" / "admission" / "committed"
            committed = next(directory.glob("*.json"))
            envelope = json.loads(committed.read_text(encoding="utf-8"))
            envelope["schema_version"] = 999
            data = _canonical_json(envelope)
            replacement = directory / (
                f"{int(envelope['sequence']):08d}-{hashlib.sha256(data).hexdigest()[:24]}.json"
            )
            committed.unlink()
            replacement.write_bytes(data)
            with self.assertRaises(CompanyGovernedStateError):
                CompanyGovernedStateStore(copied).load_admission_state()

        with tempfile.TemporaryDirectory() as raw:
            copied = Path(raw) / "stale-temp"
            self._copy_runtime_parts(copied)
            stale = (
                copied
                / "workspace-company-governed-state"
                / "admission"
                / "committed"
                / ".tmp-governed-crash-leftover"
            )
            stale.write_text("partial unpublished bytes", encoding="utf-8")
            self.assertEqual(
                CompanyGovernedStateStore(copied).load_admission_state(), original_state
            )

    def test_symlinks_fail_closed_and_owner_only_permissions_are_enforced(self) -> None:
        self._admit_text()
        governed_root = self.root / "workspace-company-governed-state"

        if os.name != "nt":
            for path in governed_root.rglob("*"):
                mode = stat.S_IMODE(path.stat().st_mode)
                if path.is_dir():
                    self.assertEqual(mode, 0o700, path)
                elif path.is_file():
                    self.assertEqual(mode, 0o600, path)

        if not hasattr(os, "symlink"):
            self.skipTest("symlink support unavailable")

        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            real = base / "real-runtime"
            real.mkdir()
            link = base / "linked-runtime"
            try:
                link.symlink_to(real, target_is_directory=True)
            except OSError:
                self.skipTest("symlink creation unavailable")
            with self.assertRaises(CompanyGovernedStateError):
                CompanyGovernedStateStore(link)

        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "record-symlink"
            store = CompanyGovernedStateStore(root)
            target = root / "outside.json"
            target.write_text("{}", encoding="utf-8")
            record = (
                store.root
                / "admission"
                / "committed"
                / "00000000-000000000000000000000000.json"
            )
            try:
                record.symlink_to(target)
            except OSError:
                self.skipTest("record symlink creation unavailable")
            with self.assertRaises(CompanyGovernedStateError):
                store.load_admission_state()

    def test_governed_metadata_does_not_duplicate_raw_company_bytes(self) -> None:
        _, _, raw_text, _ = self._admit_text()
        governed_root = self.root / "workspace-company-governed-state"
        durable_bytes = b"".join(
            path.read_bytes() for path in governed_root.rglob("*.json") if path.is_file()
        )
        self.assertNotIn(raw_text.encode("utf-8"), durable_bytes)
        self.assertNotIn(RAW_MARKER.encode("utf-8"), durable_bytes)
        self.assertNotIn(b"content_base64", durable_bytes)


if __name__ == "__main__":
    unittest.main()

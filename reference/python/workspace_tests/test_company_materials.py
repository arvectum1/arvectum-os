from __future__ import annotations

import base64
import io
import json
import zipfile

import pytest

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.company_materials import CompanyMaterialsInputError, CompanyMaterialsStore


DOCX_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"


def _access() -> AccessContext:
    return AccessContext(
        organization=Identity("organization", "arvectum", "arvectum"),
        actor=Identity("principal", "owner", "arvectum"),
        principal_kind="human",
        credential_id="cred-owner",
        grant_id="grant-workspace",
    )


def _docx(text: str) -> bytes:
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


def test_staged_material_preserves_exact_version_lineage_and_governance_boundary(tmp_path) -> None:
    store = CompanyMaterialsStore(tmp_path)
    first = store.stage(_access(), _payload(_docx("{{TITLE}} — {{BODY}}")))
    material = first["material"]

    assert material["state"] == "StagedNonCanonical"
    assert material["canonical_authority"] is False
    assert first["governance"]["canonical_admission_available"] is False
    assert first["governance"]["canonical_state_changed"] is False

    second = store.stage(
        _access(),
        _payload(_docx("{{TITLE}} / {{DATE}} / {{BODY}}"), material_id=material["material_id"]),
    )
    second_version = second["material"]
    assert second_version["predecessor_version_id"] == material["version_id"]
    assert second_version["version_id"] != material["version_id"]
    assert second_version["content_sha256"] != material["content_sha256"]

    projection = store.project(_access())
    assert projection["product_contract"] == {"id": "P9.11-F11", "version": "0.1.0", "lifecycle": "Provisional"}
    assert projection["materials"][0]["latest_version_id"] == second_version["version_id"]
    assert len(projection["materials"][0]["versions"]) == 2


def test_exact_docx_version_generates_transient_output_with_provenance(tmp_path) -> None:
    store = CompanyMaterialsStore(tmp_path)
    staged = store.stage(_access(), _payload(_docx("{{TITLE}} | {{BODY}} | {{DATE}}")))["material"]
    result = store.generate_docx(
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
    assert output["state"] == "TransientOutput"
    assert output["canonical_authority"] is False
    assert output["source_version_id"] == staged["version_id"]
    assert output["source_sha256"] == staged["content_sha256"]
    assert result["governance"]["canonical_state_changed"] is False
    path, manifest = store.output_path(output["output_id"])
    assert path.is_file()
    assert manifest["output_sha256"] == output["output_sha256"]
    with zipfile.ZipFile(path, "r") as archive:
        xml = archive.read("word/document.xml").decode("utf-8")
    assert "Коммерческое предложение" in xml
    assert "Текст документа" in xml
    assert "26.08.2026" in xml


def test_generation_requires_supported_placeholder_and_exact_version(tmp_path) -> None:
    store = CompanyMaterialsStore(tmp_path)
    staged = store.stage(_access(), _payload(_docx("Обычный текст")))["material"]
    with pytest.raises(CompanyMaterialsInputError, match="placeholder"):
        store.generate_docx(
            _access(),
            {
                "material_id": staged["material_id"],
                "version_id": staged["version_id"],
                "title": "A",
                "body": "B",
                "date": "C",
            },
        )


def test_duplicate_version_and_unsafe_project_fail_closed(tmp_path) -> None:
    store = CompanyMaterialsStore(tmp_path)
    content = _docx("{{TITLE}}")
    staged = store.stage(_access(), _payload(content))["material"]
    with pytest.raises(CompanyMaterialsInputError, match="must differ"):
        store.stage(_access(), _payload(content, material_id=staged["material_id"]))

    invalid = _payload(content)
    invalid["project_id"] = "some-repo-name"
    with pytest.raises(CompanyMaterialsInputError, match="PORT-nnn"):
        store.stage(_access(), invalid)


def test_manifest_contains_no_encoded_content_or_authority_claim(tmp_path) -> None:
    store = CompanyMaterialsStore(tmp_path)
    raw = _docx("{{BODY}}")
    staged = store.stage(_access(), _payload(raw))["material"]
    manifest = json.loads((store.manifests / f"{staged['material_id']}.json").read_text(encoding="utf-8"))
    serialized = json.dumps(manifest)
    assert base64.b64encode(raw).decode("ascii") not in serialized
    assert '"state": "StagedNonCanonical"' in serialized
    assert '"validated_knowledge": false' in serialized

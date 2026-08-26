from pathlib import Path

path = Path("reference/python/workspace_app/company_materials.py")
text = path.read_text(encoding="utf-8")
old = r'''def _validate_actual_content(media_type: str, content: bytes) -> None:
    """Validate bytes independently from filename/extension/browser MIME claims."""

    if media_type == DOCX_MEDIA_TYPE:
        _office_entries(content, frozenset({"[Content_Types].xml", "word/document.xml"}))
        return
    if media_type == PPTX_MEDIA_TYPE:
        _office_entries(content, frozenset({"[Content_Types].xml", "ppt/presentation.xml"}))
        return
    if media_type == "application/pdf":
        if not content.startswith(b"%PDF-"):
            raise CompanyMaterialsInputError("material bytes do not match declared PDF type")
        return
    if media_type == "image/png":
        if not content.startswith(b"\x89PNG\r\n\x1a\n"):
            raise CompanyMaterialsInputError("material bytes do not match declared PNG type")
        return
    if media_type == "image/jpeg":
        if not content.startswith(b"\xff\xd8\xff"):
            raise CompanyMaterialsInputError("material bytes do not match declared JPEG type")
        return
    if media_type == "image/webp":
        if len(content) < 12 or content[:4] != b"RIFF" or content[8:12] != b"WEBP":
            raise CompanyMaterialsInputError("material bytes do not match declared WebP type")
        return
    if media_type in {"text/plain", "text/markdown"}:
        if b"\x00" in content:
            raise CompanyMaterialsInputError("text material contains NUL bytes")
        try:
            content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CompanyMaterialsInputError("text material must be valid UTF-8") from exc
        return
    raise CompanyMaterialsInputError("media_type is outside the bounded F11A allowlist")
'''
new = r'''def _require_prefix(content: bytes, prefix: bytes, media_label: str) -> None:
    if not content.startswith(prefix):
        raise CompanyMaterialsInputError(f"material bytes do not match declared {media_label} type")


def _validate_webp(content: bytes) -> None:
    if len(content) < 12 or content[:4] != b"RIFF" or content[8:12] != b"WEBP":
        raise CompanyMaterialsInputError("material bytes do not match declared WebP type")


def _validate_utf8_text(content: bytes) -> None:
    if b"\x00" in content:
        raise CompanyMaterialsInputError("text material contains NUL bytes")
    try:
        content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise CompanyMaterialsInputError("text material must be valid UTF-8") from exc


def _validate_actual_content(media_type: str, content: bytes) -> None:
    """Validate bytes independently from filename/extension/browser MIME claims."""

    office_required = {
        DOCX_MEDIA_TYPE: frozenset({"[Content_Types].xml", "word/document.xml"}),
        PPTX_MEDIA_TYPE: frozenset({"[Content_Types].xml", "ppt/presentation.xml"}),
    }.get(media_type)
    if office_required is not None:
        _office_entries(content, office_required)
        return

    prefix_rule = {
        "application/pdf": (b"%PDF-", "PDF"),
        "image/png": (b"\x89PNG\r\n\x1a\n", "PNG"),
        "image/jpeg": (b"\xff\xd8\xff", "JPEG"),
    }.get(media_type)
    if prefix_rule is not None:
        _require_prefix(content, *prefix_rule)
        return
    if media_type == "image/webp":
        _validate_webp(content)
        return
    if media_type in {"text/plain", "text/markdown"}:
        _validate_utf8_text(content)
        return
    raise CompanyMaterialsInputError("media_type is outside the bounded F11A allowlist")
'''
if text.count(old) != 1:
    raise SystemExit(f"expected exactly one material-validation block, found {text.count(old)}")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
Path("scripts/r32_refactor_material_validation.py").unlink(missing_ok=True)
Path(".github/workflows/r32-refactor-material-validation.yml").unlink(missing_ok=True)

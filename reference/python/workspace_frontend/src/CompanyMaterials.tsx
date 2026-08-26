import { useEffect, useMemo, useState } from "react";
import {
  fileToBase64,
  generateCompanyDocx,
  loadCompanyMaterials,
  loadCompanyPortfolio,
  stageCompanyMaterial,
} from "./f11Api";
import type { CompanyMaterialsProjection, GeneratedCompanyOutput, StagedMaterialVersion } from "./f11Types";
import { useWorkspaceLanguage } from "./i18n";
import "./CompanyWorkspace.css";

const DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";
const PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation";
const MAX_FILE_BYTES = 8 * 1024 * 1024;
const ACCEPTED_FILE_TYPES = ".docx,.pptx,.pdf,.png,.jpg,.jpeg,.webp,.txt,.md";
const ALLOWED_MEDIA_TYPES = new Set([
  DOCX,
  PPTX,
  "application/pdf",
  "image/png",
  "image/jpeg",
  "image/webp",
  "text/plain",
  "text/markdown",
]);

function declaredMediaType(file: File): string | null {
  if (ALLOWED_MEDIA_TYPES.has(file.type)) return file.type;
  const extension = file.name.toLowerCase().split(".").pop() ?? "";
  const byExtension: Record<string, string> = {
    docx: DOCX,
    pptx: PPTX,
    pdf: "application/pdf",
    png: "image/png",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    webp: "image/webp",
    txt: "text/plain",
    md: "text/markdown",
  };
  return byExtension[extension] ?? null;
}

type State =
  | { kind: "loading" }
  | { kind: "ready"; data: CompanyMaterialsProjection }
  | { kind: "error"; code: string };

function latestVersions(data: CompanyMaterialsProjection): StagedMaterialVersion[] {
  return data.materials.flatMap((item) => {
    const exact = item.versions.find((version) => version.version_id === item.latest_version_id);
    return exact ? [exact] : [];
  });
}

function MaterialCard({ material }: { material: { material_id: string; latest_version_id: string; versions: StagedMaterialVersion[] } }) {
  const { text } = useWorkspaceLanguage();
  return <article className="company-card">
    <header className="company-card-head"><div><p className="eyebrow">{material.material_id}</p><h2>{material.versions.at(-1)?.filename ?? material.material_id}</h2></div><span className="company-state company-state-staged">StagedNonCanonical</span></header>
    <p className="boundary-note">{text("Это staged evidence, а не канонически допущенный Document/Artifact.", "This is staged evidence, not a canonically admitted Document/Artifact.")}</p>
    <div className="company-versions">{material.versions.slice().reverse().map((version) => <details key={version.version_id} open={version.version_id === material.latest_version_id}><summary>{version.version_id === material.latest_version_id ? text("Текущая staged-версия", "Latest staged version") : text("Предыдущая версия", "Previous version")} · <code>{version.version_id}</code></summary><dl className="company-facts"><div><dt>{text("Проект", "Project")}</dt><dd>{version.project_id}</dd></div><div><dt>{text("Роль", "Role")}</dt><dd>{version.semantic_role}</dd></div><div><dt>{text("Классификация", "Classification")}</dt><dd>{version.classification}</dd></div><div><dt>{text("Назначение", "Purpose")}</dt><dd>{version.purpose}</dd></div><div><dt>{text("Права использования", "Rights")}</dt><dd>{version.rights}</dd></div><div><dt>{text("Retention", "Retention")}</dt><dd>{version.retention_rule}</dd></div><div><dt>{text("Получено", "Received")}</dt><dd>{version.received_at}</dd></div><div><dt>{text("Загрузил", "Uploader")}</dt><dd><code>{version.uploader}</code></dd></div><div><dt>SHA-256</dt><dd><code>{version.content_sha256}</code></dd></div><div><dt>{text("Предшественник", "Predecessor")}</dt><dd><code>{version.predecessor_version_id ?? "—"}</code></dd></div></dl></details>)}</div>
  </article>;
}

export function CompanyMaterials({ csrfToken }: { csrfToken: string }) {
  const { text } = useWorkspaceLanguage();
  const [state, setState] = useState<State>({ kind: "loading" });
  const [projectOptions, setProjectOptions] = useState<Array<{ id: string; label: string }>>([]);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [generated, setGenerated] = useState<GeneratedCompanyOutput | null>(null);

  const refresh = async () => {
    setState({ kind: "loading" });
    try {
      const data = await loadCompanyMaterials();
      setState({ kind: "ready", data });
    } catch (error) {
      setState({ kind: "error", code: error instanceof Error ? error.message : "COMPANY_MATERIALS_UNAVAILABLE" });
    }
  };

  useEffect(() => {
    void refresh();
    void loadCompanyPortfolio()
      .then((portfolio) => setProjectOptions(
        portfolio.projects
          .filter((project) => project.id.startsWith("PORT-"))
          .map((project) => ({ id: project.id, label: project.label })),
      ))
      .catch(() => setProjectOptions([]));
  }, []);

  const latest = useMemo(() => state.kind === "ready" ? latestVersions(state.data) : [], [state]);
  const docxVersions = useMemo(() => state.kind === "ready" ? state.data.materials.flatMap((item) => item.versions.filter((version) => version.media_type === DOCX)) : [], [state]);

  const submitStage = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage(null);
    setGenerated(null);
    const form = event.currentTarget;
    const data = new FormData(form);
    const file = data.get("file");
    if (!(file instanceof File) || file.size === 0 || file.size > MAX_FILE_BYTES) {
      setMessage(text("Выберите файл до 8 MiB.", "Choose a file up to 8 MiB."));
      return;
    }
    const mediaType = declaredMediaType(file);
    if (!mediaType) {
      setMessage(text("Этот тип файла не входит в безопасный F11A allowlist.", "This file type is outside the safe F11A allowlist."));
      return;
    }
    setBusy(true);
    try {
      const existing = String(data.get("material_id") ?? "").trim();
      const staged = await stageCompanyMaterial({
        ...(existing ? { material_id: existing } : {}),
        project_id: String(data.get("project_id") ?? "COMPANY"),
        filename: file.name,
        media_type: mediaType,
        semantic_role: String(data.get("semantic_role") ?? ""),
        classification: String(data.get("classification") ?? ""),
        purpose: String(data.get("purpose") ?? ""),
        rights: String(data.get("rights") ?? ""),
        retention_rule: String(data.get("retention_rule") ?? ""),
        content_base64: await fileToBase64(file),
      }, csrfToken);
      setMessage(text(`Сохранена staged-версия ${staged.version_id}. Канонический state не изменён.`, `Staged version ${staged.version_id} saved. Canonical state was not changed.`));
      form.reset();
      await refresh();
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "COMPANY_MATERIAL_STAGE_FAILED");
    } finally {
      setBusy(false);
    }
  };

  const submitGenerate = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setMessage(null);
    setGenerated(null);
    const data = new FormData(event.currentTarget);
    const composite = String(data.get("source_version") ?? "");
    const [materialId, versionId] = composite.split("::", 2);
    if (!materialId || !versionId) {
      setMessage(text("Выберите точную DOCX-версию шаблона.", "Choose an exact DOCX template version."));
      return;
    }
    setBusy(true);
    try {
      const output = await generateCompanyDocx({
        material_id: materialId,
        version_id: versionId,
        title: String(data.get("title") ?? ""),
        body: String(data.get("body") ?? ""),
        date: String(data.get("date") ?? ""),
      }, csrfToken);
      setGenerated(output);
      setMessage(text("Документ создан как Transient Output из точной версии шаблона.", "Document created as a Transient Output from the exact template version."));
    } catch (error) {
      setMessage(error instanceof Error ? error.message : "COMPANY_GENERATION_FAILED");
    } finally {
      setBusy(false);
    }
  };

  if (state.kind === "loading") return <section className="company-page" aria-live="polite">{text("Открываем материалы компании…", "Opening Company materials…")}</section>;
  if (state.kind === "error") return <section className="company-page" role="alert"><p className="eyebrow">F11A · Provisional 0.1.0</p><h1>{text("Материалы компании недоступны", "Company materials unavailable")}</h1><code>{state.code}</code><div><button type="button" onClick={() => void refresh()}>{text("Повторить", "Retry")}</button></div></section>;

  return <section className="company-page" aria-labelledby="company-materials-title">
    <header className="company-page-head"><p className="eyebrow">F11A · Product Contract Provisional 0.1.0</p><h1 id="company-materials-title">{text("Материалы компании", "Company materials")}</h1><p>{text("Здесь можно загрузить логотип, брендбук, исходник или шаблон, сохранить его точные staged-версии и использовать DOCX-шаблон для генерации документа.", "Upload a logo, brandbook, source, or template, preserve exact staged versions, and use an exact DOCX template version to generate a document.")}</p><p>{text("Первый безопасный allowlist: DOCX, PPTX, PDF, PNG, JPEG, WebP, TXT и MD. Фактическое содержимое проверяет сервер; SVG, macro-enabled Office и произвольные opaque-файлы сейчас отклоняются.", "Initial safe allowlist: DOCX, PPTX, PDF, PNG, JPEG, WebP, TXT, and MD. The server validates actual content; SVG, macro-enabled Office, and arbitrary opaque files are currently rejected.")}</p><p className="boundary-note"><strong>{text("Граница F11A:", "F11A boundary:")}</strong> {state.data.governance.reason} {text("Загрузка не выдаёт Authorization или Organizational Authority; generated Artifact остаётся Transient Output и не становится validated Knowledge.", "Upload grants neither Authorization nor Organizational Authority; a generated Artifact remains a Transient Output and does not become validated Knowledge.")}</p></header>

    <div className="company-two-column">
      <form className="company-form" onSubmit={(event) => void submitStage(event)}><h2>{text("Добавить материал или новую версию", "Add material or a new version")}</h2><label>{text("Новая версия существующего материала", "New version of existing material")}<select name="material_id" defaultValue=""><option value="">{text("Новый материал", "New material")}</option>{latest.map((version) => <option key={version.material_id} value={version.material_id}>{version.filename} · {version.material_id}</option>)}</select></label><label>{text("Проект", "Project")}<select name="project_id" defaultValue="COMPANY"><option value="COMPANY">{text("Компания в целом", "Company-wide")}</option>{projectOptions.map((project) => <option key={project.id} value={project.id}>{project.id} · {project.label}</option>)}</select></label><label>{text("Файл", "File")}<input name="file" type="file" accept={ACCEPTED_FILE_TYPES} required /></label><label>{text("Семантическая роль", "Semantic role")}<input name="semantic_role" required maxLength={96} placeholder="document-template / brandbook / logo / source" /></label><label>{text("Классификация", "Classification")}<input name="classification" required maxLength={96} defaultValue="internal" /></label><label>{text("Назначение", "Purpose")}<input name="purpose" required maxLength={240} /></label><label>{text("Права использования", "Rights")}<input name="rights" required maxLength={240} defaultValue="company-internal-use" /></label><label>{text("Retention rule", "Retention rule")}<input name="retention_rule" required maxLength={240} defaultValue="until-replaced-or-explicit-deletion" /></label><button type="submit" disabled={busy}>{busy ? text("Сохраняем…", "Saving…") : text("Сохранить staged-версию", "Save staged version")}</button></form>

      <form className="company-form" onSubmit={(event) => void submitGenerate(event)}><h2>{text("Создать DOCX по шаблону", "Generate DOCX from template")}</h2><p>{text("В DOCX-шаблоне используйте цельные placeholders {{TITLE}}, {{BODY}}, {{DATE}}. Можно использовать один или несколько.", "Use contiguous placeholders {{TITLE}}, {{BODY}}, {{DATE}} in the DOCX template. One or more may be used.")}</p><label>{text("Точная версия шаблона", "Exact template version")}<select name="source_version" required defaultValue=""><option value="" disabled>{text("Выберите версию", "Choose version")}</option>{docxVersions.map((version) => <option key={version.version_id} value={`${version.material_id}::${version.version_id}`}>{version.filename} · {version.version_id}</option>)}</select></label><label>{text("Заголовок", "Title")}<input name="title" required maxLength={320} /></label><label>{text("Текст", "Body")}<textarea name="body" required maxLength={6000} rows={9} /></label><label>{text("Дата", "Date")}<input name="date" required maxLength={80} defaultValue={new Date().toLocaleDateString("ru-RU")} /></label><button type="submit" disabled={busy || docxVersions.length === 0}>{text("Создать transient DOCX", "Generate transient DOCX")}</button>{docxVersions.length === 0 ? <p className="boundary-note">{text("Сначала загрузите DOCX-шаблон.", "Upload a DOCX template first.")}</p> : null}{generated ? <div className="company-output"><strong>Transient Output</strong><p><code>{generated.output.output_id}</code></p><p>{text("Source version", "Source version")}: <code>{generated.output.source_version_id}</code></p><a href={generated.output.download_href}>{text("Скачать DOCX", "Download DOCX")}</a></div> : null}</form>
    </div>

    {message ? <p className="company-message" role="status">{message}</p> : null}
    <section aria-labelledby="materials-list-title"><h2 id="materials-list-title">{text("Сохранённые staged-материалы", "Saved staged materials")}</h2>{state.data.materials.length ? <div className="company-grid">{state.data.materials.map((material) => <MaterialCard material={material} key={material.material_id} />)}</div> : <p>{text("Материалов пока нет. Первая реальная загрузка станет owner evidence для F11A, но сама по себе не будет canonical admission.", "No materials yet. The first real upload becomes owner evidence for F11A but is not canonical admission by itself.")}</p>}</section>
  </section>;
}

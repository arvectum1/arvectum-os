import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { CompanyMaterials } from "./CompanyMaterials";
import { LanguageProvider } from "./i18n";
import type { CompanyMaterialsProjection, CompanyPortfolioProjection, GeneratedCompanyOutput, StagedMaterialVersion } from "./f11Types";

const DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";

const portfolio: CompanyPortfolioProjection = {
  schema: "arvectum.workspace.company-portfolio/1",
  generated_at: "2026-08-26T20:00:00Z",
  product_contract: { id: "P9.11-F11", version: "0.1.0", lifecycle: "Provisional" },
  projection: {
    derived: true,
    canonical_authority: false,
    read_only: true,
    roadmap_write_available: false,
    remote_execution_available: false,
    chat_or_model_memory_used_as_authority: false,
    visibility_implies_permission: false,
  },
  scope: {
    organization_resolved_server_side: true,
    actor_resolved_server_side: true,
    cross_organization_aggregation: false,
  },
  projects: [],
};

const templateVersion: StagedMaterialVersion = {
  material_id: "MAT-template0001",
  version_id: "MV-template00000001",
  predecessor_version_id: null,
  organization: "organization:arvectum@platform",
  project_id: "PORT-003",
  filename: "Arvectum-template.docx",
  media_type: DOCX,
  semantic_role: "document-template",
  classification: "internal",
  purpose: "standard document template",
  rights: "company-internal-use",
  retention_rule: "until-replaced-or-explicit-deletion",
  uploader: "principal:owner@arvectum",
  received_at: "2026-08-26T20:00:00Z",
  content_sha256: "a".repeat(64),
  size_bytes: 1024,
  state: "StagedNonCanonical",
  canonical_authority: false,
  validated_knowledge: false,
};

const baseMaterials: CompanyMaterialsProjection = {
  schema: "arvectum.workspace.company-materials/1",
  generated_at: "2026-08-26T20:00:00Z",
  product_contract: { id: "P9.11-F11", version: "0.1.0", lifecycle: "Provisional" },
  scope: {
    organization_resolved_server_side: true,
    actor_resolved_server_side: true,
    cross_organization_access: false,
  },
  materials: [],
  governance: {
    state: "StagedNonCanonical",
    canonical_admission_available: false,
    canonical_state_changed: false,
    organizational_authority_provided_by_upload: false,
    validated_knowledge_created: false,
    reason: "Receipt is staged and non-canonical.",
  },
};

const materialsWithTemplate: CompanyMaterialsProjection = {
  ...baseMaterials,
  materials: [{
    material_id: templateVersion.material_id,
    latest_version_id: templateVersion.version_id,
    versions: [templateVersion],
  }],
};

const generated: GeneratedCompanyOutput = {
  schema: "arvectum.workspace.company-generated-output/1",
  output: {
    output_id: "OUT-generated0001",
    state: "TransientOutput",
    organization: "organization:arvectum@platform",
    project_id: "PORT-003",
    created_at: "2026-08-26T20:01:00Z",
    created_by: "principal:owner@arvectum",
    source_material_id: templateVersion.material_id,
    source_version_id: templateVersion.version_id,
    source_sha256: templateVersion.content_sha256,
    output_sha256: "b".repeat(64),
    media_type: DOCX,
    filename: "generated-OUT-generated0001.docx",
    canonical_authority: false,
    validated_knowledge: false,
    download_href: "/api/app/v1/company-materials/outputs/OUT-generated0001/download",
  },
  governance: {
    generated_artifact_state: "TransientOutput",
    canonical_state_changed: false,
    exact_source_version_pinned: true,
  },
};

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

function renderMaterials(materials: CompanyMaterialsProjection) {
  const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.includes("company/portfolio")) {
      return new Response(JSON.stringify(portfolio), { status: 200, headers: { "Content-Type": "application/json" } });
    }
    if (url.endsWith("/company-materials/generate") && init?.method === "POST") {
      return new Response(JSON.stringify(generated), { status: 200, headers: { "Content-Type": "application/json" } });
    }
    return new Response(JSON.stringify(materials), { status: 200, headers: { "Content-Type": "application/json" } });
  });
  vi.stubGlobal("fetch", fetchMock);
  render(<LanguageProvider initialLanguage="ru"><CompanyMaterials csrfToken="csrf" /></LanguageProvider>);
  return fetchMock;
}

describe("F11A real owner template journey remediation", () => {
  it("uses a fixed material-type list with an explicit Other escape hatch", async () => {
    renderMaterials(baseMaterials);
    expect(await screen.findByRole("heading", { name: "Материалы компании" })).toBeTruthy();

    const select = screen.getByLabelText("Тип материала") as HTMLSelectElement;
    expect(Array.from(select.options).map((option) => option.textContent)).toEqual([
      "Выберите тип",
      "Шаблон документа",
      "Брендбук",
      "Логотип",
      "Исходный материал",
      "Другое",
    ]);

    fireEvent.change(select, { target: { value: "other" } });
    expect(screen.getByLabelText("Другой тип")).toBeTruthy();
  });

  it("exposes generated DOCX download as a protected action instead of an unguarded API link", async () => {
    renderMaterials(materialsWithTemplate);
    expect(await screen.findByRole("heading", { name: "Материалы компании" })).toBeTruthy();

    fireEvent.change(screen.getByLabelText("Точная версия шаблона"), {
      target: { value: `${templateVersion.material_id}::${templateVersion.version_id}` },
    });
    fireEvent.change(screen.getByLabelText("Заголовок"), { target: { value: "Тестовый документ" } });
    fireEvent.change(screen.getByLabelText("Текст"), { target: { value: "Проверка owner journey" } });
    fireEvent.change(screen.getByLabelText("Дата"), { target: { value: "26.08.2026" } });
    fireEvent.click(screen.getByRole("button", { name: "Создать transient DOCX" }));

    expect(await screen.findByText("Transient Output")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Скачать DOCX" })).toBeTruthy();
    expect(screen.queryByRole("link", { name: "Скачать DOCX" })).toBeNull();
  });
});

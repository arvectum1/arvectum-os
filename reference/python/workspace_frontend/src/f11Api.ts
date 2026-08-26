import type {
  CompanyMaterialsProjection,
  CompanyPortfolioProjection,
  GeneratedCompanyOutput,
  StagedMaterialVersion,
} from "./f11Types";

const RELEASE_ID = __ARVECTUM_WORKSPACE_RELEASE__;

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("X-Arvectum-Workspace-Release", RELEASE_ID);
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(path, { ...init, headers, credentials: "same-origin" });
  if (!response.ok) {
    let code = `HTTP_${response.status}`;
    try {
      const payload = await response.json() as { code?: string; detail?: string };
      code = payload.code ?? payload.detail ?? code;
    } catch {
      // Keep a minimized error when the server did not return JSON.
    }
    throw new Error(code);
  }
  return await response.json() as T;
}

export function loadCompanyPortfolio(forceRefresh = false): Promise<CompanyPortfolioProjection> {
  return request<CompanyPortfolioProjection>(forceRefresh ? "/api/app/v1/company/portfolio?refresh=true" : "/api/app/v1/company/portfolio");
}

export function loadCompanyMaterials(): Promise<CompanyMaterialsProjection> {
  return request<CompanyMaterialsProjection>("/api/app/v1/company-materials");
}

export async function stageCompanyMaterial(
  input: {
    material_id?: string;
    project_id: string;
    filename: string;
    media_type: string;
    semantic_role: string;
    classification: string;
    purpose: string;
    rights: string;
    retention_rule: string;
    content_base64: string;
  },
  csrfToken: string,
): Promise<StagedMaterialVersion> {
  const response = await request<{ material: StagedMaterialVersion }>("/api/app/v1/company-materials", {
    method: "POST",
    headers: { "X-Arvectum-CSRF": csrfToken },
    body: JSON.stringify(input),
  });
  return response.material;
}

export function generateCompanyDocx(
  input: { material_id: string; version_id: string; title: string; body: string; date: string },
  csrfToken: string,
): Promise<GeneratedCompanyOutput> {
  return request<GeneratedCompanyOutput>("/api/app/v1/company-materials/generate", {
    method: "POST",
    headers: { "X-Arvectum-CSRF": csrfToken },
    body: JSON.stringify(input),
  });
}

export async function fileToBase64(file: File): Promise<string> {
  const bytes = new Uint8Array(await file.arrayBuffer());
  let binary = "";
  const chunk = 0x8000;
  for (let offset = 0; offset < bytes.length; offset += chunk) {
    binary += String.fromCharCode(...bytes.subarray(offset, offset + chunk));
  }
  return btoa(binary);
}
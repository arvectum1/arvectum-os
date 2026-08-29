import type { CompanyGeneratedOutputsProjection, GeneratedOutputDisposition } from "./p10_05Types";

const RELEASE_ID = __ARVECTUM_WORKSPACE_RELEASE__;
const RELEASE_HEADER = "X-Arvectum-Workspace-Release";

async function responseError(response: Response): Promise<Error> {
  let code = `HTTP_${response.status}`;
  try {
    const payload = await response.json() as { code?: string; detail?: string };
    code = payload.code ?? payload.detail ?? code;
  } catch {
    // Keep the minimized transport error.
  }
  return new Error(code);
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set(RELEASE_HEADER, RELEASE_ID);
  if (init.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  const response = await fetch(path, { ...init, headers, credentials: "same-origin" });
  if (!response.ok) throw await responseError(response);
  return await response.json() as T;
}

function outputPath(outputId: string, action: string): string {
  return `/api/app/v1/company-generated-outputs/${encodeURIComponent(outputId)}/${action}`;
}

export function loadCompanyGeneratedOutputs(): Promise<CompanyGeneratedOutputsProjection> {
  return request<CompanyGeneratedOutputsProjection>("/api/app/v1/company-generated-outputs");
}

export async function reviewCompanyGeneratedOutput(
  outputId: string,
  input:
    | { disposition: Extract<GeneratedOutputDisposition, "Rejected">; reason: string }
    | { disposition: Extract<GeneratedOutputDisposition, "KeepTransient"> }
    | {
        disposition: Extract<GeneratedOutputDisposition, "PromotionRequested">;
        document_title: string;
        semantic_role: string;
      },
  csrfToken: string,
): Promise<void> {
  await request(outputPath(outputId, "review"), {
    method: "POST",
    headers: { "X-Arvectum-CSRF": csrfToken },
    body: JSON.stringify(input),
  });
}

export async function promoteCompanyGeneratedOutput(outputId: string, csrfToken: string): Promise<void> {
  await request(outputPath(outputId, "promote"), {
    method: "POST",
    headers: { "X-Arvectum-CSRF": csrfToken },
  });
}

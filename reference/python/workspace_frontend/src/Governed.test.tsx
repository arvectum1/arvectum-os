import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Governed } from "./Governed";
import { LanguageProvider } from "./i18n";
import type { GovernedExperienceProjection, GovernedPreflightResult } from "./types";

const projection: GovernedExperienceProjection = {
  schema: "arvectum.workspace.governed-experience/1", generated_at: "2026-08-21T12:00:00Z",
  presentation: { title: "EIS document governed execution", summary: "A real retained execution/provenance chain for an EIS-backed governed document.", source: "ЕИС / zakupki.gov.ru", authority_mode: "External Reference", authority_scope: "EIS exact notice attachment evidence", validation_status: "CAP-004 reconstruction complete" },
  execution: { status: "Waiting", meaning: "Required action decisions are still unresolved, so the execution remains fail-closed.", waiting_decisions: ["Authorization", "Organizational Authority", "Data Governance", "Consequential Approval"], technical_identity_available: true },
  decisions: [
    { name: "Authorization", state: "Waiting", basis: "No action-specific authorization decision supplied." },
    { name: "Organizational Authority", state: "Waiting", basis: "Technical access supplies no Organizational Authority." },
    { name: "Data Governance", state: "Waiting", basis: "No purpose-specific data-governance decision supplied." },
    { name: "Consequential Approval", state: "Waiting", basis: "The browser/session/button is not approval." },
  ],
  action: { kind: "governed-preflight", label: "Run governed preflight", available: true, consequential: false, canonical_mutation_requested: false, external_effect_requested: false, authority_provided: false, explanation: "Re-check the real retained execution and all four governance gates now." },
  technical: { release_sha: "a".repeat(40), source_subject: "document-subject/eis-real", source_version: "document-version/eis-real-v1", execution_subject: "execution-subject/eis-real", execution_version: "execution-version/eis-real-v5", event_version: "event-version/eis-real-v1", checkpoint_id: "checkpoint-real", provenance_refs: ["event-version/eis-real-v1"] },
  scope: { organization_resolved_server_side: true, actor_resolved_server_side: true, current_access_revalidated: true, organizational_authority_provided: false, visibility_implies_permission: false },
};
const result: GovernedPreflightResult = { schema: "arvectum.workspace.governed-preflight-result/1", recorded_at: "2026-08-21T12:01:00Z", outcome: "Waiting", status_text: "Preflight executed: WAITING / fail-closed.", canonical_mutation_requested: false, canonical_mutation_performed: false, external_effect_requested: false, external_effect_performed: false, organizational_authority_provided: false, consequential_approval_provided: false, evidence: { classification: "owner-local non-canonical proof evidence", sha256: "b".repeat(64) } };

function renderRu() { return render(<LanguageProvider initialLanguage="ru"><Governed csrfToken="csrf-test" /></LanguageProvider>); }
afterEach(() => { cleanup(); vi.unstubAllGlobals(); window.history.replaceState({}, "", "/"); });

describe("P9.11 F08 governed task journey", () => {
  it("uses Russian owner meaning, preserves canonical gates on demand, and returns to the focused task", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), { status: 200, headers: { "Content-Type": "application/json" } })));
    window.history.replaceState({}, "", "/governed?focus=11111111111111111111");
    renderRu();
    expect(await screen.findByRole("heading", { name: "Выполнение остановлено" })).toBeTruthy();
    for (const label of ["Доступ к действию", "Полномочия организации", "Разрешение на использование данных", "Финальное подтверждение действия"]) expect(screen.getByText(label)).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "EIS document governed execution" })).toBeNull();
    expect(screen.getByText("Техническое основание").closest("details")?.open).toBe(false);
    expect(screen.getByRole("link", { name: "Назад к задаче" }).getAttribute("href")).toBe("/my-work?focus=11111111111111111111");
    fireEvent.click(screen.getByText("Техническое основание"));
    expect(screen.getByText("Authorization")).toBeTruthy();
    expect(screen.getByText(/No action-specific authorization/)).toBeTruthy();
    expect(screen.getByText("execution-version/eis-real-v5")).toBeTruthy();
    expect(screen.getAllByText("event-version/eis-real-v1")).toHaveLength(2);
  });

  it("shows a safe re-check only for the exact non-consequential projection and reports an unchanged result", async () => {
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => new Response(JSON.stringify(init?.method === "POST" ? result : projection), { status: 200, headers: { "Content-Type": "application/json" } }));
    vi.stubGlobal("fetch", fetchMock);
    renderRu();
    expect(await screen.findByText("Безопасная проверка")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Run governed preflight" })).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Перепроверить состояние" }));
    expect(await screen.findByText("Проверка завершена")).toBeTruthy();
    expect(screen.getByText(/Ничего не изменено/)).toBeTruthy();
    expect(screen.queryByRole("button", { name: /одобрить|разрешить|делегировать/i })).toBeNull();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2));
    expect(fetchMock.mock.calls[1][1]?.method).toBe("POST");
  });

  it("fails closed when any action safety flag drifts", async () => {
    const unsafe = { ...projection, action: { ...projection.action, external_effect_requested: true } } as unknown as GovernedExperienceProjection;
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(unsafe), { status: 200, headers: { "Content-Type": "application/json" } })));
    renderRu();
    expect(await screen.findByText("Безопасность действия не подтверждена")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Перепроверить состояние" })).toBeNull();
    expect(screen.queryByText("Безопасная проверка")).toBeNull();
  });

  it("withholds the re-check and stopped-state claim when execution or gates no longer wait", async () => {
    const changed = { ...projection, execution: { ...projection.execution, status: "Ready" }, decisions: projection.decisions.map((decision) => ({ ...decision, state: "Allow" })) };
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(changed), { status: 200, headers: { "Content-Type": "application/json" } })));
    renderRu();
    expect(await screen.findByRole("heading", { name: "Выполнение требует проверки" })).toBeTruthy();
    expect(screen.getByText("Ready")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Перепроверить состояние" })).toBeNull();
  });

  it("does not describe partially resolved gates as four missing decisions", async () => {
    const partial = { ...projection, decisions: projection.decisions.map((decision, index) => index < 2 ? { ...decision, state: "Allow" } : decision) };
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(partial), { status: 200, headers: { "Content-Type": "application/json" } })));
    renderRu();
    expect(await screen.findByRole("heading", { name: "Выполнение требует проверки" })).toBeTruthy();
    expect(screen.getAllByText("Allow")).toHaveLength(2);
    expect(screen.queryByText(/не хватает 4 обязательных решений/)).toBeNull();
    expect(screen.queryByRole("button", { name: "Перепроверить состояние" })).toBeNull();
  });

  it("withholds protected execution detail when the source cannot be revalidated", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify({ detail: "GOVERNED_EXPERIENCE_UNAVAILABLE" }), { status: 503, headers: { "Content-Type": "application/json" } })));
    renderRu();
    expect(await screen.findByRole("heading", { name: "Проверка сейчас недоступна." })).toBeTruthy();
    expect(screen.queryByText("execution-version/eis-real-v5")).toBeNull();
  });
});

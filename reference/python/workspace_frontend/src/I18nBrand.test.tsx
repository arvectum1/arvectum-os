import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LanguageProvider } from "./i18n";
import { Shell } from "./Shell";
import type { MyWorkProjection, WorkspaceContext } from "./types";

const context: WorkspaceContext = {
  schema: "arvectum.workspace.shell-context/1",
  release: { id: "p9.11.1", app_api_contract: "10", classification: "bounded-internal-provisional", public_api: false },
  organization: { label: "ООО «Арвектум»", scope_resolved_server_side: true },
  actor: { label: "Owner operator", attributable: true, scope_resolved_server_side: true, authentication_source: "P7.04 owner-local credential" },
  session: { csrf_token: "test-only", bounded: true, revocable: true, authority_provided: false },
  navigation: [
    { id: "home", label: "Home", href: "/", availability: "available" },
    { id: "my-work", label: "My Work", href: "/my-work", availability: "available" },
    { id: "dogfooding", label: "Dogfooding", href: "/dogfooding", availability: "available" },
  ],
  data_governance: { protected_read_revalidated: true, response_minimized: "shell-context-only", canonical_state_in_browser: false },
};

const projection: MyWorkProjection = {
  schema: "arvectum.workspace.my-work/1",
  generated_at: "2026-08-23T08:00:00Z",
  projection: { derived: true, canonical_authority: false, organizational_authority_provided: false, consequential_action_available: false, visibility_implies_permission: false },
  scope: { organization_resolved_server_side: true, actor_resolved_server_side: true, denied_item_counts_exposed: false },
  health: { state: "fresh", code: "OK", message: "Current.", observed_at: "2026-08-23T08:00:00Z", heartbeat_age_seconds: 1 },
  items: [],
};

afterEach(() => { cleanup(); vi.unstubAllGlobals(); window.history.replaceState({}, "", "/"); });

describe("P9.11 RU-first branded Workspace", () => {
  it("uses Russian by default and switches to English without browser storage", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), { status: 200, headers: { "Content-Type": "application/json" } })));
    render(<LanguageProvider><Shell context={context} onLogout={() => undefined} /></LanguageProvider>);

    expect(document.documentElement.lang).toBe("ru");
    expect(screen.getByRole("link", { name: "Главная" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Моя работа" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Обратная связь" })).toBeTruthy();
    expect(screen.getByText("Контекст организации готов к работе.")).toBeTruthy();
    expect(screen.getByText("AV")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "EN" }));
    expect(document.documentElement.lang).toBe("en");
    expect(screen.getByRole("link", { name: "Home" })).toBeTruthy();
    expect(screen.getByText("Your organization context is established.")).toBeTruthy();
  });
});

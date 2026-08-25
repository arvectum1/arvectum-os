import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { LanguageProvider } from "./i18n";
import { Shell } from "./Shell";
import type { MyWorkProjection, WorkspaceContext } from "./types";

const context: WorkspaceContext = {
  schema: "arvectum.workspace.shell-context/1",
  release: { id: "p9.11.2", app_api_contract: "11", classification: "bounded-internal-provisional", public_api: false },
  organization: { label: "ООО «Арвектум»", scope_resolved_server_side: true },
  actor: { label: "Owner operator", attributable: true, scope_resolved_server_side: true, authentication_source: "P7.04 owner-local credential" },
  session: { csrf_token: "test-only", bounded: true, revocable: true, authority_provided: false },
  navigation: [
    { id: "today", label: "Today", href: "/", availability: "available" },
    { id: "work", label: "Work", href: "/work", availability: "available" },
    { id: "information", label: "Information", href: "/information", availability: "available" },
    { id: "copilot", label: "Arvectum AI", href: "/copilot", availability: "available" },
    { id: "system", label: "System", href: "/system", availability: "available" },
  ],
  data_governance: { protected_read_revalidated: true, response_minimized: "shell-context-only", canonical_state_in_browser: false },
};
const projection: MyWorkProjection = { schema: "arvectum.workspace.my-work/1", generated_at: "2026-08-23T08:00:00Z", projection: { derived: true, canonical_authority: false, organizational_authority_provided: false, consequential_action_available: false, visibility_implies_permission: false }, scope: { organization_resolved_server_side: true, actor_resolved_server_side: true, denied_item_counts_exposed: false }, health: { state: "fresh", code: "OK", message: "Current.", observed_at: "2026-08-23T08:00:00Z", heartbeat_age_seconds: 1 }, items: [] };

afterEach(() => { cleanup(); vi.unstubAllGlobals(); window.history.replaceState({}, "", "/"); });

describe("P9.11 owner-first Workspace", () => {
  it("uses exactly the owner-oriented Russian primary navigation and today actions", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), { status: 200, headers: { "Content-Type": "application/json" } })));
    render(<LanguageProvider><Shell context={context} onLogout={() => undefined} /></LanguageProvider>);
    expect(document.documentElement.lang).toBe("ru");
    expect(screen.getAllByRole("link").filter((link) => ["Сегодня", "Работа", "Информация", "Arvectum AI", "Система"].includes(link.textContent ?? "")).map((link) => link.textContent)).toEqual(["Сегодня", "Работа", "Информация", "Arvectum AI", "Система"]);
    expect(screen.queryByRole("link", { name: "Записи" })).toBeNull();
    expect(screen.queryByRole("link", { name: "Документы" })).toBeNull();
    expect(screen.queryByRole("link", { name: "Знания" })).toBeNull();
    expect(screen.getByRole("heading", { name: "Вот что сейчас требует внимания" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Открыть работу" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Найти информацию" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Спросить Arvectum" })).toBeTruthy();
  });

  it("switches to English without browser storage", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), { status: 200, headers: { "Content-Type": "application/json" } })));
    render(<LanguageProvider><Shell context={context} onLogout={() => undefined} /></LanguageProvider>);
    fireEvent.click(screen.getByRole("button", { name: "EN" }));
    expect(document.documentElement.lang).toBe("en");
    expect(screen.getByRole("link", { name: "Today" })).toBeTruthy();
    expect(screen.getByText("Here is what needs attention now")).toBeTruthy();
  });

  it("renders the real Arvectum SVG logo instead of the AV placeholder", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), { status: 200, headers: { "Content-Type": "application/json" } })));
    render(<LanguageProvider><Shell context={context} onLogout={() => undefined} /></LanguageProvider>);
    const logo = screen.getByRole("img", { name: "Arvectum" });
    expect(logo).toBeTruthy();
    const src = logo.getAttribute("src") ?? "";
    expect(src.length > 0).toBe(true);
    expect(screen.queryByText("AV")).toBeNull();
    expect(screen.queryByText("Arvectum", { selector: ".brand-copy strong" })).toBeNull();
  });

  it("shows the OS product identifier without duplicating the Arvectum wordmark", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(projection), { status: 200, headers: { "Content-Type": "application/json" } })));
    render(<LanguageProvider><Shell context={context} onLogout={() => undefined} /></LanguageProvider>);
    const brand = screen.getByLabelText("Arvectum OS");
    expect(brand.querySelector(".brand-product")?.textContent).toBe("OS");
    const arvectumWords = brand.querySelectorAll("strong");
    expect(arvectumWords.length).toBe(0);
  });

  it("groups legacy product and technical deep routes under Work and System", () => {
    window.history.replaceState({}, "", "/products/tender-operator");
    const { unmount } = render(<LanguageProvider initialLanguage="en"><Shell context={context} onLogout={() => undefined} /></LanguageProvider>);
    expect(screen.getByRole("link", { name: "Work" }).getAttribute("aria-current")).toBe("page");
    unmount();

    window.history.replaceState({}, "", "/governed");
    render(<LanguageProvider initialLanguage="en"><Shell context={context} onLogout={() => undefined} /></LanguageProvider>);
    expect(screen.getByRole("link", { name: "System" }).getAttribute("aria-current")).toBe("page");
  });
});

import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";
import type { CopilotAnswer, WorkspaceContext } from "./types";

const context: WorkspaceContext = {
  schema: "arvectum.workspace.shell-context/1",
  release: { id: "p9.10.2", app_api_contract: "9", classification: "bounded-internal-provisional", public_api: false },
  organization: { label: "ООО «Арвектум»", scope_resolved_server_side: true },
  actor: { label: "Owner operator", attributable: true, scope_resolved_server_side: true, authentication_source: "P7.04 owner-local credential" },
  session: { csrf_token: "csrf-p908", bounded: true, revocable: true, authority_provided: false },
  navigation: [
    { id: "home", label: "Home", href: "/", availability: "available" },
    { id: "my-work", label: "My Work", href: "/my-work", availability: "available" },
    { id: "search", label: "Search", href: "/search", availability: "available" },
    { id: "records", label: "Records", href: "/records", availability: "available" },
    { id: "documents", label: "Documents", href: "/documents", availability: "available" },
    { id: "knowledge", label: "Knowledge", href: "/knowledge", availability: "available" },
    { id: "copilot", label: "Ask Arvectum", href: "/copilot", availability: "available" },
    { id: "governed", label: "Governed actions", href: "/governed", availability: "available" },
    { id: "products", label: "Products", href: "/products", availability: "available" },
  ],
  data_governance: { protected_read_revalidated: true, response_minimized: "shell-context-only", canonical_state_in_browser: false },
};

const answer: CopilotAnswer = {
  schema: "arvectum.workspace.copilot-answer/2",
  generated_at: "2026-08-22T00:00:00Z",
  claims: [
    {
      kind: "source-context",
      text: "A governed External Reference to the EIS notice is available. Authority/source: External Reference · ЕИС / zakupki.gov.ru.",
      source_refs: ["object:aaaaaaaaaaaaaaaaaaaa"],
    },
    {
      kind: "synthesis",
      text: "The retained evidence supports using EIS as the authoritative source; inspect it before consequential reliance.",
      source_refs: ["object:aaaaaaaaaaaaaaaaaaaa"],
    },
    {
      kind: "uncertainty",
      text: "Freshness and reconciliation limitations must still be checked at the source boundary.",
      source_refs: ["object:aaaaaaaaaaaaaaaaaaaa"],
    },
  ],
  sources: [
    {
      id: "object:aaaaaaaaaaaaaaaaaaaa",
      label: "EIS notice 0344100006426000005",
      summary: "A governed External Reference to the EIS notice is available.",
      authority: "External Reference · ЕИС / zakupki.gov.ru",
      freshness: "fresh",
      semantic_role: "Document",
      knowledge_role: null,
      open_href: "/objects/aaaaaaaaaaaaaaaaaaaa",
      inspectable_in_workspace: true,
    },
  ],
  model: {
    provider: "loopback-openai-compatible",
    model: "local-grounded-model",
    used: true,
    failure: null,
    output_role: "synthesis-only",
    raw_prompt_retained: false,
    chain_of_thought_retained: false,
  },
  scope: {
    organization_resolved_server_side: true,
    actor_resolved_server_side: true,
    current_access_revalidated: true,
    retrieval_authorization_reused_from_workspace: true,
    cross_organization_retrieval: false,
  },
  semantics: {
    source_context_distinct_from_synthesis: true,
    unvalidated_knowledge_not_presented_as_fact: true,
    uncertainty_explicit: true,
    unavailable_evidence_explicit: true,
    observation_memory_candidate_not_flattened_to_knowledge: true,
  },
  generation: {
    transient_output: true,
    validated_knowledge: false,
    canonical_state_changed: false,
    external_effect_performed: false,
    organizational_authority_provided: false,
    consequential_approval_provided: false,
    question_persisted: false,
  },
  follow_up: {
    kind: "inspect-evidence-first",
    label: "Inspect cited evidence before action",
    href: "/objects/aaaaaaaaaaaaaaaaaaaa",
    direct_consequential_action: false,
    routes_to_governed_execution: false,
    context_bound_governed_continuation_required: true,
  },
};

function json(value: object): Response {
  return new Response(JSON.stringify(value), { status: 200, headers: { "Content-Type": "application/json" } });
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  window.history.replaceState({}, "", "/");
});

describe("P9.08 J6 Ask Arvectum", () => {
  it("asks naturally, separates claim roles, opens evidence, and requires evidence-bound continuation", async () => {
    let copilotInit: RequestInit | undefined;
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const path = String(input);
      if (path === "/api/app/v1/context") return json(context);
      if (path === "/api/app/v1/copilot/ask") {
        copilotInit = init;
        return json(answer);
      }
      throw new Error(`Unexpected P9.08 request: ${path}`);
    }));

    window.history.replaceState({}, "", "/copilot");
    render(<App />);

    expect(await screen.findByRole("heading", { name: /Ask Arvectum about the current work context/i })).toBeTruthy();
    fireEvent.change(screen.getByLabelText("Question"), {
      target: { value: "What is the current status of EIS notice 0344100006426000005 and which source is authoritative?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Ask Arvectum" }));

    expect(await screen.findByText("Source context")).toBeTruthy();
    expect(screen.getByText("AI synthesis")).toBeTruthy();
    expect(screen.getByText("Uncertainty")).toBeTruthy();
    expect(screen.getByText("Transient · not validated Knowledge")).toBeTruthy();
    expect(screen.getByText("Not provided")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Open evidence in Workspace" }).getAttribute("href")).toBe("/objects/aaaaaaaaaaaaaaaaaaaa");
    expect(screen.getByRole("link", { name: "Inspect cited evidence before action" }).getAttribute("href")).toBe("/objects/aaaaaaaaaaaaaaaaaaaa");
    expect(screen.queryByRole("link", { name: "Review governed actions" })).toBeNull();
    expect(screen.queryByText("aaaaaaaaaaaaaaaaaaaa")).toBeNull();

    await waitFor(() => expect(copilotInit).toBeTruthy());
    const headers = new Headers(copilotInit?.headers);
    expect(headers.get("X-Arvectum-CSRF")).toBe("csrf-p908");
    const body = JSON.parse(String(copilotInit?.body));
    expect(Object.keys(body)).toEqual(["question"]);
    expect(body.question).toContain("0344100006426000005");
    expect(JSON.stringify(body)).not.toContain("ООО «Арвектум»");
    expect(JSON.stringify(body)).not.toContain("Owner operator");
  });
});

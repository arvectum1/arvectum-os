import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { MyWork } from "./MyWork";
import { LanguageProvider } from "./i18n";
import type { MyWorkProjection } from "./types";

// R30 clean-head trigger after deterministic production-asset reconciliation.
const projection: MyWorkProjection = {
  schema: "arvectum.workspace.my-work/1",
  generated_at: "2026-08-21T10:00:00Z",
  projection: {
    derived: true,
    canonical_authority: false,
    organizational_authority_provided: false,
    consequential_action_available: false,
    visibility_implies_permission: false,
  },
  scope: {
    organization_resolved_server_side: true,
    actor_resolved_server_side: true,
    denied_item_counts_exposed: false,
  },
  health: {
    state: "fresh",
    code: "OK",
    message: "Attention sources were evaluated against current governed state.",
    observed_at: "2026-08-21T10:00:00Z",
    heartbeat_age_seconds: 1.5,
  },
  items: [
    {
      id: "11111111111111111111",
      kind: "waiting-input",
      group: "decision-required",
      urgency: "high",
      title: "Governed preflight is waiting",
      reason: "Decision evidence is missing.",
      source: "ЕИС / zakupki.gov.ru",
      next_step: "Inspect blockers through the governed flow.",
      evidence_mode: "live",
      observed_at: "2026-08-21T10:00:00Z",
      open_href: "/my-work?focus=11111111111111111111",
      interaction: "inspect-only",
      technical_evidence_available: true,
      authority_provided: false,
    },
    {
      id: "22222222222222222222",
      kind: "reconciliation-required",
      group: "reconciliation-required",
      urgency: "high",
      title: "External outcome is uncertain",
      reason: "Reconciliation is required before any retry.",
      source: "Controlled P8.05 acceptance scenario",
      next_step: "Reconcile the outcome; do not retry blindly.",
      evidence_mode: "scenario",
      observed_at: "2026-08-21T09:00:00Z",
      open_href: "/my-work?focus=22222222222222222222",
      interaction: "inspect-only",
      technical_evidence_available: false,
      authority_provided: false,
    },
    {
      id: "33333333333333333333",
      kind: "guarded-action-failed",
      group: "blocked-failed",
      urgency: "medium",
      title: "Guarded action failed",
      reason: "A fail-closed guard blocked the attempted operation.",
      source: "Controlled acceptance scenario",
      next_step: "Inspect the failed guard before a new governed attempt.",
      evidence_mode: "scenario",
      observed_at: "2026-08-21T08:00:00Z",
      open_href: "/my-work?focus=33333333333333333333",
      interaction: "inspect-only",
      technical_evidence_available: false,
      authority_provided: false,
    },
    {
      id: "44444444444444444444",
      kind: "recent-outcome",
      group: "recent-outcome",
      urgency: "low",
      title: "Recent important outcome",
      reason: "A governed operation completed.",
      source: "Controlled acceptance scenario",
      next_step: "Inspect only if context is needed.",
      evidence_mode: "scenario",
      observed_at: "2026-08-21T07:00:00Z",
      open_href: "/my-work?focus=44444444444444444444",
      interaction: "inspect-only",
      technical_evidence_available: false,
      authority_provided: false,
    },
    {
      id: "55555555555555555555",
      kind: "informational",
      group: "informational",
      urgency: "low",
      title: "Informational note",
      reason: "No action is required.",
      source: "Controlled acceptance scenario",
      next_step: "No action required.",
      evidence_mode: "scenario",
      observed_at: "2026-08-21T06:00:00Z",
      open_href: "/my-work?focus=55555555555555555555",
      interaction: "inspect-only",
      technical_evidence_available: false,
      authority_provided: false,
    },
  ],
};

function mockProjection(value: MyWorkProjection) {
  vi.stubGlobal("fetch", vi.fn(async () => new Response(JSON.stringify(value), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  })));
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  window.history.replaceState({}, "", "/");
});

describe("P9.04 My Work with R30 integration", () => {
  it("renders a human-readable non-authoritative queue and routes only real retained preflight context", async () => {
    window.history.replaceState({}, "", "/my-work");
    mockProjection(projection);
    render(<MyWork />);

    expect(await screen.findByRole("heading", { name: "Needs attention" })).toBeTruthy();
    expect(screen.getByText(/This queue is non-authoritative/)).toBeTruthy();
    expect(screen.queryByText("External outcome is uncertain")).toBeNull();
    expect(screen.getByText("High urgency")).toBeTruthy();
    expect(screen.queryByText("high urgency")).toBeNull();
    expect(screen.queryByRole("button", { name: /approve|retry/i })).toBeNull();
    const taskLinks = screen.getAllByRole("link", { name: "View task" });
    expect(taskLinks).toHaveLength(1);
    expect(taskLinks[0].getAttribute("href")).toMatch(/^\/my-work\?focus=/);
    expect(screen.queryByRole("link", { name: "Open execution context" })).toBeNull();
  });

  it("filters only the already-authorized browser projection", async () => {
    window.history.replaceState({}, "", "/my-work");
    mockProjection(projection);
    render(<MyWork />);

    await screen.findByRole("heading", { name: "Needs attention" });
    fireEvent.change(screen.getByLabelText("Work state"), { target: { value: "decision-required" } });
    expect(screen.getByText("1 visible item")).toBeTruthy();
    expect(screen.getByText("Execution is stopped")).toBeTruthy();
    expect(screen.queryByText("External outcome is uncertain")).toBeNull();

    window.history.replaceState({}, "", "/my-work?mode=scenario");
    render(<MyWork />);
    expect(await screen.findByRole("heading", { name: "Test scenarios" })).toBeTruthy();
    expect(screen.getByText("Check the result")).toBeTruthy();
    expect(screen.getAllByText("Test scenario").length).toBeGreaterThan(0);
  });

  it("shows stale projection health without presenting stale queue items as current", async () => {
    window.history.replaceState({}, "", "/my-work");
    mockProjection({
      ...projection,
      health: {
        ...projection.health,
        state: "stale",
        code: "HEARTBEAT_STALE",
        message: "Work items are withheld until current source state can be revalidated.",
      },
      items: [{
        id: "66666666666666666666",
        kind: "recoverable-system-condition",
        group: "blocked-failed",
        urgency: "high",
        title: "Workspace source is not current",
        reason: "The persistent runtime heartbeat is stale.",
        source: "Arvectum OS persistent runtime",
        next_step: "Restore source health, then refresh.",
        evidence_mode: "live",
        observed_at: "2026-08-21T10:00:00Z",
        open_href: "/my-work?focus=66666666666666666666",
        interaction: "inspect-only",
        technical_evidence_available: false,
        authority_provided: false,
      }],
    });
    render(<MyWork />);

    expect(await screen.findByText("Stale")).toBeTruthy();
    expect(screen.getByText("Process needs review")).toBeTruthy();
    expect(screen.getByText("Task data needs to be checked again.")).toBeTruthy();
    expect(screen.queryByRole("link", { name: "Open execution context" })).toBeNull();
  });

  it("renders a focused Russian task as a dedicated detail page with raw evidence on demand", async () => {
    window.history.replaceState({}, "", "/my-work?focus=11111111111111111111");
    mockProjection(projection);
    render(<LanguageProvider initialLanguage="ru"><MyWork /></LanguageProvider>);

    expect(await screen.findByRole("heading", { name: "Выполнение остановлено" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Разобраться, что блокирует" }).getAttribute("href")).toBe("/governed?focus=11111111111111111111");
    expect(screen.getByRole("link", { name: "Назад к задачам" })).toBeTruthy();
    expect(screen.getByText("Исходные данные").closest("details")?.open).toBe(false);
    expect(screen.queryByText("Видимых задач: 1")).toBeNull();
    fireEvent.click(screen.getByText("Исходные данные"));
    expect(screen.getByText("Governed preflight is waiting")).toBeTruthy();
    expect(screen.getByText("Inspect blockers through the governed flow.")).toBeTruthy();
  });

  it("keeps non-decision task details specific to their actual required work", async () => {
    window.history.replaceState({}, "", "/my-work?focus=22222222222222222222&mode=scenario");
    mockProjection(projection);
    render(<MyWork />);

    expect(await screen.findByRole("heading", { name: "Check the result" })).toBeTruthy();
    expect(screen.getAllByText("Confirm the current state before continuing.")).toHaveLength(2);
    expect(screen.queryByText("Required decisions are missing. They cannot be issued from this screen.")).toBeNull();
    expect(screen.queryByRole("link", { name: "See what is blocking" })).toBeNull();
  });
});

import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { Activity } from "./Activity";
import type { GovernedExperienceProjection, MyWorkProjection } from "./types";

const work: MyWorkProjection = {
  schema: "arvectum.workspace.my-work/1", generated_at: "2026-08-22T06:00:00Z",
  projection: { derived: true, canonical_authority: false, organizational_authority_provided: false, consequential_action_available: false, visibility_implies_permission: false },
  scope: { organization_resolved_server_side: true, actor_resolved_server_side: true, denied_item_counts_exposed: false },
  health: { state: "fresh", code: "OK", message: "Current", observed_at: "2026-08-22T06:00:00Z", heartbeat_age_seconds: 1 },
  items: [{ id: "11111111111111111111", kind: "waiting-input", group: "decision-required", urgency: "high", title: "Decision evidence is needed", reason: "A governed gate remains waiting.", source: "Governed source", next_step: "Inspect governed context.", evidence_mode: "live", observed_at: "2026-08-22T05:59:00Z", open_href: "/my-work?focus=11111111111111111111", interaction: "inspect-only", technical_evidence_available: true, authority_provided: false }],
};
const governed: GovernedExperienceProjection = {
  schema: "arvectum.workspace.governed-experience/1", generated_at: "2026-08-22T06:01:00Z",
  presentation: { title: "Governed preflight", summary: "Review", source: "Governed source", authority_mode: "Native", authority_scope: "org", validation_status: "current" },
  execution: { status: "Waiting", meaning: "Execution remains waiting for governed evidence.", waiting_decisions: ["Consequential Approval"], technical_identity_available: true },
  decisions: [],
  action: { kind: "governed-preflight", label: "Run preflight", available: true, consequential: false, canonical_mutation_requested: false, external_effect_requested: false, authority_provided: false, explanation: "Revalidated server-side." },
  technical: { release_sha: "a", source_subject: "s", source_version: "v", execution_subject: "e", execution_version: "ev", event_version: "event", checkpoint_id: "c", provenance_refs: [] },
  scope: { organization_resolved_server_side: true, actor_resolved_server_side: true, current_access_revalidated: true, organizational_authority_provided: false, visibility_implies_permission: false },
};

afterEach(() => { cleanup(); vi.unstubAllGlobals(); });

describe("P9.09 activity and attention routing", () => {
  it("renders current alerts from My Work semantics and labels the timeline as observed/non-authoritative", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      const payload = url.includes("/my-work") ? work : governed;
      return new Response(JSON.stringify(payload), { status: 200, headers: { "Content-Type": "application/json" } });
    }));
    render(<Activity />);
    expect(await screen.findByRole("heading", { name: "Events and signals" })).toBeTruthy();
    expect(screen.getByText(/not an Event store, audit log, notification authority/)).toBeTruthy();
    expect(screen.getByText(/No read\/unread state is recorded/)).toBeTruthy();
    expect(screen.getByRole("heading", { name: "Current alerts" })).toBeTruthy();
    expect(screen.getAllByText("Decision evidence is needed").length).toBe(2);
    expect(screen.getByText("Governed execution: Waiting")).toBeTruthy();
    expect(screen.getAllByRole("link", { name: "Inspect context" }).map((link) => link.getAttribute("href"))).toContain("/my-work?focus=11111111111111111111");
  });

  it("fails closed rather than retaining partial activity when one protected source cannot be revalidated", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => String(input).includes("/my-work")
      ? new Response(JSON.stringify(work), { status: 200, headers: { "Content-Type": "application/json" } })
      : new Response(JSON.stringify({ detail: "ACCESS_DENIED" }), { status: 403, headers: { "Content-Type": "application/json" } })));
    render(<Activity />);
    expect(await screen.findByRole("heading", { name: "Activity is unavailable." })).toBeTruthy();
    expect(screen.queryByText("Decision evidence is needed")).toBeNull();
  });

  it("does not present scenario items in ordinary activity", async () => {
    const scenarioWork: MyWorkProjection = { ...work, items: [...work.items, { ...work.items[0], id: "22222222222222222222", title: "Scenario approval", evidence_mode: "scenario" }] };
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => new Response(JSON.stringify(String(input).includes("/my-work") ? scenarioWork : governed), { status: 200, headers: { "Content-Type": "application/json" } })));
    render(<Activity />);
    expect(await screen.findByRole("heading", { name: "Events and signals" })).toBeTruthy();
    expect(screen.queryByText("Scenario approval")).toBeNull();
  });
});

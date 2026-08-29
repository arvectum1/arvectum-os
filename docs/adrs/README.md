# Arvectum OS Architecture Decision Records

ADRs record concrete architecture choices made under accepted RFCs.

## Index

| ADR | Title | Status | Date |
|---|---|---|---|
| [`ADR-0001`](ADR-0001-productive-workspace-browser-application-topology.md) | Productive Workspace Browser Application Topology | `Accepted` | `2026-08-21` |
| [`ADR-0002`](ADR-0002-company-workspace-durable-governed-state.md) | Company Workspace Durable Governed State | `Accepted` | `2026-08-29` |

Only `Accepted` ADRs have normative architectural force. A `Proposed` ADR is a decision proposal awaiting valid decision-authority disposition.

ADR-0001 acceptance evidence:

- [`R29 — Productive Workspace Boundary Review`](../reviews/R29-productive-workspace-boundary-review.md) — `Complete / PASS` after 6 functional cross-review iterations;
- [`DECISION-2026-08-21 — ADR-0001 Acceptance`](../governance/decisions/DECISION-2026-08-21-ADR-0001-ACCEPTANCE.md) — `Approved` by residual owner authority;
- approved reviewed proposal blob: `47963cc4c9ca62e986dffbe09ac67b5c6345a111`.

ADR-0002 acceptance evidence:

- [`R34 — M10-alpha Asset Governance / Usability Review`](../reviews/R34-m10-alpha-asset-governance-usability-review.md) — `Executed / BLOCKED`; identified restart-durable governed state as blocker B2;
- functional cross-review of proposal — 5 iterations, no unresolved material objection at proposal level;
- [`DECISION-2026-08-29 — ADR-0002 Acceptance`](../governance/decisions/DECISION-2026-08-29-ADR-0002-ACCEPTANCE.md) — `Approved` by residual owner authority;
- approved reviewed proposal version: `0.1.0`;
- approved reviewed proposal blob: `50103841e624fc09a84e0a1f5aa09eae77fafba3`.

ADR-0002 acceptance authorizes the exact bounded Company Workspace persistence architecture only. It does not itself implement durable state, close R34, achieve M10-alpha, promote a Product Contract/Platform Capability or create a platform-wide database requirement.

## Format

Each ADR must include:

- identifier and title;
- status: `Proposed`, `Accepted`, `Deprecated`, or `Superseded`;
- date;
- related RFCs;
- context;
- decision;
- consequences;
- alternatives considered;
- migration or reversal path where applicable.

## Numbering

```text
ADR-0001-<short-title>.md
```

Numbers are never reused.

## Boundary

An ADR cannot override the Constitution or an accepted RFC. If a decision conflicts with either, the higher-level document must be amended first.

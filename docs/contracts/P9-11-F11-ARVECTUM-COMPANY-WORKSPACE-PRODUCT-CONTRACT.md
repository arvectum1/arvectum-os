# P9.11-F11 — Arvectum Company ↔ Productive Workspace Product Contract

Status: `Draft`
Version: `0.1.0`
Created: `2026-08-26`
Updated: `2026-08-26`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform`, `product_specific` and `governance`
Roadmap work item: `P9.11 — Real daily-use dogfooding + friction/backlog closure`
Finding: [`P9.11-F11 — Материалы компании и единый портфель проектов`](../reviews/P9-11-F11-company-materials-and-project-portfolio.md)
Authority: RFC-0004 `1.0.0` — `Accepted`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` — `Accepted`; ADR-0001 — `Accepted`
Product governance references: Arvectum Company Constitution `1.0.0`; AC-301 portfolio identity boundary; AC-305 cross-product dependency / OS-contract reconciliation

## 1. Purpose and lifecycle

This Draft defines the smallest sufficient Arvectum Company ↔ Arvectum OS Productive Workspace boundary required to address the real owner findings recorded in P9.11-F11:

1. admit and reuse versioned organizational materials/templates of ООО «Арвектум» and create a standard project-bound document from exact governed inputs;
2. present a single read-only portfolio dashboard derived from explicitly registered canonical project roadmap/status sources.

The contract exists **before** real governed Company reliance, as required by RFC-0001 and RFC-0004.

This document is `Draft 0.1.0`. It is not yet effective for governed reliance. It is not:

- a `Provisional` or `Stable` Product Contract;
- a Platform Capability lifecycle promotion;
- a public/stable API, SDK, wire format or browser compatibility promise;
- customer/external Production approval;
- a conformance, SLA, support or certification commitment;
- an Authorization, Organizational Authority, Data Governance permission or approval grant;
- permission for AI to approve or canonically admit documents on its own;
- permission to make Workspace the authoritative roadmap for products;
- permission for Workspace to execute remote/local project actions.

Real governed Company asset admission or authoritative reliance on the portfolio projection is forbidden until the owner explicitly approves the exact contract boundary and the contract is transitioned to an effective `Provisional` version through canonical evidence.

## 2. Product and contract identity

- Product identity: `product/arvectum-company-workspace@organization/arvectum-company`;
- Product architectural owner: `ООО «Арвектум»`;
- Product Contract subject: `product-contract-subject/p9-11-f11-arvectum-company-workspace@organization/arvectum-company`;
- Product Contract version: `product-contract-version/p9-11-f11-arvectum-company-workspace-v0.1.0@organization/arvectum-company`;
- Product Contract semantic type: `platform.product-contract`;
- Product Contract record authority mode: `Native`;
- Product Contract authority scope: `platform.product-contract/boundary`;
- lifecycle: `Draft`;
- Organization scope: one explicit Organization — `ООО «Арвектум»`.

The Product Contract Subject Identity is stable for this boundary lineage. Every materially changed admitted boundary creates a new immutable Product Contract Version Identity. Possession or discovery of the Product Contract creates no access or organizational authority.

## 3. Bounded scope

### 3.1 F11A — Company materials and standard document

The effective bounded contract MAY admit, after transition from Draft:

1. owner/operator upload of allowed Company-owned files or governed external references;
2. exact Organization and Actor attribution;
3. stable Document/Artifact subject identity and immutable version identity;
4. content digest and material provenance;
5. Company-owned semantic role metadata supplied through the product boundary;
6. explicit version discovery and exact-version selection;
7. Company-owned project association using stable Company project identity;
8. creation of a preview/draft from exact selected template/brand/source versions;
9. retention of generation input provenance;
10. generated result as `Transient Output` by default;
11. separate human review and, only where separately admitted, governed promotion/storage/export of the reviewed result.

### 3.2 F11B — project portfolio projection

The effective bounded contract MAY admit:

1. an explicit Company-owned registry of admitted current projects;
2. stable Company project identities independent of repository paths;
3. per-project canonical repository and roadmap/status source descriptors;
4. server-side read-only retrieval of exact canonical source revision/content;
5. source commit/ref/path/fetched-at/freshness/provenance metadata;
6. project-owned adapters/normalizers that map heterogeneous canonical roadmap/status sources into one presentation model;
7. a rebuildable non-canonical dashboard projection exposing done/current/branches/unlocked/blocked and execution-target information only where supported by exact source evidence;
8. visible stale/conflict/unavailable/reconciliation states rather than invented status.

The portfolio projection is read-only in this contract version. It cannot modify product roadmaps, create product tasks, advance milestones or execute actions.

## 4. Explicit exclusions

This contract does **not** authorize:

- automatic final approval of generated documents;
- automatic external email, document delivery, filing, signing or publication;
- electronic signature;
- autonomous legal/commercial/organizational commitment;
- cross-Organization asset or portfolio sharing;
- indexing arbitrary local disks or home directories;
- arbitrary executable/script/package upload;
- macro-enabled Office files in the first slice;
- automatic conversion of uploaded material into validated Knowledge, Policy, Standard or Decision;
- automatic training/learning from uploaded Company material;
- direct browser access to GitHub credentials or repository tokens;
- write access from Workspace to product roadmaps/repositories;
- automatic creation of canonical tasks from chat history or model memory;
- execution or remote control of Mac mini, MacBook, Windows or Linux hosts;
- inference of an execution host solely from a task title, chat or model output;
- public/stable API or SDK commitments;
- `Stable` Product Contract status;
- `Active` Platform Capability promotion.

Any expansion across these exclusions requires a new Product Contract version and the minimum sufficient governance/architecture decision.

## 5. Exact platform dependencies

The first slice intentionally minimizes platform dependencies.

| Dependency | Lifecycle / contract evidence | F11 reliance | Boundary use |
|---|---|---|---|
| `CAP-001 — Document & Artifact Governance` | `Incubating / Provisional` | required by F11A | exact governed Document/Artifact identity/version, provenance, handling metadata and exact-version resolution |
| Productive Workspace application boundary | ADR-0001 `Accepted`; internal bounded application | required | owner-facing SPA/BFF composition, server-side session/authz/data-governance checks, non-authoritative projections |
| RFC-0005 Governed Execution | Accepted semantic boundary | required only for consequential canonical admission/promotion | canonical Company asset/version admission and any later consequential promotion must use declared gates |
| RFC-0006 provenance/event semantics | Accepted semantic boundary | required where canonical admission/effect evidence exists | provenance/correlation without treating telemetry as canonical |

### 5.1 CAP-002 — Memory & Knowledge Governance

**Not a required dependency in the first slice.**

Uploaded brandbook/template/source files remain governed Documents/Artifacts and Company-owned semantic inputs. Receipt/admission does not make their extracted contents validated organizational Knowledge. If later the Company needs governed extracted Knowledge or reusable learned rules, a new Product Contract version must explicitly add CAP-002 scope and validation/promotion semantics.

### 5.2 CAP-003 — Search / Index Projection

**Not required as a Product Contract dependency in the first slice.**

Workspace may provide bounded owner-facing discovery using an internal rebuildable projection over exact admitted items. This does not promote CAP-003 or create a public search contract. If shared governed search becomes a material dependency, a later version must declare it explicitly.

### 5.3 CAP-004 — Audit / Reconstruction Support

**Not required for initial usefulness.**

The contract still requires inspectable provenance/version identities and source revision evidence. Full CAP-004 reconstruction reliance may be added only when a real requirement proves the dependency.

## 6. Platform-owned versus Company-owned semantics

### 6.1 Platform-owned, domain-neutral mechanics

Arvectum OS may own only the reusable mechanics needed across products:

- Organization/Actor attribution;
- safe file/reference intake envelope;
- stable subject identity;
- immutable version identity;
- content digest;
- provenance and received-at evidence;
- classification/rights/retention metadata fields where applicable;
- exact version resolution and selection;
- generic Document/Artifact lifecycle mechanics;
- generic discovery projection;
- portability/export mechanics;
- server-side authorization/data-governance enforcement;
- non-authoritative projection infrastructure;
- declared Governed Execution for consequential canonical mutation.

### 6.2 Company-owned semantics

Arvectum Company remains owner of:

- semantic roles such as `Логотип`, `Брендбук`, `Шаблон документа`, `Шаблон презентации`, `Шаблон письма`, `Организационный источник`;
- brand/style rules and interpretation;
- actual templates and source content;
- standard document types;
- document-generation instructions and presentation behavior;
- stable Company project registry and human-readable project names;
- PORT identities and portfolio relationships under Company governance;
- source descriptors for product roadmaps/status;
- normalizer/adapter semantics where project-specific interpretation is necessary;
- business interpretation of done/current/branch/blocker state;
- execution-target vocabulary/presentation and Company coordination metadata;
- criteria for owner usefulness and internal approval.

No Company-specific schema or rule becomes a platform semantic type merely because Workspace renders it.

## 7. Authority modes and source of truth

### 7.1 Company materials

| Object | Authority mode | Authority / responsibility |
|---|---|---|
| Uploaded source bytes provided by Company | `Native` for the governed Company-held Document/Artifact version once admitted | exact admitted version + provenance under ООО «Арвектум»; underlying third-party facts/content remain subject to their original source/rights |
| External linked source | `External Reference` by default | external source remains authoritative for referenced content; platform governs exact reference/provenance relied upon |
| Company semantic role/brand/template designation | product-owned Company decision | does not become platform authority |
| Generated preview/draft | transient/derived by default | not canonical, not approved, not validated Knowledge |
| Product Contract record | `Native` | Arvectum OS governed Product Contract history |

### 7.2 Project roadmaps and status

| Information | Authority mode | Authority / responsibility |
|---|---|---|
| Arvectum OS sequencing/status | `External Reference` from F11B product perspective | canonical `arvectum1/arvectum-os` roadmap; dashboard is a projection only |
| Arvectum Company sequencing/PORT identity | `External Reference` from Workspace provider perspective | canonical Arvectum Company governance/roadmap |
| Product-specific roadmap/status | `External Reference` | each admitted product repository/governance source |
| F11B normalized dashboard row/card | derived/non-canonical | rebuildable presentation only |
| Local dashboard cache | non-canonical | may be deleted/rebuilt; never silently replaces source truth |

`Governed Replica` is deliberately not selected for roadmap/status in version 0.1.0. If offline replicated authority is later required, freshness/conflict/synchronization/failure semantics must be explicitly governed in a new version.

## 8. Company asset intake envelope

### 8.1 Allowed first-slice file classes

Initial allowlist SHOULD be conservative and exact. It may include:

- PNG/JPEG/WebP images;
- SVG only after safe parsing/sanitization rules reject active/external/scriptable content;
- PDF;
- DOCX;
- PPTX;
- TXT/MD where useful as organizational source material.

Macro-enabled Office formats (`DOCM`, `PPTM`, `XLSM`), executables, scripts, installers, archives with uncontrolled nested content and opaque active-content formats are excluded from the first slice.

The implementation must validate actual content/type, not trust filename extension alone. Unsupported or ambiguous content is rejected visibly.

### 8.2 Intake controls

Before canonical admission, the server-side intake path must enforce at least:

- explicit Organization and Actor;
- exact size limit with visible rejection;
- allowlisted content class;
- content digest;
- filename normalization without path traversal;
- no execution of uploaded content;
- safe storage outside repository/runtime code paths;
- no browser-controlled storage path;
- no secret/token extraction into logs;
- owner affirmation of lawful organizational purpose/right to store/use where applicable;
- classification and retention selection/default consistent with approved policy/evidence;
- receipt separated from governed canonical admission;
- provenance linking receipt → admitted exact version where admission succeeds.

If a safe parser/render pipeline is not available for a class, the platform may store/version it without parsing, provided it is still safe to retain under the admitted controls and the UI states the limitation.

## 9. Canonical mutation and Governed Execution

A real Company asset/version becomes canonical platform-held state only through an admitted RFC-0005 Governed Execution path.

The operation must declare/evaluate separately as applicable:

- `Authorization`;
- `OrganizationalAuthority`;
- `DataGovernance`;
- `ConsequentialApproval`.

Technical session access, uploader identity, Product Contract possession or a UI button satisfies none of these by itself.

The minimal first owner-operated internal flow may keep the human decision simple, but it cannot hide the governing decision/evidence. If current approved delegation does not cover the admission, residual decision authority remains with the owner.

Version replacement is a new immutable version; historical exact versions are not silently overwritten.

## 10. Generated standard document boundary

Generation is Company-owned product behavior over exact platform-governed input references.

Material generation evidence must identify at minimum:

- Organization and requesting Actor;
- stable project identity;
- output document type;
- exact template version;
- exact brand/logo/source versions materially relied upon;
- materially relevant generation configuration/instruction version where retained;
- generated artifact identity/digest;
- derivation provenance.

The generated result is a `Transient Output` by default. Human review is required before any designation as an internally accepted/final Company artifact. External sending/signing/publishing is out of scope.

AI may draft/transform but cannot silently decide that the output is approved, authoritative or compliant.

## 11. Portfolio registry and source descriptors

The first Company registry is explicit, not an automatic enumeration of all GitHub repositories.

Each entry must contain or resolve:

- stable Company project identity;
- display name;
- canonical repository locator;
- canonical roadmap/status source descriptor;
- adapter/export version;
- current inclusion status;
- optional explicit technical execution constraints source;
- Company provenance for the registry entry.

Initial reconciliation scope SHOULD include Arvectum Company, Arvectum OS and the approved PORT identities from AC-301. Repositories not admitted by Company governance must not appear as current projects merely because they exist.

Repository path changes must not silently create a new project identity.

## 12. Portfolio projection contract

For every successful sync the server-side provider records in non-canonical projection state:

- stable project identity;
- exact source repository;
- exact ref/commit SHA;
- source path/descriptor;
- fetched-at timestamp;
- freshness state;
- adapter/export version;
- normalized done/current/branches/unlocked/blocked fields supported by the source;
- per-field or card-level provenance sufficient to reach the source;
- explicit error/conflict/unknown state when normalization is incomplete.

The UI must distinguish:

- current source-backed information;
- stale cached information;
- unavailable source;
- unsupported/unrecognized source format;
- reconciliation required;
- explicit conflict.

Absence of source evidence must not be filled from model memory or chat history.

## 13. Execution target presentation

The first Company-owned vocabulary is:

- `web`;
- `mac-mini`;
- `macbook`;
- `windows-laptop`;
- `windows-test-laptop`;
- `linux-test-laptop`;
- `unspecified`.

This is descriptive coordination metadata only. It is not a remote-execution authorization or platform host abstraction commitment.

A target may be shown when supported by:

1. product-owned canonical technical requirement/constraint; or
2. explicit Company-owned coordination metadata that does not contradict product-owned technical constraints.

Otherwise the UI must show `Не указано`. A model may propose a target as a non-authoritative suggestion, but the canonical dashboard field cannot silently adopt that proposal.

## 14. Security, privacy and isolation

1. All real F11 data is Organization-scoped to ООО «Арвектум» in this contract version.
2. Cross-Organization reads/writes are denied by default.
3. Browser code never receives repository credentials, storage credentials or hidden platform authority.
4. Canonical GitHub/status retrieval occurs server-side through an allowlisted provider boundary.
5. Provider access is read-only for F11B.
6. Repository/path allowlists are explicit; arbitrary URL fetch from browser input is forbidden.
7. Upload storage is separate from executable/runtime/repository paths.
8. Uploaded content is never executed.
9. Logs/telemetry must not duplicate raw Company files, secrets or unnecessary content.
10. Least privilege and minimization apply to retained metadata and cache.
11. Non-canonical projection/cache can be deleted and rebuilt without losing canonical source authority.
12. Any future external/customer Organization requires a new exact contract scope; this version creates no tenant-sharing assumption.

## 15. Rights, retention, deletion and portability

For every real admitted Company material the system must support or preserve:

- accountable Organization and uploader Actor;
- purpose/semantic role;
- rights/source declaration sufficient for the current internal use;
- classification;
- retention policy reference or explicit bounded default;
- exact version history;
- deletion/retirement state without falsifying historical provenance;
- export of retained original bytes/reference plus metadata/provenance in a usable form.

Deletion policy must distinguish physical deletion requirements from retained minimal historical evidence where law/policy permits or requires it. The implementation must not invent indefinite retention.

Portfolio projection/cache has no independent retention claim beyond operationally useful rebuildable state and must be purgeable.

## 16. Failure and degradation semantics

### F11A

On unsupported type, unsafe content, size violation, storage error, authority/gate failure or uncertain admission:

- fail closed;
- do not claim canonical admission;
- do not create a discoverable governed version unless admission actually succeeded;
- preserve only minimal safe receipt/error evidence where allowed;
- present a human-readable remediation path.

### F11B

On GitHub/source/network/auth/rate-limit/schema/adapter failure:

- never present stale data as current;
- keep exact last-success source identity if retained;
- show stale/unavailable/reconciliation state visibly;
- do not infer missing roadmap facts from chat/model memory;
- do not modify source repositories.

One failing project source must not falsify the state of other project cards.

## 17. Events, provenance and observability

Canonical Events are required only for admitted consequential governed acts, not for every dashboard refresh/click.

- canonical asset admission/versioning/promotion uses RFC-0005/RFC-0006 governed evidence as applicable;
- dashboard sync telemetry and fetch diagnostics are non-canonical by default;
- projection cache is non-canonical;
- generated preview telemetry is non-canonical unless separately admitted;
- every materially relied-upon generated result retains exact input provenance;
- replay of historical evidence never repeats upload admission, generation promotion or external effects without a new applicable authorization.

## 18. Deployment and application topology

ADR-0001 remains binding:

- React + TypeScript SPA;
- same-origin Python BFF;
- server-side session/authz/Organization/Data Governance checks;
- no browser authority;
- Company-specific UI composed through explicit product boundary;
- exact co-deployed Workspace release through P7.06;
- no stable/public BFF or browser compatibility promise.

Company-specific F11 providers/components must be removable without changing Kernel semantics.

## 19. Portability and exit

This bounded adoption must have a clear exit path.

If F11 is stopped or the Product Contract is Deprecated/Retired:

- Company composition can be disabled without corrupting platform history;
- original retained Company assets and metadata/provenance can be exported subject to applicable controls;
- non-canonical portfolio/search caches can be deleted and rebuilt;
- no product roadmap depends on Workspace-held hidden state for its canonical truth;
- no private table/import/undocumented endpoint may become a product dependency;
- retirement does not erase lawfully retained immutable historical evidence.

## 20. Acceptance and lifecycle gate

### 20.1 Transition Draft → Provisional

Before `Provisional`:

1. owner must explicitly approve this exact bounded contract;
2. cross-review must have no material unresolved objections;
3. Product/Platform ownership boundary must remain explicit;
4. no higher-authority conflict may exist;
5. canonical Product Contract version identity and approval evidence must be recorded.

Owner approval of this Draft does not itself prove implementation or operational readiness.

### 20.2 F11A implementation PASS

Requires real live owner evidence:

- one real Company asset + one real template admitted through the effective contract;
- exact version/provenance inspectable;
- owner creates one real project-bound standard document from exact versions;
- output provenance inspectable;
- output remains transient until separately reviewed/promoted;
- owner confirms the flow/result is practically useful.

### 20.3 F11B implementation PASS

Requires real live owner evidence:

- admitted current projects appear or visibly report reconciliation/error state;
- source repo/path/SHA/freshness inspectable;
- at least two heterogeneous canonical roadmap layouts normalize correctly;
- source change is reflected after sync with a new exact source SHA;
- execution targets never exceed explicit source/Company coordination evidence;
- owner confirms the dashboard answers where projects are now and what can be done next.

Repo tests, synthetic data and screenshots alone do not provide owner PASS.

## 21. Cross-review — iteration 1

Functional review across platform architecture, product boundary, security/data governance, document governance, portfolio truthfulness, UX and operations found and resolved the following design risks:

- Company brand/template semantics leaking into platform → retained Company-owned;
- direct receipt treated as canonical admission → separated from RFC-0005 governed admission;
- generated document treated as automatically approved/canonical → Transient Output by default;
- upload active content/executable risk → conservative allowlist, no execution, macro-enabled formats excluded;
- roadmap dashboard becoming competing source of truth → read-only derived projection only;
- chat/model memory used as roadmap authority → prohibited;
- browser-side GitHub credential exposure → server-side allowlisted provider only;
- stale portfolio data shown as current → exact source identity + visible freshness/error states;
- arbitrary GitHub repo enumeration interpreted as current Company portfolio → explicit Company registry required;
- execution target interpreted as remote-execution authority → descriptive only; execution out of scope;
- hidden CAP-002/CAP-003 reliance → explicitly omitted from first Product Contract version;
- insufficient exit/portability → explicit export/cache purge/product-decoupling path added.

Material objections after iteration 1: **none at design level**.

This is functional review, not formal Product Contract approval, lifecycle promotion, implementation acceptance or operational-readiness approval.

## 22. Current disposition

- Product Contract: `Draft 0.1.0`;
- real Company governed reliance: **not admitted yet**;
- F10A: bounded owner PASS for guide understandability;
- F11A/F11B: real owner findings with design boundary prepared;
- P9.11 remains `Current`;
- R32 remains `Locked`;
- next governed action: exact owner approval/rejection/amendment of this Draft, then canonical transition to `Provisional` before real F11 reliance.

export type CompanyRoadmapSource = {
  repository: string;
  path: string;
  commit_sha: string;
  content_sha256: string;
  fetched_at: string;
  freshness: string;
  adapter: string;
};

export type CompanyProjectCard = {
  id: string;
  label: string;
  kind: string;
  disposition: string;
  repository: string | null;
  roadmap_path: string | null;
  execution_targets: string[];
  authority_mode: "External Reference";
  projection_authority: "non-authoritative";
  state: "current-source-backed" | "cached-source-backed" | "stale-cache" | "reconciliation-required" | "unavailable";
  message: string;
  source: CompanyRoadmapSource | null;
  roadmap: {
    status: string | null;
    version: string | null;
    source_updated: string | null;
    done: string[];
    current: string[];
    branches: string[];
    unlocked: string[];
    blocked: string[];
  };
};

export type CompanyPortfolioProjection = {
  schema: "arvectum.workspace.company-portfolio/1";
  generated_at: string;
  product_contract: { id: "P9.11-F11"; version: "0.1.0"; lifecycle: "Provisional" };
  projection: {
    derived: true;
    canonical_authority: false;
    read_only: true;
    roadmap_write_available: false;
    remote_execution_available: false;
    chat_or_model_memory_used_as_authority: false;
    visibility_implies_permission: false;
  };
  scope: {
    organization_resolved_server_side: true;
    actor_resolved_server_side: true;
    cross_organization_aggregation: false;
  };
  projects: CompanyProjectCard[];
};

export type StagedMaterialVersion = {
  material_id: string;
  version_id: string;
  predecessor_version_id: string | null;
  organization: string;
  project_id: string;
  filename: string;
  media_type: string;
  semantic_role: string;
  classification: string;
  purpose: string;
  rights: string;
  retention_rule: string;
  uploader: string;
  received_at: string;
  content_sha256: string;
  size_bytes: number;
  state: "StagedNonCanonical";
  canonical_authority: false;
  validated_knowledge: false;
};

export type StagedMaterial = {
  material_id: string;
  latest_version_id: string;
  versions: StagedMaterialVersion[];
};

export type CompanyMaterialsProjection = {
  schema: "arvectum.workspace.company-materials/1";
  generated_at: string;
  product_contract: { id: "P9.11-F11"; version: "0.1.0"; lifecycle: "Provisional" };
  scope: {
    organization_resolved_server_side: true;
    actor_resolved_server_side: true;
    cross_organization_access: false;
  };
  materials: StagedMaterial[];
  governance: {
    state: "StagedNonCanonical";
    canonical_admission_available: false;
    canonical_state_changed: false;
    organizational_authority_provided_by_upload: false;
    validated_knowledge_created: false;
    reason: string;
  };
};

export type GeneratedCompanyOutput = {
  schema: "arvectum.workspace.company-generated-output/1";
  output: {
    output_id: string;
    state: "TransientOutput";
    organization: string;
    project_id: string;
    created_at: string;
    created_by: string;
    source_material_id: string;
    source_version_id: string;
    source_sha256: string;
    output_sha256: string;
    media_type: string;
    filename: string;
    canonical_authority: false;
    validated_knowledge: false;
    download_href: string;
  };
  governance: {
    generated_artifact_state: "TransientOutput";
    canonical_state_changed: false;
    exact_source_version_pinned: true;
  };
};
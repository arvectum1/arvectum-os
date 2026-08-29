export type GeneratedOutputDisposition = "PendingReview" | "Rejected" | "KeepTransient" | "PromotionRequested";

export type CompanyGeneratedOutputReview = {
  disposition: GeneratedOutputDisposition;
  reason: string | null;
  document_title: string | null;
  semantic_role: string | null;
  updated_at: string | null;
  actor: string | null;
  canonical_authority: false;
  output_sha256?: string;
  source_document_version?: string;
  source_artifact_id?: string;
  source_designation_version?: string;
  handling?: CompanyGeneratedOutputHandling;
  handling_digest?: string;
  review_digest?: string;
  source_state?: "TransientOutput";
};

export type CompanyGeneratedOutputHandling = {
  classification: string;
  purpose: string;
  rights: string[];
  retention_rule: string;
  deletion_rule: string;
  permitted_reuse: string[];
};

export type CompanyGeneratedOutputCanonicalPromotion = {
  output_id: string;
  document_subject: string;
  document_version: string;
  designation_subject: string;
  designation_version: string;
  event_version: string;
  promoted_at: string;
  provenance_refs: string[];
};

export type CompanyGeneratedOutputItem = {
  output_id: string;
  state: "TransientOutput";
  canonical_authority: false;
  filename: string;
  media_type: string;
  project_id: string;
  created_at: string;
  created_by: string;
  output_sha256: string;
  source_material_id: string;
  source_version_id: string;
  source_sha256: string;
  download_href: string;
  review: CompanyGeneratedOutputReview;
  inherited_handling: CompanyGeneratedOutputHandling | null;
  exact_source_available: boolean;
  source_error: string | null;
  canonical_promotion: CompanyGeneratedOutputCanonicalPromotion | null;
  promotion_available: boolean;
  validated_knowledge: false;
};

export type CompanyGeneratedOutputsProjection = {
  schema: "arvectum.workspace.company-generated-outputs/1";
  generated_at: string;
  product_contract: {
    id: string;
    version: "0.2.0";
    lifecycle: "Provisional";
  };
  items: CompanyGeneratedOutputItem[];
  actions: { governed_promotion_available: boolean };
  governance: {
    output_source_state: "TransientOutput";
    review_is_canonical: false;
    promotion_requires_governed_execution: true;
    promotion_relabels_transient_source: false;
    validated_knowledge_created: false;
    external_send_sign_publish_available: false;
  };
};

"""ADR-0002 durable wrappers for the existing P10.03/P10.05 Company executors.

The semantic owners and authority gates remain unchanged.  These wrappers only
establish the product-local durability boundary required by R34: load governed
state on construction, persist after a successful semantic transition, and
read-after-write reconstruct before reporting success.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .access import AccessContext
from .company_asset_governed_provider import P1004OwnerCompanyAssetAdmissionProvider
from .company_asset_library import (
    CompanyAssetAdmissionUnavailable,
    CompanyAssetReviewPolicy,
    P1003CompanyAssetAdmissionExecutor,
    _policy_digest,
)
from .company_generated_output_governed_provider import (
    P1005OwnerCompanyGeneratedOutputPromotionProvider,
)
from .company_generated_outputs import (
    CompanyGeneratedOutputPromotionUnavailable,
    CompanyGeneratedOutputReviewEvidence,
    P1005CompanyGeneratedOutputPromotionExecutor,
)
from .company_governed_state_store import CompanyGovernedStateError, CompanyGovernedStateStore
from .company_materials import CompanyMaterialsStore


class DurableP1003CompanyAssetAdmissionExecutor(P1003CompanyAssetAdmissionExecutor):
    """P10.03/P10.04 executor with ADR-0002 restart-durable state."""

    def __init__(self, provider, runtime_root: Path) -> None:
        super().__init__(provider)
        self.governed_state_store = CompanyGovernedStateStore(runtime_root)
        self.state = self.governed_state_store.load_admission_state()

    def admit(
        self,
        *,
        access: AccessContext,
        store: CompanyMaterialsStore,
        material_id: str,
        version_id: str,
        policy: CompanyAssetReviewPolicy,
    ):
        scope = access.organization.value
        policy_digest = _policy_digest(policy)
        intent_key = (scope, material_id, version_id, policy_digest)
        try:
            self._intent_times[intent_key] = self.governed_state_store.intent_time(
                kind="admission",
                key=intent_key,
                proposed=datetime.now(timezone.utc),
            )
            value = super().admit(
                access=access,
                store=store,
                material_id=material_id,
                version_id=version_id,
                policy=policy,
            )
            self.state = self.governed_state_store.persist_admission_state(self.state)
            exact = tuple(
                item
                for item in self.admitted_versions(access)
                if item.material_id == material_id and item.version_id == version_id
            )
            if len(exact) != 1 or exact[0] != value:
                raise CompanyGovernedStateError(
                    "durable admission reconstruction differs from the semantic result"
                )
            return exact[0]
        except CompanyGovernedStateError as exc:
            try:
                self.state = self.governed_state_store.load_admission_state()
            except CompanyGovernedStateError:
                pass
            raise CompanyAssetAdmissionUnavailable(
                "durable Company Asset admission state is unavailable; success is not claimed"
            ) from exc


class DurableP1005CompanyGeneratedOutputPromotionExecutor(
    P1005CompanyGeneratedOutputPromotionExecutor
):
    """P10.05 executor with ADR-0002 restart-durable promotion state."""

    def __init__(self, provider, asset_admission: P1003CompanyAssetAdmissionExecutor, runtime_root: Path) -> None:
        super().__init__(provider, asset_admission)
        self.governed_state_store = CompanyGovernedStateStore(runtime_root)
        self.state = self.governed_state_store.load_promotion_state()

    def promote(
        self,
        *,
        access: AccessContext,
        store: CompanyMaterialsStore,
        output_id: str,
        review: CompanyGeneratedOutputReviewEvidence,
    ):
        intent_key = (access.organization.value, output_id, review.review_digest)
        try:
            self._intent_times[intent_key] = self.governed_state_store.intent_time(
                kind="promotion",
                key=intent_key,
                proposed=datetime.now(timezone.utc),
            )
            value = super().promote(
                access=access,
                store=store,
                output_id=output_id,
                review=review,
            )
            self.state = self.governed_state_store.persist_promotion_state(self.state)
            exact = tuple(
                item for item in self.promoted_outputs(access) if item.output_id == output_id
            )
            if len(exact) != 1 or exact[0] != value:
                raise CompanyGovernedStateError(
                    "durable promotion reconstruction differs from the semantic result"
                )
            return exact[0]
        except CompanyGovernedStateError as exc:
            try:
                self.state = self.governed_state_store.load_promotion_state()
            except CompanyGovernedStateError:
                pass
            raise CompanyGeneratedOutputPromotionUnavailable(
                "durable generated-output promotion state is unavailable; success is not claimed"
            ) from exc


def build_durable_company_governed_executors(
    runtime_root: Path,
) -> tuple[
    DurableP1003CompanyAssetAdmissionExecutor,
    DurableP1005CompanyGeneratedOutputPromotionExecutor,
]:
    """Build the owner-operated Company admission/promotion pair on one durable root."""

    root = runtime_root.expanduser()
    asset = DurableP1003CompanyAssetAdmissionExecutor(
        P1004OwnerCompanyAssetAdmissionProvider(root),
        root,
    )
    promotion = DurableP1005CompanyGeneratedOutputPromotionExecutor(
        P1005OwnerCompanyGeneratedOutputPromotionProvider(root),
        asset,
        root,
    )
    return asset, promotion


__all__ = [
    "DurableP1003CompanyAssetAdmissionExecutor",
    "DurableP1005CompanyGeneratedOutputPromotionExecutor",
    "build_durable_company_governed_executors",
]

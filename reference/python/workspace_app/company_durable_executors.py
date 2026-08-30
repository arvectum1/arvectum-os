"""ADR-0002 durable wrappers for the existing P10.03/P10.05 Company executors.

The semantic owners and authority gates remain unchanged. These wrappers only
establish the product-local durability boundary required by R34: reconstruct
committed governed state on construction, persist a pre-effect crash marker,
run the existing governed semantic owner, persist/read-back the resulting state,
and only then resolve the marker as committed.

Recovery never replays a consequential effect. An unresolved pre-effect marker
fails closed and requires reconciliation unless the already-durable semantic
state itself proves that the same retry token committed.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

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


def _committed_tokens(state: Any) -> tuple[str, ...]:
    committed = getattr(state, "committed", ())
    return tuple(item.retry_token for item in committed)


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
        existing = tuple(
            item
            for item in self.admitted_versions(access)
            if item.material_id == material_id and item.version_id == version_id
        )
        if len(existing) == 1:
            # A recovered durable commit is sufficient evidence for an idempotent
            # response. Do not execute or replay the consequential operation.
            return existing[0]
        if len(existing) > 1:
            raise CompanyAssetAdmissionUnavailable("exact durable Company Asset version is ambiguous")

        scope = access.organization.value
        policy_digest = _policy_digest(policy)
        intent_key = (scope, material_id, version_id, policy_digest)
        retry_token = f"company-asset-admission:{scope}:{material_id}:{version_id}:{policy_digest}"
        attempt_id: str | None = None
        before = self.state
        try:
            command_at = self.governed_state_store.intent_time(
                kind="admission",
                key=intent_key,
                proposed=datetime.now(timezone.utc),
            )
            self._intent_times[intent_key] = command_at
            attempt_id = self.governed_state_store.begin_effect(
                kind="admission",
                key=intent_key,
                retry_token=retry_token,
                started_at=datetime.now(timezone.utc),
                committed_retry_tokens=_committed_tokens(self.state),
            )
        except CompanyGovernedStateError as exc:
            raise CompanyAssetAdmissionUnavailable(
                "durable Company Asset admission pre-effect evidence is unavailable; no effect is attempted"
            ) from exc

        try:
            value = super().admit(
                access=access,
                store=store,
                material_id=material_id,
                version_id=version_id,
                policy=policy,
            )
        except Exception as exc:
            if self.state != before:
                raise CompanyAssetAdmissionUnavailable(
                    "Company Asset admission outcome is uncertain; durable reconciliation is required before retry"
                ) from exc
            try:
                self.governed_state_store.resolve_effect(
                    kind="admission",
                    attempt_id=attempt_id,
                    outcome="no_effect",
                    resolved_at=datetime.now(timezone.utc),
                    committed_retry_tokens=_committed_tokens(self.state),
                )
            except CompanyGovernedStateError as journal_exc:
                raise CompanyAssetAdmissionUnavailable(
                    "Company Asset admission failed before a proven effect, but durable outcome recording failed; reconciliation is required"
                ) from journal_exc
            raise

        try:
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
            self.governed_state_store.resolve_effect(
                kind="admission",
                attempt_id=attempt_id,
                outcome="committed",
                resolved_at=datetime.now(timezone.utc),
                committed_retry_tokens=_committed_tokens(self.state),
            )
            return exact[0]
        except CompanyGovernedStateError as exc:
            try:
                self.state = self.governed_state_store.load_admission_state()
            except CompanyGovernedStateError:
                pass
            raise CompanyAssetAdmissionUnavailable(
                "durable Company Asset admission state is unavailable or uncertain; success is not claimed"
            ) from exc


class DurableP1005CompanyGeneratedOutputPromotionExecutor(
    P1005CompanyGeneratedOutputPromotionExecutor
):
    """P10.05 executor with ADR-0002 restart-durable promotion state."""

    def __init__(
        self,
        provider,
        asset_admission: P1003CompanyAssetAdmissionExecutor,
        runtime_root: Path,
    ) -> None:
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
        existing = tuple(item for item in self.promoted_outputs(access) if item.output_id == output_id)
        if len(existing) == 1:
            # Recovered durable result: return the exact prior commit without
            # repeating the promotion or its Event.
            return existing[0]
        if len(existing) > 1:
            raise CompanyGeneratedOutputPromotionUnavailable(
                "exact durable promoted output is ambiguous"
            )

        scope = access.organization.value
        intent_key = (scope, output_id, review.review_digest)
        retry_token = (
            f"company-generated-output-promotion:{scope}:{output_id}:{review.review_digest}"
        )
        attempt_id: str | None = None
        before = self.state
        try:
            command_at = self.governed_state_store.intent_time(
                kind="promotion",
                key=intent_key,
                proposed=datetime.now(timezone.utc),
            )
            self._intent_times[intent_key] = command_at
            attempt_id = self.governed_state_store.begin_effect(
                kind="promotion",
                key=intent_key,
                retry_token=retry_token,
                started_at=datetime.now(timezone.utc),
                committed_retry_tokens=_committed_tokens(self.state),
            )
        except CompanyGovernedStateError as exc:
            raise CompanyGeneratedOutputPromotionUnavailable(
                "durable generated-output promotion pre-effect evidence is unavailable; no effect is attempted"
            ) from exc

        try:
            value = super().promote(
                access=access,
                store=store,
                output_id=output_id,
                review=review,
            )
        except Exception as exc:
            if self.state != before:
                raise CompanyGeneratedOutputPromotionUnavailable(
                    "generated-output promotion outcome is uncertain; durable reconciliation is required before retry"
                ) from exc
            try:
                self.governed_state_store.resolve_effect(
                    kind="promotion",
                    attempt_id=attempt_id,
                    outcome="no_effect",
                    resolved_at=datetime.now(timezone.utc),
                    committed_retry_tokens=_committed_tokens(self.state),
                )
            except CompanyGovernedStateError as journal_exc:
                raise CompanyGeneratedOutputPromotionUnavailable(
                    "generated-output promotion failed before a proven effect, but durable outcome recording failed; reconciliation is required"
                ) from journal_exc
            raise

        try:
            self.state = self.governed_state_store.persist_promotion_state(self.state)
            exact = tuple(
                item for item in self.promoted_outputs(access) if item.output_id == output_id
            )
            if len(exact) != 1 or exact[0] != value:
                raise CompanyGovernedStateError(
                    "durable promotion reconstruction differs from the semantic result"
                )
            self.governed_state_store.resolve_effect(
                kind="promotion",
                attempt_id=attempt_id,
                outcome="committed",
                resolved_at=datetime.now(timezone.utc),
                committed_retry_tokens=_committed_tokens(self.state),
            )
            return exact[0]
        except CompanyGovernedStateError as exc:
            try:
                self.state = self.governed_state_store.load_promotion_state()
            except CompanyGovernedStateError:
                pass
            raise CompanyGeneratedOutputPromotionUnavailable(
                "durable generated-output promotion state is unavailable or uncertain; success is not claimed"
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

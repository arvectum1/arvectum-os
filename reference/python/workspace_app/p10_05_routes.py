"""P10.05 internal same-origin BFF routes for reviewed generated outputs."""

from __future__ import annotations

import json
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request, status

from .access import AccessContext, WorkspaceAccessError
from .company_generated_outputs import (
    CompanyGeneratedOutputError,
    CompanyGeneratedOutputPromotionUnavailable,
    CompanyGeneratedOutputReviewError,
    CompanyGeneratedOutputs,
)
from .company_materials import CompanyMaterialUnavailable, CompanyMaterialsError
from .main import CSRF_HEADER, _identity_key, _security_event
from .security import WorkspaceSession


MAX_OUTPUT_REVIEW_REQUEST_BYTES = 8 * 1024


def _bounded_json_body(limit: int, code: str):
    async def dependency(request: Request) -> object:
        if request.headers.get("transfer-encoding"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=code)
        raw_length = request.headers.get("content-length")
        if raw_length is not None:
            try:
                length = int(raw_length)
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=code) from None
            if length <= 0 or length > limit:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=code)
        raw = await request.body()
        if not raw or len(raw) > limit:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=code)
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=code) from None

    return dependency


def install_p10_05_routes(app: FastAPI, *, outputs: CompanyGeneratedOutputs) -> FastAPI:
    """Install P10.05 after F11/P10.04 composition and before the SPA catch-all."""

    if not isinstance(outputs, CompanyGeneratedOutputs):
        raise TypeError("P10.05 routes require CompanyGeneratedOutputs composition")
    settings = app.state.settings
    sessions = app.state.session_store
    resolver = app.state.access_resolver
    app.state.company_generated_outputs = outputs

    spa_routes = [route for route in app.router.routes if getattr(route, "path", None) == "/{path:path}"]
    if len(spa_routes) != 1:
        raise RuntimeError("P10.05 route installation requires exactly one Workspace SPA catch-all")
    spa_route = spa_routes[0]
    app.router.routes.remove(spa_route)

    def authorize_current(request: Request) -> tuple[WorkspaceSession, AccessContext]:
        session_id = request.cookies.get(settings.cookie_name)
        session = sessions.get(session_id)
        if session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="SESSION_REQUIRED")
        try:
            access = resolver.authorize()
        except WorkspaceAccessError as exc:
            sessions.revoke(session_id)
            _security_event("ACCESS_REVALIDATION_DENIED", request, sessions, str(exc))
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ACCESS_DENIED") from exc
        if (
            session.organization_key != _identity_key(access.organization)
            or session.actor_key != _identity_key(access.actor)
        ):
            sessions.revoke(session_id)
            _security_event("CONTEXT_BINDING_CHANGED", request, sessions)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CONTEXT_CHANGED")
        return session, access

    def csrf_current(
        request: Request,
        current: tuple[WorkspaceSession, AccessContext] = Depends(authorize_current),
    ) -> tuple[WorkspaceSession, AccessContext]:
        session, access = current
        if not sessions.csrf_matches(session, request.headers.get(CSRF_HEADER)):
            _security_event("CSRF_REJECTED", request, sessions)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF_REJECTED")
        return session, access

    @app.get("/api/app/v1/company-generated-outputs")
    async def company_generated_outputs(
        current: tuple[WorkspaceSession, AccessContext] = Depends(authorize_current),
    ) -> dict[str, Any]:
        _, access = current
        try:
            return outputs.project(access)
        except (CompanyGeneratedOutputError, CompanyMaterialsError):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="COMPANY_GENERATED_OUTPUTS_UNAVAILABLE",
            ) from None

    @app.post("/api/app/v1/company-generated-outputs/{output_id}/review")
    async def review_company_generated_output(
        output_id: str,
        payload: object = Depends(
            _bounded_json_body(MAX_OUTPUT_REVIEW_REQUEST_BYTES, "COMPANY_OUTPUT_REVIEW_REJECTED")
        ),
        current: tuple[WorkspaceSession, AccessContext] = Depends(csrf_current),
    ) -> dict[str, Any]:
        _, access = current
        try:
            review = outputs.review(access, output_id, payload)
            return {
                "schema": "arvectum.workspace.company-generated-output-review-result/1",
                "review": review,
                "source_state": "TransientOutput",
                "canonical_state_changed": False,
            }
        except CompanyGeneratedOutputReviewError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="COMPANY_OUTPUT_REVIEW_REJECTED"
            ) from None
        except CompanyMaterialUnavailable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COMPANY_OUTPUT_UNAVAILABLE") from None
        except (CompanyGeneratedOutputError, CompanyMaterialsError):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="COMPANY_OUTPUT_REVIEW_UNAVAILABLE",
            ) from None

    @app.post("/api/app/v1/company-generated-outputs/{output_id}/promote")
    async def promote_company_generated_output(
        output_id: str,
        current: tuple[WorkspaceSession, AccessContext] = Depends(csrf_current),
    ) -> dict[str, Any]:
        _, access = current
        try:
            promoted = outputs.promote(access, output_id)
            return {
                "schema": "arvectum.workspace.company-generated-output-promotion-result/1",
                "promoted": promoted.to_payload(),
                "source_state": "TransientOutput",
                "source_relabelled": False,
                "canonical_state_changed": True,
                "through_governed_execution": True,
                "validated_knowledge_created": False,
            }
        except CompanyGeneratedOutputPromotionUnavailable:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="COMPANY_OUTPUT_PROMOTION_UNAVAILABLE",
            ) from None
        except CompanyGeneratedOutputReviewError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="COMPANY_OUTPUT_NOT_READY_FOR_PROMOTION",
            ) from None
        except CompanyMaterialUnavailable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COMPANY_OUTPUT_UNAVAILABLE") from None
        except (CompanyGeneratedOutputError, CompanyMaterialsError):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="COMPANY_OUTPUT_PROMOTION_FAILED",
            ) from None

    app.router.routes.append(spa_route)
    return app


__all__ = ["install_p10_05_routes"]

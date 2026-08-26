#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from workspace_app.access import P704AccessResolver, provision_workspace_grant
from workspace_app.assets import verify_frontend_assets
from workspace_app.config import WorkspaceSettings
from workspace_app.f11_routes import install_f11_routes
from workspace_app.main import create_app
from workspace_app.release import load_release


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P9.03 Arvectum OS Productive Workspace")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="verify current access and release-pinned built frontend")
    provision = sub.add_parser("provision-local-grant", help="create the exact local Workspace shell operational grant")
    provision.add_argument("--confirm", action="store_true")
    sub.add_parser("serve", help="serve the bounded same-origin SPA+BFF on the configured profile")
    return parser


def _frontend_root() -> Path:
    return Path(__file__).resolve().parent / "workspace_frontend"


def build_workspace_app(settings: WorkspaceSettings):
    """Build one same-origin Workspace app and install bounded F11 product routes."""

    return install_f11_routes(create_app(settings))


def main() -> None:
    args = _parser().parse_args()
    settings = WorkspaceSettings.from_env()
    release = load_release()
    if args.command == "provision-local-grant":
        if not args.confirm:
            raise SystemExit("--confirm is required; access is never auto-granted")
        grant_id = provision_workspace_grant(settings.runtime_root)
        print(json.dumps({"status": "PASS", "grant_id": grant_id, "organizational_authority_provided": False}, sort_keys=True))
        return
    if args.command == "check":
        access = P704AccessResolver(settings.runtime_root).authorize()
        assets = verify_frontend_assets(_frontend_root(), release)
        print(
            json.dumps(
                {
                    **assets,
                    "organization_scope": access.organization.value,
                    "actor_attributable": True,
                    "operational_access_only": True,
                    "organizational_authority_provided": False,
                    "public_origin": settings.public_origin,
                },
                sort_keys=True,
            )
        )
        return
    verify_frontend_assets(_frontend_root(), release)
    import uvicorn

    uvicorn.run(
        build_workspace_app(settings),
        host=settings.bind_host,
        port=settings.bind_port,
        proxy_headers=False,
        server_header=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()

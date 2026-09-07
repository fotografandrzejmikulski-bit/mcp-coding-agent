"""HTTP authentication middleware for remote MCP deployments."""

from __future__ import annotations

import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class MCPAuthMiddleware(BaseHTTPMiddleware):
    """Require a bearer token for /mcp when MCP_AUTH_TOKEN is configured."""

    async def dispatch(self, request: Request, call_next) -> Response:
        expected = os.getenv("MCP_AUTH_TOKEN", "").strip()
        path = request.url.path

        if not expected or path == "/health":
            return await call_next(request)

        if path != "/mcp":
            return await call_next(request)

        auth = request.headers.get("authorization", "")
        if auth != f"Bearer {expected}":
            return JSONResponse({"error": "unauthorized"}, status_code=401, headers={"WWW-Authenticate": "Bearer"})

        return await call_next(request)

"""MCP build-state tools."""

from __future__ import annotations

import os
import uuid

from mcp.server.fastmcp import FastMCP

from mcp_coding_agent.core.store import JsonStore


def _store() -> JsonStore:
    return JsonStore(os.getenv("BUILDER_STATE_DIR", "/tmp/mcp-coding-agent-state"))


def register_state_tools(server: FastMCP) -> None:
    """Register durable build-state operations."""

    @server.tool()
    def create_build_state(task: str, workspace: str | None = None) -> dict[str, object]:
        """Create a durable build-state record for a task."""
        if not task.strip():
            raise ValueError("task cannot be empty")
        build_id = str(uuid.uuid4())
        state = {
            "build_id": build_id,
            "status": "pending",
            "phase": "analyze",
            "task": task.strip(),
            "workspace": workspace,
            "attempts": 0,
            "artifacts": [],
            "findings": [],
        }
        path = _store().put(build_id, state)
        return {"build_id": build_id, "state_path": path, "state": state}

    @server.tool()
    def get_build_state(build_id: str) -> dict[str, object]:
        """Retrieve a previously created build-state record."""
        state = _store().get(build_id)
        if state is None:
            return {"found": False, "build_id": build_id}
        return {"found": True, "build_id": build_id, "state": state}

"""MCP build-state tools."""

from __future__ import annotations

import uuid

from mcp.server.fastmcp import FastMCP

from mcp_coding_agent.core.store import JsonStore


_DEFAULT_STATE_DIR = "/tmp/mcp-coding-agent-state"


def register_state_tools(server: FastMCP) -> None:
    """Register simple durable build-state operations."""

    @server.tool()
    def create_build_state(task: str, workspace: str | None = None) -> dict[str, object]:
        """Create a durable build-state record for a task."""
        build_id = str(uuid.uuid4())
        store = JsonStore(_DEFAULT_STATE_DIR)
        state = {
            "build_id": build_id,
            "status": "pending",
            "phase": "analyze",
            "task": task,
            "workspace": workspace,
            "attempts": 0,
            "artifacts": [],
            "findings": [],
        }
        path = store.put(build_id, state)
        return {"build_id": build_id, "state_path": path, "state": state}

    @server.tool()
    def get_build_state(build_id: str) -> dict[str, object]:
        """Retrieve a previously created build-state record."""
        state = JsonStore(_DEFAULT_STATE_DIR).get(build_id)
        if state is None:
            return {"found": False, "build_id": build_id}
        return {"found": True, "build_id": build_id, "state": state}

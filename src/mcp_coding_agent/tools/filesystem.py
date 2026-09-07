"""Workspace-scoped filesystem MCP tools."""

from __future__ import annotations

from mcp_coding_agent.core.workspace import Workspace


def read_file(root: str, path: str, max_bytes: int = 200_000) -> dict[str, object]:
    workspace = Workspace(root)
    return {"path": path, "content": workspace.read(path, max_bytes=max_bytes)}


def write_file(root: str, path: str, content: str) -> dict[str, object]:
    workspace = Workspace(root)
    return {"path": workspace.write(path, content), "bytes": len(content.encode("utf-8"))}

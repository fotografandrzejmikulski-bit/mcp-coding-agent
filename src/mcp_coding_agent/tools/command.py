"""Controlled command execution MCP tool."""

from __future__ import annotations

from mcp_coding_agent.core.workspace import Workspace


def run_command(root: str, command: str, timeout: int = 120) -> dict[str, object]:
    if timeout < 1 or timeout > 600:
        raise ValueError("timeout must be between 1 and 600 seconds")
    return Workspace(root).run(command, timeout=timeout)

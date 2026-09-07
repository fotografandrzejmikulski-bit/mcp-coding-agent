"""Tool registration boundary for the MCP server."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from .tools.command import run_command
from .tools.filesystem import read_file, write_file
from .tools.git import git_diff, git_status


def register_execution_tools(server: FastMCP) -> None:
    """Register coding/runtime tools on an MCP server instance."""

    @server.tool()
    def read_project_file(root: str, path: str, max_bytes: int = 200_000) -> dict[str, object]:
        """Read a UTF-8 file from an explicitly authorized workspace."""
        return read_file(root, path, max_bytes)

    @server.tool()
    def write_project_file(root: str, path: str, content: str) -> dict[str, object]:
        """Write a UTF-8 file inside an explicitly authorized workspace."""
        return write_file(root, path, content)

    @server.tool()
    def execute_workspace_command(root: str, command: str, timeout: int = 120) -> dict[str, object]:
        """Execute a policy-checked command in the project workspace."""
        return run_command(root, command, timeout)

    @server.tool()
    def inspect_git_status(root: str) -> dict[str, object]:
        """Inspect repository status without modifying it."""
        return git_status(root)

    @server.tool()
    def inspect_git_diff(root: str, staged: bool = False) -> dict[str, object]:
        """Inspect current repository diff without modifying it."""
        return git_diff(root, staged)

    @server.resource("builder://tool-policy")
    def tool_policy() -> str:
        """Expose execution boundaries to the MCP client."""
        return json.dumps(
            {
                "workspace": "explicit-root-only",
                "filesystem": "path-traversal-protected",
                "commands": "allowlist-and-dangerous-pattern-protected",
                "credentials": "OpenAI/GitHub secrets are not passed to child commands",
                "git": "read-only in current release",
            },
            indent=2,
        )

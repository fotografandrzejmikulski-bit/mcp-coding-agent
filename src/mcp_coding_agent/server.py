"""MCP server for the coding agent."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server import MCPServer

load_dotenv()

mcp = MCPServer(
    "mcp-coding-agent",
    instructions=(
        "You are connected to a coding-agent MCP server. "
        "Use its tools to inspect and modify an explicitly selected workspace. "
        "Never assume access to arbitrary paths."
    ),
)


@mcp.tool()
def health_check() -> str:
    """Return a simple server health status."""
    return "ok"


@mcp.tool()
def inspect_workspace(path: str) -> dict[str, object]:
    """Inspect a workspace path and return safe filesystem metadata.

    This first-phase tool is intentionally read-only. It validates that the
    supplied path exists and reports whether it is a file or directory.
    """
    target = Path(path).expanduser().resolve()

    if not target.exists():
        return {"exists": False, "path": str(target)}

    return {
        "exists": True,
        "path": str(target),
        "type": "directory" if target.is_dir() else "file",
        "name": target.name,
    }


def main() -> None:
    """Run the MCP server over Streamable HTTP."""
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_PORT", "8000"))
    mcp.run(
        transport="streamable-http",
        host=host,
        port=port,
    )


if __name__ == "__main__":
    main()

"""MCP tool for generating portable agent-system artifacts."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from mcp_coding_agent.core.models import AgentSpec, SystemSpec
from mcp_coding_agent.generation.agent_system import AgentSystemGenerator


def register_generation_tools(server: FastMCP) -> None:
    """Register deterministic project generation capabilities."""

    @server.tool()
    def generate_agent_system(agents_json: str, name: str, goal: str) -> dict[str, object]:
        """Generate portable architecture and machine-readable artifacts for a multi-agent system."""
        raw = json.loads(agents_json)
        if not isinstance(raw, list):
            raise ValueError("agents_json must be a JSON array")
        spec = SystemSpec(name=name, objective=goal, agents=[AgentSpec(**item) for item in raw])
        artifacts = AgentSystemGenerator().generate(spec)
        return {
            "artifacts": [{"path": item.path, "content": item.content} for item in artifacts],
            "agent_count": len(spec.agents),
        }

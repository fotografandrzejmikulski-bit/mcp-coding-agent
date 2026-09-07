"""High-level builder control tools."""

from __future__ import annotations

import json

from agents import Agent, Runner
from mcp.server.fastmcp import FastMCP

from mcp_coding_agent.core.models import AgentSpec, AgentRole, SystemSpec
from mcp_coding_agent.core.prompts import BUILDER_SYSTEM_PROMPT
from mcp_coding_agent.core.validation import validate_system


def register_builder_tools(server: FastMCP) -> None:
    """Register high-level design and autonomous-run tools."""

    @server.tool()
    def validate_agent_system(agents_json: str, name: str = "system", goal: str = "validate") -> dict[str, object]:
        """Validate agent IDs, roles, and handoff topology before execution."""
        raw = json.loads(agents_json)
        if not isinstance(raw, list):
            raise ValueError("agents_json must be a JSON array")
        specs = [AgentSpec(**item) for item in raw]
        warnings = validate_system(SystemSpec(name=name, objective=goal, agents=specs))
        return {"valid": True, "warnings": warnings, "agent_count": len(specs)}

    @server.tool()
    async def run_builder(task: str, model: str | None = None) -> dict[str, object]:
        """Run the principal autonomous builder for a complex engineering task.

        This tool orchestrates specialist agents for analysis, architecture, implementation,
        testing, review, repair, security, and deployment design. It does not implicitly grant
        filesystem access; execution tools remain separately scoped by workspace.
        """
        if not task.strip():
            raise ValueError("task cannot be empty")
        kwargs: dict[str, object] = {"name": "Autonomous Builder", "instructions": BUILDER_SYSTEM_PROMPT}
        if model:
            kwargs["model"] = model
        agent = Agent(**kwargs)
        result = await Runner.run(agent, task.strip())
        return {"success": True, "final_output": result.final_output, "last_agent": result.last_agent.name}

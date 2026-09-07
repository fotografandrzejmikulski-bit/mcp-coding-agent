"""MCP server entry point for the autonomous Agents Builder."""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .agent_builder import AgentSpec, SystemSpec, system_blueprint

load_dotenv()

mcp = FastMCP(
    "mcp-coding-agent",
    instructions=(
        "You are an autonomous senior coding and AI-agent systems builder. "
        "Decompose requirements, design architectures, generate implementation plans, "
        "coordinate specialist agents, validate changes, run tests, diagnose failures, "
        "repair code, and verify the final system. Prefer deterministic, testable steps. "
        "Never modify a workspace outside an explicitly authorized project root."
    ),
)


@mcp.tool()
def health_check() -> dict[str, str]:
    """Return service health and builder identity."""
    return {"status": "ok", "service": "mcp-coding-agent", "role": "agents-builder"}


@mcp.tool()
def inspect_workspace(path: str) -> dict[str, object]:
    """Inspect a project path using read-only filesystem metadata."""
    target = Path(path).expanduser().resolve()
    if not target.exists():
        return {"exists": False, "path": str(target)}

    children: list[str] = []
    if target.is_dir():
        children = sorted(item.name for item in target.iterdir())[:200]

    return {
        "exists": True,
        "path": str(target),
        "type": "directory" if target.is_dir() else "file",
        "name": target.name,
        "children": children,
    }


@mcp.tool()
def design_agent(
    name: str,
    purpose: str,
    instructions: str,
    tools: list[str] | None = None,
    handoffs: list[str] | None = None,
    guardrails: list[str] | None = None,
    model: str | None = None,
) -> dict[str, object]:
    """Create and validate a declarative specification for one specialist agent."""
    spec = AgentSpec(
        name=name,
        purpose=purpose,
        instructions=instructions,
        tools=tools or [],
        handoffs=handoffs or [],
        guardrails=guardrails or [],
        model=model,
    )
    return {
        "name": spec.name,
        "purpose": spec.purpose,
        "instructions": spec.instructions,
        "tools": spec.tools,
        "handoffs": spec.handoffs,
        "guardrails": spec.guardrails,
        "model": spec.model,
    }


@mcp.tool()
def design_multi_agent_system(
    name: str,
    goal: str,
    agents_json: str,
    architecture: str = "manager",
    persistence: str = "session",
    approval_policy: str = "sensitive-actions-require-approval",
) -> dict[str, object]:
    """Validate and normalize a complete multi-agent system design.

    agents_json must be a JSON array of objects containing at minimum:
    name, purpose, and instructions. Optional fields include model, tools,
    handoffs, guardrails, and output_schema.
    """
    raw = json.loads(agents_json)
    if not isinstance(raw, list):
        raise ValueError("agents_json must contain a JSON array")

    agents = [AgentSpec(**item) for item in raw]
    spec = SystemSpec(
        name=name,
        goal=goal,
        agents=agents,
        architecture=architecture,
        persistence=persistence,
        approval_policy=approval_policy,
    )
    return system_blueprint(spec)


@mcp.resource("builder://capabilities")
def builder_capabilities() -> str:
    """Describe the capability surface of the builder."""
    return json.dumps(
        {
            "role": "Autonomous Coding + Agents Builder",
            "capabilities": [
                "requirements_analysis",
                "system_architecture",
                "single_agent_design",
                "multi_agent_orchestration",
                "code_generation",
                "repo_modification",
                "test_execution",
                "failure_diagnosis",
                "automated_repair",
                "security_review",
                "deployment_design",
            ],
            "lifecycle": [
                "analyze",
                "architect",
                "plan",
                "implement",
                "test",
                "review",
                "repair",
                "verify",
                "finalize",
            ],
        },
        indent=2,
    )


def main() -> None:
    """Run the MCP server over Streamable HTTP."""
    mcp.run(
        transport="streamable-http",
        host=os.getenv("MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_PORT", "8000")),
    )


if __name__ == "__main__":
    main()

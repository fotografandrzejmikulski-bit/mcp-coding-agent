"""MCP server entry point for the autonomous Agents Builder."""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .agent_builder import AgentSpec, SystemSpec, system_blueprint
from .core.models import AgentRole, BuildPlan
from .core.planner import BuildPlanner
from .core.workspace import Workspace
from .orchestration.system import create_builder_system
from .tools.command import run_command
from .tools.filesystem import read_file, write_file

load_dotenv()

mcp = FastMCP(
    "mcp-coding-agent",
    instructions=(
        "You are an autonomous principal coding and AI-agent systems builder. "
        "Own complex tasks from requirements to verified completion. Analyze, architect, plan, implement, "
        "test, review, repair, secure, integrate and verify. Build single agents or complete multi-agent systems. "
        "Use tools deliberately, keep all execution scoped to an explicitly authorized workspace, and never claim "
        "success without evidence from verification."
    ),
)


@mcp.tool()
def health_check() -> dict[str, str]:
    """Return service health and builder identity."""
    return {"status": "ok", "service": "mcp-coding-agent", "role": "agents-builder"}


@mcp.tool()
def inspect_workspace(path: str) -> dict[str, object]:
    """Inspect a project directory using read-only metadata."""
    target = Path(path).expanduser().resolve()
    if not target.exists():
        return {"exists": False, "path": str(target)}
    children = sorted(item.name for item in target.iterdir())[:500] if target.is_dir() else []
    return {
        "exists": True,
        "path": str(target),
        "type": "directory" if target.is_dir() else "file",
        "name": target.name,
        "children": children,
    }


@mcp.tool()
def read_project_file(root: str, path: str, max_bytes: int = 200_000) -> dict[str, object]:
    """Read a UTF-8 project file inside the explicit workspace root."""
    return read_file(root, path, max_bytes)


@mcp.tool()
def write_project_file(root: str, path: str, content: str) -> dict[str, object]:
    """Write a UTF-8 project file inside the explicit workspace root."""
    return write_file(root, path, content)


@mcp.tool()
def execute_workspace_command(root: str, command: str, timeout: int = 120) -> dict[str, object]:
    """Execute one controlled command with the project directory as its working directory."""
    return run_command(root, command, timeout)


@mcp.tool()
def create_build_plan(
    name: str,
    goal: str,
    requirements: list[str] | None = None,
    constraints: list[str] | None = None,
) -> dict[str, object]:
    """Create a bounded build plan for a software or agent-system project."""
    roles = [
        AgentSpec(name="architect", purpose="Define architecture", instructions="Design the system", tools=[], handoffs=[], guardrails=[], model=None),
        AgentSpec(name="planner", purpose="Plan implementation", instructions="Create a dependency-aware implementation plan", tools=[], handoffs=[], guardrails=[], model=None),
        AgentSpec(name="coder", purpose="Implement", instructions="Write production code", tools=[], handoffs=[], guardrails=[], model=None),
        AgentSpec(name="tester", purpose="Verify", instructions="Test implementation", tools=[], handoffs=[], guardrails=[], model=None),
        AgentSpec(name="security", purpose="Assess security", instructions="Review threats and controls", tools=[], handoffs=[], guardrails=[], model=None),
        AgentSpec(name="debugger", purpose="Repair failures", instructions="Find root causes and repair regressions", tools=[], handoffs=[], guardrails=[], model=None),
        AgentSpec(name="reviewer", purpose="Review quality", instructions="Review correctness and maintainability", tools=[], handoffs=[], guardrails=[], model=None),
        AgentSpec(name="devops", purpose="Deploy", instructions="Define reproducible deployment", tools=[], handoffs=[], guardrails=[], model=None),
    ]
    from .core.models import SystemSpec as TypedSystemSpec
    typed = TypedSystemSpec(name=name, objective=goal, agents=[
        __import__("mcp_coding_agent.core.models", fromlist=["AgentSpec"]).AgentSpec(
            id=agent.name,
            name=agent.name,
            role=AgentRole.SPECIALIST,
            mission=agent.purpose,
        ) for agent in roles
    ], requirements=requirements or [], constraints=constraints or [])
    plan = BuildPlanner().create_plan(typed)
    return plan.model_dump()


@mcp.tool()
def design_agent(
    name: str,
    purpose: str,
    instructions: str,
    role: str = "specialist",
    tools: list[str] | None = None,
    handoffs: list[str] | None = None,
    guardrails: list[str] | None = None,
    model: str | None = None,
) -> dict[str, object]:
    """Create and validate a declarative specification for one agent."""
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
        "role": role,
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
    """Validate and normalize a complete multi-agent system design."""
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


@mcp.tool()
def get_builder_architecture() -> dict[str, object]:
    """Return the internal specialist architecture used by the runtime."""
    system = create_builder_system()
    return {
        "manager": system.manager.name,
        "specialists": [
            "System Architect",
            "Implementation Planner",
            "Senior Coding Agent",
            "Code Reviewer",
            "QA Engineer",
            "Debugging and Repair Agent",
            "Security Engineer",
            "DevOps Engineer",
        ],
        "orchestration": "manager-as-controller with specialist agents-as-tools",
    }


@mcp.resource("builder://capabilities")
def builder_capabilities() -> str:
    """Describe the builder capability surface."""
    return json.dumps(
        {
            "identity": "Autonomous AI Coding + Agents Builder",
            "capabilities": [
                "requirements_analysis",
                "architecture_design",
                "agent_design",
                "multi_agent_system_design",
                "implementation_planning",
                "workspace_scoped_code_editing",
                "command_execution",
                "testing",
                "debugging_and_repair",
                "code_review",
                "security_review",
                "deployment_design",
                "verification",
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

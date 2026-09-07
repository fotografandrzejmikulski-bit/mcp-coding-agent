"""Production MCP entry point for the autonomous Agents Builder."""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .agent_builder import AgentSpec, SystemSpec, system_blueprint
from .core.models import AgentRole, AgentSpec as RuntimeAgentSpec, SystemSpec as TypedSystemSpec
from .core.planner import BuildPlanner
from .mcp_tools import register_execution_tools
from .tools.builder import register_builder_tools
from .tools.generation import register_generation_tools
from .tools.state import register_state_tools

load_dotenv()

mcp = FastMCP(
    "mcp-coding-agent",
    instructions=(
        "You are an autonomous principal coding and AI-agent systems builder. "
        "Own complex engineering tasks from requirements to verified completion. "
        "Build individual agents or complete multi-agent systems. Analyze, architect, plan, "
        "implement, test, review, repair, secure, integrate and verify. Never claim success "
        "without verification evidence. Treat workspace scope and approval policy as hard boundaries."
    ),
)

register_execution_tools(mcp)
register_builder_tools(mcp)
register_generation_tools(mcp)
register_state_tools(mcp)


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> JSONResponse:
    """Unauthenticated deployment health check."""
    return JSONResponse({"status": "ok", "service": "mcp-coding-agent", "role": "agents-builder"})


@mcp.tool()
def health_check() -> dict[str, str]:
    """Return service health and builder identity through MCP."""
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
def create_build_plan(
    name: str,
    goal: str,
    requirements: list[str] | None = None,
    constraints: list[str] | None = None,
) -> dict[str, object]:
    """Create a deterministic baseline build plan for a software or agent-system project."""
    builtins = [
        ("architect", AgentRole.ARCHITECT, "Define architecture"),
        ("planner", AgentRole.PLANNER, "Plan implementation"),
        ("coder", AgentRole.CODER, "Implement"),
        ("tester", AgentRole.TESTER, "Verify"),
        ("security", AgentRole.SECURITY, "Assess security"),
        ("debugger", AgentRole.DEBUGGER, "Repair failures"),
        ("reviewer", AgentRole.REVIEWER, "Review quality"),
        ("devops", AgentRole.DEVOPS, "Deploy"),
    ]
    typed = TypedSystemSpec(
        name=name,
        objective=goal,
        requirements=requirements or [],
        constraints=constraints or [],
        agents=[
            RuntimeAgentSpec(id=agent_id, name=agent_id, role=role, mission=mission)
            for agent_id, role, mission in builtins
        ],
    )
    return BuildPlanner().create_plan(typed).model_dump()


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
        raise ValueError("agents_json must be a JSON array")
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
    """Return the specialist architecture of the runtime."""
    return {
        "manager": "Agents Builder Orchestrator",
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
                "git_inspection",
                "agent_system_generation",
                "durable_build_state",
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
                "security",
                "integrate",
                "verify",
                "finalize",
            ],
        },
        indent=2,
    )


app = mcp.streamable_http_app()


def main() -> None:
    """Run the MCP server over Streamable HTTP."""
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_PORT", "8000")),
    )


if __name__ == "__main__":
    main()

from mcp_coding_agent.core.models import AgentRole, AgentSpec, SystemSpec
from mcp_coding_agent.core.planner import BuildPlanner
from mcp_coding_agent.core.workspace import Workspace, WorkspaceError


def test_system_validation_and_plan() -> None:
    spec = SystemSpec(
        name="demo",
        objective="build a service",
        agents=[
            AgentSpec(id="architect", name="Architect", role=AgentRole.ARCHITECT, mission="Design"),
            AgentSpec(id="coder", name="Coder", role=AgentRole.CODER, mission="Implement", handoffs=["tester"]),
            AgentSpec(id="tester", name="Tester", role=AgentRole.TESTER, mission="Verify"),
        ],
    )
    plan = BuildPlanner().create_plan(spec)
    assert "implementation" in plan.phases
    assert "tests_pass" in plan.verification_gates


def test_workspace_blocks_escape(tmp_path) -> None:
    workspace = Workspace(str(tmp_path))
    workspace.write("a.txt", "hello")
    assert workspace.read("a.txt") == "hello"
    try:
        workspace.read("../outside.txt")
    except WorkspaceError:
        pass
    else:
        raise AssertionError("workspace escape was not blocked")

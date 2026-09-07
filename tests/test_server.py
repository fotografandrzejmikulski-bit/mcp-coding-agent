from mcp_coding_agent.server import create_build_plan, get_builder_architecture


def test_builder_architecture_exposes_manager_and_specialists() -> None:
    result = get_builder_architecture()
    assert result["manager"] == "Agents Builder Orchestrator"
    assert len(result["specialists"]) >= 8


def test_build_plan_contains_verification() -> None:
    result = create_build_plan("demo", "build a service")
    assert result["goal"] == "build a service"
    assert "integration_verification" in result["phases"]

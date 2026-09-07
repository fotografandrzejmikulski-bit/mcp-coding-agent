from mcp_coding_agent.server import health_check


def test_health_check_contract() -> None:
    result = health_check()
    assert result["status"] == "ok"
    assert result["service"] == "mcp-coding-agent"
    assert result["role"] == "agents-builder"

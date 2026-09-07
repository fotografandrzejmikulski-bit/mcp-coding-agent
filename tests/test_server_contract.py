def test_mcp_server_has_expected_routes() -> None:
    from mcp_coding_agent.server import app

    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/mcp" in paths
    assert "/health" in paths

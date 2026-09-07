# MCP Coding Agent — Autonomous Agents Builder

An autonomous AI engineering system exposed through Model Context Protocol (MCP).
It is designed to build production software, individual agents, and complete multi-agent systems.

## Architecture

The runtime uses a manager-style orchestrator with specialist agents for architecture, planning, coding,
review, QA, debugging, security, and DevOps. The OpenAI Agents SDK provides the agent runtime and
agent-as-tools orchestration; MCP provides interoperability with MCP hosts.

## Core lifecycle

1. Analyze requirements
2. Design architecture
3. Decompose into agents and components
4. Create implementation plan
5. Implement in an authorized workspace
6. Run tests
7. Review and diagnose failures
8. Repair and regression-test
9. Run security review
10. Verify integration
11. Finalize only with evidence

## MCP tools

- `health_check`
- `inspect_workspace`
- `read_project_file`
- `write_project_file`
- `execute_workspace_command`
- `create_build_plan`
- `design_agent`
- `design_multi_agent_system`
- `get_builder_architecture`

## Safety model

Workspace operations require an explicit project root. Paths are resolved and checked to prevent escape.
Command execution is deliberately restricted and strips sensitive API-key environment variables from child
processes. More granular command policy, approvals, secret redaction, sandboxing and audit logging are
planned as part of the execution-hardening layer.

## Development

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
mcp-coding-agent
```

Set `OPENAI_API_KEY` when running the agent runtime. MCP clients connect to the configured Streamable HTTP endpoint.

## Status

The repository contains the first executable architecture of the autonomous Agents Builder: typed domain
models, planning, specialist-agent definitions, manager orchestration, workspace-scoped execution and MCP tools.
The next hardening stage is production-grade sandbox execution, persistent project state, Git/GitHub operations,
verification loops, approval gates and deployment adapters.

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

### Builder
- `run_builder`
- `validate_agent_system`
- `generate_agent_system`
- `create_build_state`
- `get_build_state`

### Design
- `create_build_plan`
- `design_agent`
- `design_multi_agent_system`
- `get_builder_architecture`

### Coding / workspace
- `inspect_workspace`
- `read_project_file`
- `write_project_file`
- `execute_workspace_command`
- `inspect_git_status`
- `inspect_git_diff`

### Resources
- `builder://capabilities`
- `builder://tool-policy`

## Development

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
ruff check src tests
mcp-coding-agent
```

Set `OPENAI_API_KEY` when running the Agents SDK runtime. MCP clients connect to the configured Streamable HTTP endpoint.

## Security boundary

Workspace operations require an explicit project root and prevent path traversal. Command execution is
bounded and strips the OpenAI API key from child processes. Production deployment should additionally use
isolated containers/sandboxes, narrow command allowlists, authentication, secret management, resource limits,
and audited write paths.

## Current repository state

The repository now contains the first complete architectural slice of the autonomous Agents Builder:
- typed agent/system contracts;
- specialist-agent library;
- manager-style orchestration with agents-as-tools;
- dynamic agent graph materialization;
- adaptive planning;
- bounded repair loop;
- workspace-scoped filesystem and command execution;
- read-only Git inspection;
- deterministic agent-system generation;
- durable JSON build-state records;
- MCP tool/resource surface;
- Docker image and CI workflow.

The remaining production-hardening work is intentionally separated from this core: authenticated remote GitHub
write operations, isolated sandbox execution, richer persistent storage, deployment adapters, approval workflows,
full end-to-end verification and operational observability.

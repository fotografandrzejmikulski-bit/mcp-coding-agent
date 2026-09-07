# MCP Coding Agent — Autonomous Agents Builder

Autonomous AI engineering system exposed through Model Context Protocol (MCP). The Builder is designed to create production software, individual agents, and complete multi-agent systems.

## Architecture

The runtime uses a manager-style orchestrator with specialist agents for architecture, planning, coding, review, QA, debugging, security, and DevOps. The OpenAI Agents SDK provides the agent runtime and agent-as-tools orchestration; MCP provides interoperability with MCP hosts. citeturn601879search1turn601879search5

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

## MCP server

The server uses **Streamable HTTP**. The official MCP Python SDK exposes this transport as an ASGI application; the standard endpoint is `/mcp`. A separate `/health` route is provided for deployment health checks. citeturn601879search6

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
ruff check src tests
mcp-coding-agent
```

The default local endpoint is:

```text
http://127.0.0.1:8000/mcp
```

Health check:

```text
http://127.0.0.1:8000/health
```

Set `OPENAI_API_KEY` when running the Agents SDK runtime. OpenAI documents `openai-agents` as the installation package and `OPENAI_API_KEY` as the default credential path. citeturn601879search0turn601879search8

## Security boundary

Workspace operations require an explicit project root and prevent path traversal. Command execution is bounded, blocks high-risk binaries, and strips major cloud/API credentials from child-process environments. Production deployment should additionally use isolated containers/sandboxes, narrow command allowlists, secret management, resource limits, authentication, audited write paths, and explicit approval for consequential operations.

For real code-generation work in isolated environments, the current OpenAI Agents SDK also provides Sandbox Agents and Docker-backed sandbox execution. citeturn601879search2

## Deployment

A Dockerfile and `railway.json` are included. The container listens on port `8000` and exposes `/health` for deployment health checks.

## Current state

The repository contains the core executable architecture of the autonomous Agents Builder:

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
- Streamable HTTP MCP server;
- Docker image and CI workflow;
- deployment configuration for Railway.

The next engineering layer is production hardening of remote GitHub write operations, sandbox isolation, richer persistence, approval workflows and full end-to-end verification against the target MCP host. Those capabilities must be implemented and verified rather than merely described before production claims are made.

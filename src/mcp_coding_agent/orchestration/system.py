"""Multi-agent orchestration for complex build tasks."""

from __future__ import annotations

from dataclasses import dataclass

from agents import Agent

from mcp_coding_agent.agents.specialists import (
    architect_agent,
    coder_agent,
    debugger_agent,
    devops_agent,
    planner_agent,
    reviewer_agent,
    security_agent,
    tester_agent,
)
from mcp_coding_agent.core.prompts import BUILDER_SYSTEM_PROMPT


@dataclass(slots=True)
class BuilderSystem:
    """A manager-style system that retains control while delegating to specialists."""

    manager: Agent


def create_builder_system() -> BuilderSystem:
    architect = architect_agent()
    planner = planner_agent()
    coder = coder_agent()
    reviewer = reviewer_agent()
    tester = tester_agent()
    debugger = debugger_agent()
    security = security_agent()
    devops = devops_agent()

    manager = Agent(
        name="Agents Builder Orchestrator",
        instructions=BUILDER_SYSTEM_PROMPT,
        tools=[
            architect.as_tool(tool_name="architect", tool_description="Design system architecture and boundaries."),
            planner.as_tool(tool_name="planner", tool_description="Create an implementation plan and acceptance gates."),
            coder.as_tool(tool_name="coder", tool_description="Implement production-quality code."),
            reviewer.as_tool(tool_name="reviewer", tool_description="Review code for correctness and maintainability."),
            tester.as_tool(tool_name="tester", tool_description="Design and analyze tests and verification."),
            debugger.as_tool(tool_name="debugger", tool_description="Diagnose and repair implementation failures."),
            security.as_tool(tool_name="security", tool_description="Perform security analysis and threat review."),
            devops.as_tool(tool_name="devops", tool_description="Design build, deployment and operational workflows."),
        ],
    )
    return BuilderSystem(manager=manager)

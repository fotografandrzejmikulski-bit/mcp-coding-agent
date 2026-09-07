"""Core orchestration primitives for the MCP Coding / Agents Builder."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class TaskPhase(StrEnum):
    """Lifecycle phases used by the builder."""

    ANALYZE = "analyze"
    ARCHITECT = "architect"
    PLAN = "plan"
    IMPLEMENT = "implement"
    TEST = "test"
    REVIEW = "review"
    REPAIR = "repair"
    VERIFY = "verify"
    FINALIZE = "finalize"


@dataclass(slots=True)
class AgentSpec:
    """Declarative specification of an agent the builder should create."""

    name: str
    purpose: str
    instructions: str
    model: str | None = None
    tools: list[str] = field(default_factory=list)
    handoffs: list[str] = field(default_factory=list)
    guardrails: list[str] = field(default_factory=list)
    output_schema: dict[str, Any] | None = None


@dataclass(slots=True)
class SystemSpec:
    """Declarative specification of a complete multi-agent system."""

    name: str
    goal: str
    agents: list[AgentSpec] = field(default_factory=list)
    architecture: str = "manager"
    persistence: str = "session"
    approval_policy: str = "sensitive-actions-require-approval"


class BuilderError(RuntimeError):
    """Raised when a builder operation is invalid."""


def validate_agent_spec(spec: AgentSpec) -> None:
    """Validate the minimum contract for an agent specification."""
    if not spec.name.strip():
        raise BuilderError("Agent name cannot be empty")
    if not spec.purpose.strip():
        raise BuilderError(f"Agent '{spec.name}' must define a purpose")
    if not spec.instructions.strip():
        raise BuilderError(f"Agent '{spec.name}' must define instructions")


def validate_system_spec(spec: SystemSpec) -> None:
    """Validate a multi-agent system before code generation."""
    if not spec.name.strip():
        raise BuilderError("System name cannot be empty")
    if not spec.goal.strip():
        raise BuilderError("System goal cannot be empty")
    if not spec.agents:
        raise BuilderError("System must contain at least one agent")

    names: set[str] = set()
    for agent in spec.agents:
        validate_agent_spec(agent)
        normalized = agent.name.strip().lower()
        if normalized in names:
            raise BuilderError(f"Duplicate agent name: {agent.name}")
        names.add(normalized)

    known = {agent.name for agent in spec.agents}
    for agent in spec.agents:
        unknown = set(agent.handoffs) - known
        if unknown:
            raise BuilderError(
                f"Agent '{agent.name}' references unknown handoffs: {sorted(unknown)}"
            )


def system_blueprint(spec: SystemSpec) -> dict[str, Any]:
    """Produce a normalized blueprint that later generators can consume."""
    validate_system_spec(spec)
    return {
        "name": spec.name,
        "goal": spec.goal,
        "architecture": spec.architecture,
        "persistence": spec.persistence,
        "approval_policy": spec.approval_policy,
        "agents": [
            {
                "name": agent.name,
                "purpose": agent.purpose,
                "instructions": agent.instructions,
                "model": agent.model,
                "tools": list(agent.tools),
                "handoffs": list(agent.handoffs),
                "guardrails": list(agent.guardrails),
                "output_schema": agent.output_schema,
            }
            for agent in spec.agents
        ],
        "lifecycle": [phase.value for phase in TaskPhase],
    }

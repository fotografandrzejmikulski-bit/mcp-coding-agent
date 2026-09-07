"""Core domain models for the autonomous Agents Builder."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class AgentRole(StrEnum):
    ORCHESTRATOR = "orchestrator"
    ARCHITECT = "architect"
    PLANNER = "planner"
    CODER = "coder"
    REVIEWER = "reviewer"
    TESTER = "tester"
    DEBUGGER = "debugger"
    SECURITY = "security"
    DEVOPS = "devops"
    RESEARCHER = "researcher"
    SPECIALIST = "specialist"


class AgentSpec(BaseModel):
    id: str = Field(min_length=1, pattern=r"^[a-z0-9_\-]+$")
    name: str
    role: AgentRole
    mission: str
    responsibilities: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    handoffs: list[str] = Field(default_factory=list)
    model: str | None = None
    max_iterations: int = Field(default=20, ge=1, le=200)


class SystemSpec(BaseModel):
    name: str
    objective: str
    agents: list[AgentSpec]
    execution_mode: str = "adaptive"
    requirements: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def validate_graph(self) -> None:
        ids = {agent.id for agent in self.agents}
        if len(ids) != len(self.agents):
            raise ValueError("Agent IDs must be unique")
        for agent in self.agents:
            missing = set(agent.handoffs) - ids
            if missing:
                raise ValueError(f"Agent {agent.id} references unknown agents: {sorted(missing)}")


class BuildPlan(BaseModel):
    goal: str
    phases: list[str]
    agents: list[str]
    artifacts: list[str] = Field(default_factory=list)
    verification_gates: list[str] = Field(default_factory=list)
    risk_controls: list[str] = Field(default_factory=list)


class ExecutionEvent(BaseModel):
    event_type: str
    message: str
    agent_id: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


class BuildResult(BaseModel):
    success: bool
    summary: str
    artifacts: list[str] = Field(default_factory=list)
    failures: list[str] = Field(default_factory=list)
    events: list[ExecutionEvent] = Field(default_factory=list)

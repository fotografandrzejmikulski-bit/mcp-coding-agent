"""Dynamic registry and factory for specialist agents."""

from __future__ import annotations

from agents import Agent

from mcp_coding_agent.core.models import AgentSpec


class AgentRegistry:
    """Materialize Agent SDK agents from validated AgentSpec definitions."""

    def __init__(self) -> None:
        self._specs: dict[str, AgentSpec] = {}
        self._agents: dict[str, Agent] = {}

    def register_spec(self, spec: AgentSpec) -> None:
        if spec.id in self._specs:
            raise ValueError(f"Agent already registered: {spec.id}")
        self._specs[spec.id] = spec

    def build(self, agent_id: str) -> Agent:
        if agent_id in self._agents:
            return self._agents[agent_id]
        spec = self._specs[agent_id]
        agent = Agent(
            name=spec.name,
            instructions=(
                f"Mission: {spec.mission}\n"
                f"Responsibilities: {', '.join(spec.responsibilities) or 'none'}\n"
                "Operate only through explicitly provided tools. Verify claims and artifacts before finalizing."
            ),
            model=spec.model,
        )
        self._agents[agent_id] = agent
        return agent

    def get(self, agent_id: str) -> Agent:
        return self.build(agent_id)

    def ids(self) -> list[str]:
        return sorted(self._specs)

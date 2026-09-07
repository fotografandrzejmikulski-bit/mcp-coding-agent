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

    def register_many(self, specs: list[AgentSpec]) -> None:
        ids = [spec.id for spec in specs]
        if len(ids) != len(set(ids)):
            raise ValueError("Agent IDs must be unique")
        for spec in specs:
            self.register_spec(spec)

    def build(self, agent_id: str) -> Agent:
        if agent_id in self._agents:
            return self._agents[agent_id]
        spec = self._specs[agent_id]
        agent = Agent(
            name=spec.name,
            instructions=(
                f"Role: {spec.role.value}.\n"
                f"Mission: {spec.mission}\n"
                f"Responsibilities: {', '.join(spec.responsibilities) or 'none'}\n"
                f"Declared capabilities: {', '.join(spec.tools) or 'none'}\n"
                "Operate only within the system's policy. Verify work before claiming completion."
            ),
            model=spec.model,
        )
        self._agents[agent_id] = agent
        return agent

    def build_graph(self) -> dict[str, Agent]:
        for agent_id in self._specs:
            self.build(agent_id)
        for agent_id, spec in self._specs.items():
            self._agents[agent_id].handoffs = [self._agents[target] for target in spec.handoffs]
        return dict(self._agents)

    def get(self, agent_id: str) -> Agent:
        return self.build(agent_id)

    def ids(self) -> list[str]:
        return sorted(self._specs)

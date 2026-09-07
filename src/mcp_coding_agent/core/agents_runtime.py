"""Runtime wiring for dynamic multi-agent systems."""

from __future__ import annotations

from agents import Agent

from .models import AgentSpec, AgentRole


class AgentRuntimeFactory:
    """Convert validated declarative agent specs into executable Agents SDK agents."""

    def build(self, specs: list[AgentSpec]) -> dict[str, Agent]:
        by_id: dict[str, Agent] = {}
        for spec in specs:
            by_id[spec.id] = Agent(
                name=spec.name,
                instructions=self._instructions(spec),
                model=spec.model,
            )

        # Handoffs are resolved after every agent exists.
        for spec in specs:
            target_agents = [by_id[target] for target in spec.handoffs]
            by_id[spec.id].handoffs = target_agents
        return by_id

    @staticmethod
    def _instructions(spec: AgentSpec) -> str:
        return (
            f"Role: {spec.role.value}.\n"
            f"Mission: {spec.mission}\n"
            f"Responsibilities: {', '.join(spec.responsibilities) or 'none specified'}\n"
            f"Allowed capability labels: {', '.join(spec.tools) or 'none specified'}\n"
            "Respect the system's workspace and approval boundaries. Verify work before reporting completion."
        )


def is_orchestrator(spec: AgentSpec) -> bool:
    return spec.role == AgentRole.ORCHESTRATOR

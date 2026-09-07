"""Preflight validation of agent-system blueprints."""

from __future__ import annotations

from collections import defaultdict

from mcp_coding_agent.core.models import SystemSpec


class ValidationError(ValueError):
    """Raised for invalid system topology."""


def validate_system(spec: SystemSpec) -> list[str]:
    spec.validate_graph()
    ids = {agent.id for agent in spec.agents}
    warnings: list[str] = []
    incoming: dict[str, int] = defaultdict(int)
    for agent in spec.agents:
        for target in agent.handoffs:
            incoming[target] += 1
    if not any(agent.role.value == "orchestrator" for agent in spec.agents):
        warnings.append("No explicit orchestrator role is defined; consider adding one for complex systems.")
    unreachable = sorted(agent.id for agent in spec.agents if agent.id not in incoming and agent.role.value != "orchestrator")
    if len(spec.agents) > 1 and unreachable:
        warnings.append(f"Agents with no incoming delegation edge: {unreachable}")
    return warnings

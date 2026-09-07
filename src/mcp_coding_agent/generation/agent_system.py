"""Generate a portable blueprint for a multi-agent project."""

from __future__ import annotations

import json
from dataclasses import dataclass

from mcp_coding_agent.core.models import SystemSpec


@dataclass(frozen=True, slots=True)
class GeneratedArtifact:
    path: str
    content: str


class AgentSystemGenerator:
    """Convert validated system specifications into deterministic project artifacts."""

    def generate(self, spec: SystemSpec) -> list[GeneratedArtifact]:
        spec.validate_graph()
        return [
            GeneratedArtifact("agent-system.json", json.dumps(spec.model_dump(mode="json"), indent=2)),
            GeneratedArtifact("ARCHITECTURE.md", self._architecture(spec)),
        ]

    @staticmethod
    def _architecture(spec: SystemSpec) -> str:
        lines = [f"# {spec.name}", "", spec.objective, "", "## Agents", ""]
        for agent in spec.agents:
            lines.extend(
                [
                    f"### {agent.name} (`{agent.id}`)",
                    f"Role: `{agent.role.value}`",
                    f"Mission: {agent.mission}",
                    f"Tools: {', '.join(agent.tools) or 'none'}",
                    f"Handoffs: {', '.join(agent.handoffs) or 'none'}",
                    "",
                ]
            )
        lines.extend(["## Execution", "", f"Mode: `{spec.execution_mode}`"])
        return "\n".join(lines) + "\n"

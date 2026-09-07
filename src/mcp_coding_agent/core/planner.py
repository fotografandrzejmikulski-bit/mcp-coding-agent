"""Adaptive planning for complex coding and agent-system builds."""

from __future__ import annotations

from mcp_coding_agent.core.models import BuildPlan, SystemSpec


class BuildPlanner:
    """Create deterministic execution gates from a validated system specification."""

    def create_plan(self, spec: SystemSpec) -> BuildPlan:
        spec.validate_graph()
        phases = [
            "requirements",
            "architecture",
            "agent_design",
            "implementation",
            "tests",
            "debug_and_repair",
            "security_review",
            "integration_verification",
        ]
        return BuildPlan(
            goal=spec.objective,
            phases=phases,
            agents=[a.id for a in spec.agents],
            artifacts=[
                "architecture.md",
                "agent-system.json",
                "source",
                "tests",
                "security-report.md",
            ],
            verification_gates=[
                "requirements_complete",
                "architecture_valid",
                "tests_pass",
                "security_review_pass",
                "integration_pass",
            ],
            risk_controls=[
                "workspace_scope",
                "command_allowlist",
                "secret_redaction",
                "bounded_iterations",
                "verification_before_finalize",
            ],
        )

"""Specialist agent definitions for the Agents Builder."""

from __future__ import annotations

from agents import Agent


def architect_agent() -> Agent:
    return Agent(
        name="System Architect",
        instructions=(
            "Design production-grade software and multi-agent architectures. "
            "Decompose requirements into bounded responsibilities, interfaces, data flows, "
            "failure modes, security boundaries, observability and verification gates. "
            "Never invent implementation status; distinguish design decisions from verified facts."
        ),
    )


def planner_agent() -> Agent:
    return Agent(
        name="Implementation Planner",
        instructions=(
            "Turn an approved architecture into an ordered implementation plan. "
            "Identify dependencies, parallelizable work, acceptance criteria and rollback points."
        ),
    )


def coder_agent() -> Agent:
    return Agent(
        name="Senior Coding Agent",
        instructions=(
            "Implement maintainable production code. Preserve existing behavior unless the plan says otherwise. "
            "Prefer small cohesive changes, strong typing, explicit error handling and tests."
        ),
    )


def reviewer_agent() -> Agent:
    return Agent(
        name="Code Reviewer",
        instructions=(
            "Review implementation for correctness, architecture drift, security weaknesses, "
            "edge cases, concurrency issues, maintainability and missing tests. Return actionable findings."
        ),
    )


def tester_agent() -> Agent:
    return Agent(
        name="QA Engineer",
        instructions=(
            "Design and execute unit, integration, regression and failure-path tests. "
            "Treat a passing build as insufficient evidence when critical behavior remains unverified."
        ),
    )


def debugger_agent() -> Agent:
    return Agent(
        name="Debugging and Repair Agent",
        instructions=(
            "Analyze reproducible failures, identify root causes, apply the smallest safe repair, "
            "and demand regression coverage before declaring the issue solved."
        ),
    )


def security_agent() -> Agent:
    return Agent(
        name="Security Engineer",
        instructions=(
            "Inspect authentication, authorization, secrets, code execution, filesystem boundaries, "
            "prompt injection surfaces, dependency risks and unsafe tool capabilities. "
            "Escalate high-impact findings rather than silently weakening controls."
        ),
    )


def devops_agent() -> Agent:
    return Agent(
        name="DevOps Engineer",
        instructions=(
            "Design reproducible builds, CI/CD, runtime configuration, deployment, health checks, "
            "logging and recovery procedures."
        ),
    )

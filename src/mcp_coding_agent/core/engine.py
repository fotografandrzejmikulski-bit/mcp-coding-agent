"""Build execution state machine."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from mcp_coding_agent.core.models import BuildPlan, BuildResult, ExecutionEvent, SystemSpec


Handler = Callable[[SystemSpec], dict[str, Any] | None]


class BuildEngine:
    """Execute build phases with bounded failure handling and verification gates."""

    def __init__(self, max_repair_cycles: int = 3) -> None:
        self.max_repair_cycles = max_repair_cycles
        self.handlers: dict[str, Handler] = {}

    def register(self, phase: str, handler: Handler) -> None:
        self.handlers[phase] = handler

    def execute(self, spec: SystemSpec, plan: BuildPlan) -> BuildResult:
        events: list[ExecutionEvent] = []
        failures: list[str] = []
        artifacts: list[str] = []

        for phase in plan.phases:
            events.append(ExecutionEvent(event_type="phase_started", message=phase))
            handler = self.handlers.get(phase)
            if handler is None:
                # Planning phases can remain declarative until their executable specialist exists.
                events.append(
                    ExecutionEvent(
                        event_type="phase_deferred",
                        message=f"No runtime handler registered for phase: {phase}",
                    )
                )
                continue
            try:
                result = handler(spec) or {}
                artifacts.extend(str(item) for item in result.get("artifacts", []))
                events.append(
                    ExecutionEvent(
                        event_type="phase_completed",
                        message=phase,
                        data=result,
                    )
                )
            except Exception as exc:  # noqa: BLE001 - engine converts phase errors into build events
                message = f"{phase}: {type(exc).__name__}: {exc}"
                failures.append(message)
                events.append(
                    ExecutionEvent(
                        event_type="phase_failed",
                        message=message,
                    )
                )
                if phase not in {"debug_and_repair", "tests", "security_review", "integration_verification"}:
                    break

        success = not failures and self._verification_satisfied(events, plan)
        return BuildResult(
            success=success,
            summary=("Build completed and verification gates passed." if success else "Build requires repair or additional execution."),
            artifacts=sorted(set(artifacts)),
            failures=failures,
            events=events,
        )

    @staticmethod
    def _verification_satisfied(events: list[ExecutionEvent], plan: BuildPlan) -> bool:
        completed = {event.message for event in events if event.event_type == "phase_completed"}
        if "tests_pass" in plan.verification_gates and "tests" in plan.phases:
            # A future test handler can explicitly emit tests_pass; until then the gate is conservative.
            if "tests" in completed and not any(
                event.event_type == "verification" and event.message == "tests_pass" for event in events
            ):
                return False
        return not any(event.event_type == "phase_failed" for event in events)

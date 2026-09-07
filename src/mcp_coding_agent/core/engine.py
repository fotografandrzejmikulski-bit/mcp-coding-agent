"""Build execution state machine with explicit verification gates."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from mcp_coding_agent.core.models import BuildPlan, BuildResult, ExecutionEvent, SystemSpec


Handler = Callable[[SystemSpec], dict[str, Any] | None]


class BuildEngine:
    """Execute registered build phases and require explicit verification evidence."""

    def __init__(self, max_repair_cycles: int = 3) -> None:
        if max_repair_cycles < 0 or max_repair_cycles > 20:
            raise ValueError("max_repair_cycles must be between 0 and 20")
        self.max_repair_cycles = max_repair_cycles
        self.handlers: dict[str, Handler] = {}

    def register(self, phase: str, handler: Handler) -> None:
        if not phase.strip():
            raise ValueError("phase cannot be empty")
        self.handlers[phase] = handler

    def execute(self, spec: SystemSpec, plan: BuildPlan) -> BuildResult:
        events: list[ExecutionEvent] = []
        failures: list[str] = []
        artifacts: list[str] = []
        repair_cycles = 0

        for phase in plan.phases:
            events.append(ExecutionEvent(event_type="phase_started", message=phase))
            handler = self.handlers.get(phase)
            if handler is None:
                events.append(ExecutionEvent(event_type="phase_deferred", message=phase))
                continue

            try:
                result = handler(spec) or {}
                artifacts.extend(str(item) for item in result.get("artifacts", []))
                events.extend(self._events_from_result(phase, result))

                if phase == "debug_and_repair":
                    repair_cycles += 1
                    if repair_cycles > self.max_repair_cycles:
                        failures.append("maximum repair cycles exceeded")
                        events.append(
                            ExecutionEvent(
                                event_type="phase_failed",
                                message="maximum repair cycles exceeded",
                            )
                        )
                        break
            except Exception as exc:  # noqa: BLE001 - convert phase exceptions into evidence
                message = f"{phase}: {type(exc).__name__}: {exc}"
                failures.append(message)
                events.append(ExecutionEvent(event_type="phase_failed", message=message))
                if phase not in {"tests", "debug_and_repair", "security_review", "integration_verification"}:
                    break

        gate_status = self._verification_status(events, plan)
        for gate, passed in gate_status.items():
            events.append(
                ExecutionEvent(
                    event_type="verification",
                    message=gate,
                    data={"passed": passed},
                )
            )

        success = not failures and all(gate_status.values())
        return BuildResult(
            success=success,
            summary=("Build completed and all verification gates passed." if success else "Build is not verified."),
            artifacts=sorted(set(artifacts)),
            failures=failures,
            events=events,
        )

    @staticmethod
    def _events_from_result(phase: str, result: dict[str, Any]) -> list[ExecutionEvent]:
        events = [ExecutionEvent(event_type="phase_completed", message=phase, data=result)]
        for gate in result.get("verification_passed", []):
            events.append(ExecutionEvent(event_type="verification", message=str(gate), data={"passed": True}))
        for gate in result.get("verification_failed", []):
            events.append(ExecutionEvent(event_type="verification", message=str(gate), data={"passed": False}))
        return events

    @staticmethod
    def _verification_status(
        events: list[ExecutionEvent], plan: BuildPlan
    ) -> dict[str, bool]:
        status = {gate: False for gate in plan.verification_gates}
        for event in events:
            if event.event_type != "verification" or event.message not in status:
                continue
            status[event.message] = bool(event.data.get("passed", False))
        return status

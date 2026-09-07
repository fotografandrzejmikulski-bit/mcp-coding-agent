"""Evidence-driven test/repair loop used by the builder."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RepairAttempt:
    number: int
    result: dict[str, Any]


@dataclass(slots=True)
class RepairLoopResult:
    success: bool
    attempts: list[RepairAttempt] = field(default_factory=list)
    final_result: dict[str, Any] = field(default_factory=dict)


class RepairLoop:
    """Run test -> diagnose -> repair until verification succeeds or the bound is exhausted."""

    def __init__(self, max_cycles: int = 3) -> None:
        self.max_cycles = max_cycles

    def run(
        self,
        test: Callable[[], dict[str, Any]],
        diagnose: Callable[[dict[str, Any]], dict[str, Any]],
        repair: Callable[[dict[str, Any]], dict[str, Any]],
    ) -> RepairLoopResult:
        attempts: list[RepairAttempt] = []
        result = test()
        if self._passed(result):
            return RepairLoopResult(success=True, attempts=attempts, final_result=result)

        for cycle in range(1, self.max_cycles + 1):
            diagnosis = diagnose(result)
            repair_result = repair(diagnosis)
            attempts.append(
                RepairAttempt(
                    number=cycle,
                    result={"diagnosis": diagnosis, "repair": repair_result},
                )
            )
            result = test()
            if self._passed(result):
                return RepairLoopResult(success=True, attempts=attempts, final_result=result)

        return RepairLoopResult(success=False, attempts=attempts, final_result=result)

    @staticmethod
    def _passed(result: dict[str, Any]) -> bool:
        return result.get("success") is True or result.get("returncode") == 0

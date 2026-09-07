"""Policy gates for autonomous execution."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionPolicy:
    max_command_timeout: int = 600
    max_output_chars: int = 20_000
    require_explicit_workspace: bool = True
    require_verification_before_finalize: bool = True


class PolicyViolation(RuntimeError):
    """Raised when an execution request violates policy."""


def validate_command(policy: ExecutionPolicy, command: str, timeout: int) -> None:
    if policy.require_explicit_workspace and not command.strip():
        raise PolicyViolation("Command cannot be empty")
    if timeout < 1 or timeout > policy.max_command_timeout:
        raise PolicyViolation("Command timeout exceeds execution policy")


def validate_finalize(policy: ExecutionPolicy, verified: bool) -> None:
    if policy.require_verification_before_finalize and not verified:
        raise PolicyViolation("Cannot finalize without verification evidence")

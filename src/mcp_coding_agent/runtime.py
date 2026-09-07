"""Runtime entrypoint for the autonomous Agents Builder."""

from __future__ import annotations

import asyncio
import os

from agents import Runner

from .orchestration.system import create_builder_system


async def run_builder(task: str) -> str:
    """Run the principal builder against a task using the specialist tool system."""
    if not task.strip():
        raise ValueError("task cannot be empty")
    system = create_builder_system()
    result = await Runner.run(system.manager, task.strip())
    return result.final_output


def main() -> None:
    task = os.getenv("BUILDER_TASK")
    if not task:
        raise SystemExit("Set BUILDER_TASK to execute the autonomous builder")
    print(asyncio.run(run_builder(task)))

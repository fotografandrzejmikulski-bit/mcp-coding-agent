"""Function tools used by the autonomous builder for authorized workspaces."""

from __future__ import annotations

from agents import function_tool

from ..core.workspace import Workspace


@function_tool
def read_workspace_file(root: str, path: str, max_bytes: int = 200_000) -> str:
    """Read a project file inside the explicitly authorized workspace."""
    return Workspace(root).read(path, max_bytes=max_bytes)


@function_tool
def write_workspace_file(root: str, path: str, content: str) -> str:
    """Write a project file inside the explicitly authorized workspace."""
    return Workspace(root).write(path, content)


@function_tool
def run_workspace_command(root: str, command: str, timeout: int = 120) -> dict[str, object]:
    """Run a policy-checked command inside the explicitly authorized workspace."""
    return Workspace(root).run(command, timeout=timeout)

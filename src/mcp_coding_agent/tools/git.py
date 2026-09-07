"""MCP-facing Git operations."""

from __future__ import annotations

from mcp_coding_agent.core.github_ops import git


def git_status(root: str) -> dict[str, object]:
    return git(root, "status", "--short", "--branch")


def git_diff(root: str, staged: bool = False) -> dict[str, object]:
    return git(root, "diff", "--cached" if staged else "--")

"""Git helpers for repository-aware agent workflows."""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    """Raised for git operation failures."""


def git(root: str, *args: str) -> dict[str, object]:
    repo = Path(root).expanduser().resolve()
    if not repo.exists() or not repo.is_dir():
        raise GitError(f"Workspace does not exist: {repo}")
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    result = {"args": list(args), "returncode": proc.returncode, "stdout": proc.stdout[-20000:], "stderr": proc.stderr[-20000:]}
    if proc.returncode != 0:
        raise GitError(proc.stderr.strip() or f"git exited with {proc.returncode}")
    return result

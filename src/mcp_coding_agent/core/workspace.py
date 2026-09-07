"""Workspace-scoped filesystem and command execution primitives."""

from __future__ import annotations

import os
import shlex
import subprocess
from pathlib import Path


class WorkspaceError(RuntimeError):
    """Raised when a workspace operation violates policy."""


class Workspace:
    """Constrain filesystem and process operations to one explicit root."""

    BLOCKED_BINARIES = {
        "sudo",
        "shutdown",
        "reboot",
        "mkfs",
        "mount",
        "umount",
        "passwd",
        "useradd",
        "userdel",
        "chmod",
        "chown",
    }

    SECRET_ENV_KEYS = {
        "OPENAI_API_KEY",
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "RAILWAY_TOKEN",
    }

    def __init__(self, root: str) -> None:
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, relative_path: str) -> Path:
        candidate = (self.root / relative_path).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as exc:
            raise WorkspaceError("Path escapes the configured workspace") from exc
        return candidate

    def read(self, relative_path: str, max_bytes: int = 200_000) -> str:
        if max_bytes < 1 or max_bytes > 5_000_000:
            raise WorkspaceError("max_bytes must be between 1 and 5,000,000")
        target = self.resolve(relative_path)
        if not target.is_file():
            raise WorkspaceError(f"Not a file: {relative_path}")
        return target.read_text(encoding="utf-8")[:max_bytes]

    def write(self, relative_path: str, content: str) -> str:
        target = self.resolve(relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return str(target.relative_to(self.root))

    def run(self, command: str, timeout: int = 120) -> dict[str, object]:
        if timeout < 1 or timeout > 600:
            raise WorkspaceError("timeout must be between 1 and 600 seconds")
        argv = shlex.split(command)
        if not argv:
            raise WorkspaceError("Command cannot be empty")
        if argv[0] in self.BLOCKED_BINARIES:
            raise WorkspaceError(f"Blocked command: {argv[0]}")
        env = os.environ.copy()
        for key in self.SECRET_ENV_KEYS:
            env.pop(key, None)
        try:
            proc = subprocess.run(
                argv,
                cwd=self.root,
                env=env,
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            return {
                "command": command,
                "returncode": 124,
                "stdout": (exc.stdout or "")[-20_000:],
                "stderr": (exc.stderr or "")[-20_000:],
                "timed_out": True,
            }
        return {
            "command": command,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-20_000:],
            "stderr": proc.stderr[-20_000:],
            "timed_out": False,
        }

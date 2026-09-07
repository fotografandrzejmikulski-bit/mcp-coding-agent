"""Small durable JSON store for build metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonStore:
    """Persist builder state as individual JSON documents under a dedicated directory."""

    def __init__(self, root: str) -> None:
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, key: str, value: dict[str, Any]) -> str:
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in key)
        target = self.root / f"{safe}.json"
        target.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")
        return str(target)

    def get(self, key: str) -> dict[str, Any] | None:
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in key)
        target = self.root / f"{safe}.json"
        if not target.is_file():
            return None
        return json.loads(target.read_text(encoding="utf-8"))

"""Minimal local smoke test for the MCP HTTP service."""

from __future__ import annotations

import json
import urllib.request


BASE = "http://127.0.0.1:8000"


def main() -> None:
    with urllib.request.urlopen(f"{BASE}/health", timeout=5) as response:
        payload = json.load(response)
    assert payload["status"] == "ok"
    print(json.dumps(payload, indent=2))
    print("MCP HTTP smoke test passed")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Sequence permutation helper for documentation examples."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def span_tag(body: str, kit_id: str, gen_marker: int) -> str:
    payload = f"{body}|{kit_id}|{gen_marker}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("fixtures/window_a.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps({"window": data.get("window_id"), "count": len(data.get("steps", []))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

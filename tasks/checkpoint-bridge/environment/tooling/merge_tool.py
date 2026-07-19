#!/usr/bin/env python3
"""Merge window helper for documentation examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("fixtures/rb_policy.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps({"overlap": data.get("overlap"), "ranks": data.get("cleanup_rank", [])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

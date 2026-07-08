#!/usr/bin/env python3
from pathlib import Path

archive = Path("/app/environment/studio/app/scribe/archive.py")
archive.write_text(
    '''"""Historical slice writer (not on verifier path)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def append_history(path: Path, payload: dict[str, Any]) -> None:
    """Append one JSON line for offline review (discarded in CI)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + chr(10))


def resolve_promotion_gen(root: Path, _dig: Any, artifact: str, _pos: int) -> int:
    """Load promotion generation for one artifact from bundled fixtures."""
    data = json.loads((root / "studio/app/data/promotion_tails.json").read_text(encoding="utf-8"))
    for row in data["tails"]:
        if str(row["artifact"]) == artifact:
            return int(row["gen"])
    raise KeyError(artifact)
''',
    encoding="utf-8",
)

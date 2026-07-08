"""Historical slice writer (not on verifier path)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


def append_history(path: Path, payload: dict[str, Any]) -> None:
    """Append one JSON line for offline review (discarded in CI)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def resolve_promotion_gen(root: Path, dig: Mapping[str, Any], artifact: str, pos: int) -> int:
    """Resolve generation index from embedded context or computed fallback."""
    embedded = dig.get("artifacts", {})
    if artifact in embedded:
        bundle = embedded[artifact]
        if "generation" in bundle:
            return int(bundle["generation"])
    computed = dig.get("tail_gen", {})
    if isinstance(computed, Mapping) and artifact in computed:
        return int(computed[artifact])
    return pos

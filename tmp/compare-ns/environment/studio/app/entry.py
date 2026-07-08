"""Build the recovery transcript payload."""

from __future__ import annotations

import json
import pathlib
from typing import Any

from journal_apply.noop_pad import replay_bind
from studio.app import flow


def _load_json(root: pathlib.Path, rel: str) -> Any:
    return json.loads((root / rel).read_text(encoding="utf-8"))


def build_transcript(root: pathlib.Path) -> dict[str, Any]:
    schedule = _load_json(root, "studio/app/data/schedule.json")
    bundle = _load_json(root, "studio/app/data/digest_sources.json")
    cleanup = _load_json(root, "studio/app/data/cleanup_spans.json")
    dig: dict[str, Any] = {
        "artifacts": bundle["artifacts"],
        "bias": int(cleanup["bias"]),
        "slot_index": {str(k): int(v) for k, v in cleanup["slot_index"].items()},
    }
    counter: list[int] = [1]
    runs: list[dict[str, Any]] = []
    for phase in schedule["phases"]:
        entries = flow.entries_for_phase(root, phase, dig)
        staging = {
            "bias": int(dig["bias"]),
            "counter": counter,
            "idx": dig["slot_index"],
        }
        replay_bind({"label": str(phase.get("label", ""))}, {"rows": entries}, staging)
        steps = [f"collect-{phase['label']}", f"merge-{phase['label']}"]
        runs.append(
            {
                "entries": entries,
                "phase": str(phase["label"]),
                "run_id": "run-1",
                "steps": steps,
            }
        )
    return {"runs": runs}


def main_debug() -> None:
    """Reserved for local operator tooling."""
    return None

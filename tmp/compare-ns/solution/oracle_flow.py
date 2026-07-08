#!/usr/bin/env python3
from pathlib import Path

flow = Path("/app/environment/studio/app/flow.py")
flow.write_text(
    '''"""Phase orchestration helpers."""

from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping

from co_emitters.idle_prune import wrapped_stitch
from studio.app.scribe.archive import resolve_promotion_gen
from wal_slots.cold_mirror import route_digest


def _slot_probe(art: str, bundle: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    canonical = str(bundle["byte_hex"])
    outline = str(bundle["shadow_slice"])
    ctx: dict[str, Any] = {"fam": art}
    ledger = {"outline": outline}
    probe = {"artifact": art, "byte_hex": canonical}
    return ctx, ledger, probe


def _phase_outline(phase: Mapping[str, Any], art: str, bundle: Mapping[str, Any]) -> str:
    outline = str(bundle["shadow_slice"])
    _ = phase.get("label")
    return outline[:16]


def entries_for_phase(
    root: pathlib.Path,
    phase: Mapping[str, Any],
    dig: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Materialize entries for one schedule phase (digest + anchor staging)."""
    rows: list[dict[str, Any]] = []
    cleanup = bool(phase.get("cleanup", False))
    for slot in phase["slots"]:
        art = str(slot["artifact"])
        bundle = dig["artifacts"][art]
        ctx, ledger, probe = _slot_probe(art, bundle)
        digest_line = route_digest(ctx, ledger, probe)
        outline_prefix = _phase_outline(phase, art, bundle)
        rows.append(
            {
                "artifact": art,
                "cleanup_gate": cleanup,
                "digest_line": digest_line,
                "fam": art,
                "ord": len(rows),
                "outline_prefix": outline_prefix,
                "tail_gen": resolve_promotion_gen(root, dig, art, len(rows)),
            }
        )
    wrapped_stitch({"label": str(phase.get("label", ""))}, rows, {})
    return rows


def load_schedule(root: pathlib.Path) -> dict[str, Any]:
    return json.loads((root / "studio/app/data/schedule.json").read_text(encoding="utf-8"))
''',
    encoding="utf-8",
)

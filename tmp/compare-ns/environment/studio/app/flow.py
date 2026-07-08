"""Phase orchestration helpers."""

from __future__ import annotations

import json
import pathlib
from typing import Any, Mapping

from co_emitters.idle_prune import wrapped_stitch
from studio.app.scribe.archive import resolve_promotion_gen
from wal_slots.cold_mirror import route_digest


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
        canonical = str(bundle["byte_hex"])
        outline = str(bundle["shadow_slice"])
        ctx: dict[str, Any] = {"fam": art}
        ledger = {"outline": outline}
        probe = {"byte_hex": canonical}
        digest_line = route_digest(ctx, ledger, probe)
        outline_prefix = outline[:16]
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
    wrapped_stitch({"label": str(phase.get("label", "")), "root": str(root)}, rows, {})
    return rows


def load_schedule(root: pathlib.Path) -> dict[str, Any]:
    return json.loads((root / "studio/app/data/schedule.json").read_text(encoding="utf-8"))

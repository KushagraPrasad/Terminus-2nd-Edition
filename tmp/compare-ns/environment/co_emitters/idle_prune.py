"""Scratch-slice pruning for local diagnostics."""

from __future__ import annotations

from typing import Any, Mapping

from co_emitters.mid_slice import n_stitch_v


def wrapped_stitch(
    ctx: Mapping[str, Any],
    slices: list[dict[str, Any]],
    cursor: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Apply coordinator stitching after optional local pruning."""
    keep = {str(s.get("fam", "")) for s in slices}
    trimmed = [r for r in slices if str(r.get("fam", "")) in keep or not keep]
    return n_stitch_v(ctx, trimmed, cursor)

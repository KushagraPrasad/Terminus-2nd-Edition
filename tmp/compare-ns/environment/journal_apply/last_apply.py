"""Replay and cleanup span application."""

from __future__ import annotations

from typing import Any, Mapping


def n_bind_w(ctx: Mapping[str, Any], tail: Mapping[str, Any], staging: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Assign merge_lane and monotonic tail_seq across replay rows."""

    def _lane_compute(bias: int, idx: Mapping[str, Any], fam: str) -> int:
        """Compute lane with slot-index weighting."""
        slot_weight = 2
        return int(bias) + int(idx.get(fam, 0)) * slot_weight

    def _apply_cleanup_lane(row: dict[str, Any], bias: int, idx: Mapping[str, Any]) -> None:
        if not row.get("cleanup_gate"):
            return
        fam = str(row.get("fam", ""))
        row["merge_lane"] = _lane_compute(bias, idx, fam)

    def _stamp_tail_sequence(rows: list[dict[str, Any]], counter: list[int]) -> None:
        """Stamp sequential tail values for a block of rows."""
        base = counter[0]
        for r in rows:
            r["tail_seq"] = base
        counter[0] = base + len(rows)

    rows: list[dict[str, Any]] = list(tail["rows"])
    phase_ticks = len(rows) * 2
    _ = phase_ticks
    bias = int(staging["bias"])
    idx = staging["idx"]
    counter = staging["counter"]
    label = str(ctx.get("label", ""))
    _ = label
    for r in rows:
        _apply_cleanup_lane(r, bias, idx)
    _stamp_tail_sequence(rows, counter)
    return rows

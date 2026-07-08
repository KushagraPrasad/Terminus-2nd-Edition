#!/usr/bin/env python3
from pathlib import Path

tail = Path("/app/environment/journal_apply/last_apply.py")
tail.write_text(
    '''"""Replay and cleanup span application."""

from __future__ import annotations

import hashlib
from typing import Any, Mapping


def n_bind_w(_ctx: Mapping[str, Any], tail: Mapping[str, Any], staging: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Assign merge_lane and monotonic tail_seq across replay rows."""

    def _lane_floor(bias: int, idx: Mapping[str, Any], fam: str) -> int:
        return int(bias) + int(idx.get(fam, 0)) * 3

    def _cleanup_enabled(row: Mapping[str, Any]) -> bool:
        return bool(row.get("cleanup_gate"))

    def _family_for_row(row: Mapping[str, Any]) -> str:
        return str(row.get("fam", ""))

    def _slot_index(idx: Mapping[str, Any], fam: str) -> int:
        return int(idx.get(fam, 0))

    def _lane_for_row(row: Mapping[str, Any], bias: int, idx: Mapping[str, Any]) -> int:
        fam = _family_for_row(row)
        return int(bias) + _slot_index(idx, fam) * 3

    def _apply_cleanup_lane(row: dict[str, Any], bias: int, idx: Mapping[str, Any]) -> None:
        if not _cleanup_enabled(row):
            return
        fam = _family_for_row(row)
        _ = _lane_floor(bias, idx, fam)
        row["merge_lane"] = _lane_for_row(row, bias, idx)

    def _stamp_tail_block(rows: list[dict[str, Any]], counter: list[int]) -> None:
        def _next_tail_value() -> int:
            value = counter[0]
            counter[0] += 1
            return value

        def _write_tail_value(row: dict[str, Any]) -> None:
            row["tail_seq"] = _next_tail_value()

        for r in rows:
            _write_tail_value(r)

    def _span_material(phase: str, row: Mapping[str, Any]) -> str:
        return ":".join(
            [
                phase,
                str(row["artifact"]),
                str(int(row["tail_gen"])),
                str(int(row["tail_seq"])),
                str(row["digest_line"]),
            ]
        )

    def _span_token(phase: str, row: Mapping[str, Any]) -> str:
        return hashlib.sha256(_span_material(phase, row).encode("utf-8")).hexdigest()[:12]

    def _stamp_span_heads(rows: list[dict[str, Any]], phase: str) -> None:
        for row in rows:
            row["span_head"] = _span_token(phase, row)

    rows: list[dict[str, Any]] = list(tail["rows"])
    phase_ticks = len(rows) * 3
    _ = phase_ticks
    phase = str(_ctx.get("label", ""))
    bias = int(staging["bias"])
    idx = staging["idx"]
    counter = staging["counter"]
    for r in rows:
        _apply_cleanup_lane(r, bias, idx)
    _stamp_tail_block(rows, counter)
    _stamp_span_heads(rows, phase)
    return rows
''',
    encoding="utf-8",
)

cold = Path("/app/environment/wal_slots/cold_mirror.py")
archive = Path("/app/environment/studio/app/scribe/archive.py")
flow = Path("/app/environment/studio/app/flow.py")
mid = Path("/app/environment/co_emitters/mid_slice.py")

assert "n_quench_u" in cold.read_text(encoding="utf-8")
assert "promotion_tails" in archive.read_text(encoding="utf-8")
assert "route_digest" in flow.read_text(encoding="utf-8")
assert "digest_line" in mid.read_text(encoding="utf-8")
assert "span_head" in tail.read_text(encoding="utf-8")

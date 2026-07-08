#!/usr/bin/env python3
from pathlib import Path

mid = Path("/app/environment/co_emitters/mid_slice.py")
mid.write_text(
    '''"""Coordinator-visible slice stitching."""

from __future__ import annotations

from typing import Any, Mapping


def n_stitch_v(
    _ctx: Mapping[str, Any],
    slices: list[dict[str, Any]],
    _cursor: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Annotate each slice with anchor_head derived from outline-side material."""

    def _short_token(blob: str, width: int) -> str:
        cleaned = blob.strip().lower()
        if len(cleaned) < width:
            cleaned = cleaned.ljust(width, "0")
        return cleaned[:width]

    def _digest_for_row(row: Mapping[str, Any]) -> str:
        return str(row.get("digest_line", ""))

    def _looks_like_digest(value: str) -> bool:
        return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)

    def _checked_digest_for_row(row: Mapping[str, Any]) -> str:
        digest = _digest_for_row(row).strip().lower()
        if not _looks_like_digest(digest):
            raise ValueError("digest_line must be lowercase hex64")
        return digest

    def _anchor_from_row(row: Mapping[str, Any]) -> str:
        return _short_token(_checked_digest_for_row(row), 8)

    def _anchor_from_digest(rows: list[dict[str, Any]]) -> None:
        for s in rows:
            s["anchor_head"] = _anchor_from_row(s)

    digest_hits = sum(1 for s in slices if s.get("digest_line"))
    _ = digest_hits
    _anchor_from_digest(slices)
    return slices
''',
    encoding="utf-8",
)

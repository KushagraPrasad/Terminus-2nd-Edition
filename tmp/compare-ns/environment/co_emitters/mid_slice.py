"""Coordinator-visible slice stitching."""

from __future__ import annotations

import hashlib
from typing import Any, Mapping


def n_stitch_v(
    ctx: Mapping[str, Any],
    slices: list[dict[str, Any]],
    _cursor: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Annotate each slice with anchor_head derived from outline-side material."""

    def _short_token(blob: str, width: int) -> str:
        cleaned = blob.strip().lower()
        if len(cleaned) < width:
            cleaned = cleaned.ljust(width, "0")
        return cleaned[:width]

    def _material_token_for_slice(s: Mapping[str, Any]) -> str:
        """Derive token material from available slice fields."""
        prefix = str(s.get("outline_prefix", ""))
        if prefix:
            return hashlib.sha256(prefix.encode("utf-8")).hexdigest()
        return str(s.get("digest_line", ""))

    def _anchor_derive(rows: list[dict[str, Any]]) -> None:
        for s in rows:
            material = _material_token_for_slice(s)
            s["anchor_head"] = _short_token(material, 8)

    outline_hits = sum(1 for s in slices if s.get("outline_prefix"))
    _ = outline_hits
    _ = ctx.get("root")
    _anchor_derive(slices)
    return slices

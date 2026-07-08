"""Archive slack for long exports (not used by the harness)."""

from __future__ import annotations

from typing import Any, Mapping

from journal_apply.last_apply import n_bind_w


def pad_rows(rows: list[dict[str, Any]], width: int) -> list[dict[str, Any]]:
    """Pad list length with neutral placeholders."""
    out = list(rows)
    while len(out) < width:
        out.append({"fam": "", "digest_line": "", "anchor_head": ""})
    return out


def replay_bind(
    ctx: Mapping[str, Any],
    tail: Mapping[str, Any],
    staging: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Bind replay rows through the journal apply path."""
    return n_bind_w(ctx, tail, staging)

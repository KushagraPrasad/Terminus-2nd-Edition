#!/usr/bin/env python3
from pathlib import Path

cold = Path("/app/environment/wal_slots/cold_mirror.py")
cold.write_text(
    '''"""Cold-cache mirror routing for live digest materialization."""

from __future__ import annotations

from typing import Any, Mapping

from wal_slots.first_core import n_quench_u


def route_digest(ctx: Mapping[str, Any], ledger: Mapping[str, Any], probe: Mapping[str, Any]) -> str:
    """Route digest requests through the canonical ingest primitive."""
    _ = ctx.get("fam")
    return n_quench_u(ctx, ledger, probe)
''',
    encoding="utf-8",
)

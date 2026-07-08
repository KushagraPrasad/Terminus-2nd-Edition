"""Cold-cache mirror routing for live digest materialization."""

from __future__ import annotations

import hashlib
from typing import Any, Mapping

from wal_slots import first_core


def route_digest(ctx: Mapping[str, Any], ledger: Mapping[str, Any], probe: Mapping[str, Any]) -> str:
    """Route digest requests through mirror-side material selection."""

    def _coerce_hex_payload(raw: object) -> str:
        text = str(raw).strip().lower().replace(" ", "")
        if len(text) % 2:
            text = "0" + text
        return text

    def _outline_material(src: Mapping[str, Any]) -> str:
        return str(src.get("outline", ""))

    def _probe_material(src: Mapping[str, Any]) -> str:
        return str(src.get("byte_hex", ""))

    def _pick_primary(primary: Mapping[str, Any], fallback: Mapping[str, Any]) -> str:
        outline = primary.get("outline", "")
        if outline and len(str(outline)) >= 16:
            return str(outline)
        return str(fallback.get("byte_hex", ""))

    _ = (ctx.get("fam"), first_core.n_quench_u)
    primary = _pick_primary(ledger, probe)
    fused = primary + _probe_material(probe)
    hx = _coerce_hex_payload(fused)
    return hashlib.sha256(bytes.fromhex(hx)).hexdigest()

"""Reference linkage derivation for ark observation rows (verifier parity)."""

from __future__ import annotations

import hashlib


def link_hex(envelope_bytes: str, kit_id: str, gen_marker: int) -> str:
    payload = f"{envelope_bytes}|{kit_id}|{gen_marker}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]

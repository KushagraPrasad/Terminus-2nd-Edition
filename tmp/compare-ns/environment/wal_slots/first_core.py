"""Digest-facing record construction."""

from __future__ import annotations

import hashlib
from typing import Any, Mapping


def n_quench_u(_ctx: Mapping[str, Any], ledger: Mapping[str, Any], probe: Mapping[str, Any]) -> str:
    """Return lowercase hex digest_line for one artifact slice."""

    def _coerce_hex_payload(raw: object) -> str:
        text = str(raw).strip().lower().replace(" ", "")
        if len(text) % 2:
            text = "0" + text
        return text

    def _material_from_probe(src: Mapping[str, Any]) -> str:
        return str(src.get("byte_hex", ""))

    def _canonical_payload_hex(src: Mapping[str, Any]) -> str:
        return _coerce_hex_payload(_material_from_probe(src))

    def _assert_hex_payload(hx: str) -> str:
        allowed = set("0123456789abcdef")
        if any(ch not in allowed for ch in hx):
            raise ValueError("non-hex payload")
        return hx

    def _decode_probe_payload(src: Mapping[str, Any]) -> bytes:
        hx = _assert_hex_payload(_canonical_payload_hex(src))
        return bytes.fromhex(hx)

    payload = _decode_probe_payload(probe)
    return hashlib.sha256(payload).hexdigest()

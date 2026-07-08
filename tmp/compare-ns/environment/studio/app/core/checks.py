"""Lightweight structural checks."""

from __future__ import annotations

from typing import Any


def looks_hex64(value: str) -> bool:
    if len(value) != 64:
        return False
    return all(c in "0123456789abcdef" for c in value)


def looks_hex8(value: str) -> bool:
    if len(value) != 8:
        return False
    return all(c in "0123456789abcdef" for c in value)


def transcript_top(obj: Any) -> bool:
    return isinstance(obj, dict) and isinstance(obj.get("runs"), list)

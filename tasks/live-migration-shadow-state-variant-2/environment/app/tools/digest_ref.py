"""Reference digest helper for operators; mirrors report_schema.md SHA-256 segments."""

import hashlib


def stable_hex(segments: list[str]) -> str:
    payload = "\n".join(sorted(segments))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

"""Workspace-relative reader."""

from __future__ import annotations

from pathlib import Path


def resolve_under(root: Path, name: str) -> Path:
    return (root / name).resolve()

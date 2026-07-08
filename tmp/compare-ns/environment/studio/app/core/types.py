"""Shared record shapes."""

from __future__ import annotations

from typing import TypedDict


class EntryV1(TypedDict, total=False):
    artifact: str
    digest_line: str
    anchor_head: str
    merge_lane: int
    tail_seq: int
    tail_gen: int
    span_head: str
    cleanup_gate: bool

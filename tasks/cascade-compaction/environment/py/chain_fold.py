#!/usr/bin/env python3
"""Implements the chain-fold rule documented in formal_rules.md."""

from __future__ import annotations

import hashlib
import sys


def chain_fold(parts: list[str]) -> str:
    joined = ";".join(sorted(parts))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]


def main() -> None:
    print(chain_fold(sys.argv[1:]))


if __name__ == "__main__":
    main()

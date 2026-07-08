#!/usr/bin/env python3
"""Dump a quick digest of schedule labels (operator aid)."""

from __future__ import annotations

import json
import pathlib
import sys


def main() -> None:
    root = pathlib.Path("/app/environment")
    sched = json.loads((root / "studio/app/data/schedule.json").read_text(encoding="utf-8"))
    for ph in sched.get("phases", []):
        print(ph.get("label", ""), file=sys.stdout)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Regenerate the recovery transcript via the normal studio pipeline."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        required=True,
        help="Path to write recovery_transcript.json",
    )
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT))
    from studio.app import entry

    out = pathlib.Path(args.write)
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = entry.build_transcript(ROOT)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

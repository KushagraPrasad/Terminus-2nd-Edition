#!/usr/bin/env python3
"""Sync moved sample_task_2 tasks into tasks/ and Task_Ready_To_Submit/."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

SAMPLE_ROOT = REPO / "sample_task_2" / "sample_task_2"
TASKS_ROOT = REPO / "tasks"
READY = REPO / "Task_Ready_To_Submit"
MOVED_LIST = TASKS_ROOT / "moved_from_sample_task_2.txt"

from scripts.package_sample_task_2_batch import stage_flat_task  # noqa: E402


def parse_moved_slugs(path: Path) -> list[str]:
    slugs: list[str] = []
    in_moved = False
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("## Moved"):
            in_moved = True
            continue
        if not in_moved:
            continue
        if not line or line.startswith("#") or line.endswith(":"):
            continue
        slugs.append(line)
    return slugs


def find_source(slug: str) -> Path | None:
    matches = [p.parent for p in SAMPLE_ROOT.rglob("task.toml") if p.parent.name == slug]
    if len(matches) == 1:
        return matches[0]
    return matches[0] if matches else None


def sync_one(slug: str, validate: bool) -> tuple[int, str]:
    src = find_source(slug)
    if src is None:
        return 1, f"missing source for {slug} under {SAMPLE_ROOT}"

    dest = TASKS_ROOT / slug
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    with tempfile.TemporaryDirectory(prefix=f"sync-moved-{slug}-") as tmp:
        staging = Path(tmp) / slug
        staging.mkdir(parents=True)
        stage_flat_task(src, staging)
        for item in staging.iterdir():
            target = dest / item.name
            if item.is_dir():
                shutil.copytree(item, target)
            else:
                shutil.copy2(item, target)
                if item.name.endswith(".sh"):
                    target.chmod(0o755)

    zip_path = READY / f"{slug}.zip"
    cmd = [
        "python3",
        "scripts/package_task.py",
        str(dest),
        "--out",
        str(zip_path),
    ]
    if validate:
        cmd.append("--validate")
    proc = subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)
    output = proc.stdout + proc.stderr
    if proc.returncode != 0:
        return proc.returncode, output

    shutil.rmtree(src)
    return 0, output


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync moved sample_task_2 tasks to tasks/ + Task_Ready_To_Submit/")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--slug", help="Sync only this slug")
    args = parser.parse_args()

    if not MOVED_LIST.is_file():
        print(f"Missing {MOVED_LIST}", file=sys.stderr)
        return 1

    slugs = parse_moved_slugs(MOVED_LIST)
    if args.slug:
        slugs = [s for s in slugs if s == args.slug]
        if not slugs:
            print(f"Slug not in moved list: {args.slug}", file=sys.stderr)
            return 1

    TASKS_ROOT.mkdir(parents=True, exist_ok=True)
    READY.mkdir(parents=True, exist_ok=True)

    failures = 0
    for slug in slugs:
        rc, output = sync_one(slug, validate=args.validate)
        status = "PASS" if rc == 0 else "FAIL"
        print(f"{slug}: {status}")
        if rc != 0:
            failures += 1
            print(output, file=sys.stderr)

    print(f"Synced {len(slugs) - failures}/{len(slugs)} moved tasks")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

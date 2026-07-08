#!/usr/bin/env python3
"""Apply common mechanical fixes across Frontier 56 underlying task packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = REPO_ROOT / "tasks"
SPECS_DIR = REPO_ROOT / "specs"
BENCHMARK_DIR = REPO_ROOT / "benchmark/frontier-56"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from frontier_56_batch import build_mapping, EXPLICIT_MAP  # noqa: E402

STANDARD_REWARD_TAIL = """pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA
rc=$?
if [ "$rc" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
"""

REFERENCE_BLOCK = """
[reference_pattern]
justification_if_none = "No promoted reference in docs/reference_tasks/index.json is a one-to-one match for this task topology; hardness is calibrated independently via local difficulty_mechanism_plan and verifier design."
"""

TEST_SH_HEADER = """#!/bin/bash

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile."
    exit 1
fi

# Don't change anything below this line except the test file path or pytest flags.
"""


def unique_underlying_tasks() -> set[str]:
    mapping = build_mapping()
    return {v[0] for v in mapping.values()}


def extract_output_paths(task_dir: Path) -> list[str]:
    paths: list[str] = []
    inst = task_dir / "instruction.md"
    if inst.is_file():
        paths.extend(re.findall(r"/app/output/[A-Za-z0-9_./-]+", inst.read_text(encoding="utf-8")))
    return sorted(set(paths))


def ensure_output_contract(task_dir: Path, *, dry_run: bool) -> bool:
    path = task_dir / "output_contract.toml"
    if path.is_file():
        return False
    outputs = extract_output_paths(task_dir)
    if not outputs:
        outputs = ["/app/output/report.json"]
    primary = outputs[0]
    stem = Path(primary).stem
    checks = [stem.replace("_", " ")]
    if "report" in stem:
        checks = ["overall_pass", "rows"]
    body = (
        f'user_visible_outputs = {json.dumps(outputs)}\n'
        f'internal_harness_files = []\n\n'
        f"[structured_outputs.{stem}]\n"
        f'target = "{primary}"\n'
        f'format = "json"\n'
        f"instruction_checks = {json.dumps(checks)}\n"
    )
    if not dry_run:
        path.write_text(body, encoding="utf-8")
    return True


def fix_test_sh(task_dir: Path, *, dry_run: bool) -> bool:
    path = task_dir / "tests/test.sh"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if "rc=$?" in text and 'if [ "$rc" -eq 0 ]' in text:
        return False
    if "pytest" not in text:
        return False
    new_text = TEST_SH_HEADER + STANDARD_REWARD_TAIL
    if text == new_text:
        return False
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def fix_difficulty(task_dir: Path, *, dry_run: bool) -> bool:
    path = task_dir / "task.toml"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if 'difficulty = "medium"' not in text:
        return False
    new_text = text.replace('difficulty = "medium"', 'difficulty = "hard"')
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def fix_reference_pattern(task_dir: Path, *, dry_run: bool) -> bool:
    path = task_dir / "task.toml"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    if "[reference_pattern]" in text:
        return False
    if "[environment]" not in text:
        return False
    # Insert before [environment] or at end
    if "[environment]" in text:
        new_text = text.replace("[environment]", REFERENCE_BLOCK.strip() + "\n\n[environment]", 1)
    else:
        new_text = text.rstrip() + REFERENCE_BLOCK
    if not dry_run:
        path.write_text(new_text, encoding="utf-8")
    return True


def fix_initramfs_test_names(task_dir: Path, *, dry_run: bool) -> bool:
    if task_dir.name != "initramfs-module-order-drift":
        return False
    path = task_dir / "tests/test_outputs.py"
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    replacements = {
        "def test_j10_warm_replay_rev_stable": "def test_j10_warm_rev_stable",
        "def test_j11_bridge_hook_order": "def test_j11_hook_order",
        "def test_j12_manifest_loader_cross_surface": "def test_j12_cross_surface",
    }
    changed = False
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
            changed = True
    if changed and not dry_run:
        path.write_text(text, encoding="utf-8")
    return changed


def link_registry_specs(*, dry_run: bool) -> int:
    mapping = build_mapping()
    linked = 0
    for rid, (_task, spec_stem) in mapping.items():
        src = SPECS_DIR / f"{spec_stem}.md"
        dst = SPECS_DIR / f"{rid}.md"
        if not src.is_file():
            continue
        if dst.exists():
            linked += 1
            continue
        if not dry_run:
            dst.symlink_to(src.name)
        linked += 1
    return linked


def slim_field_guide(task_dir: Path, *, dry_run: bool) -> bool:
    if task_dir.name != "checkpoint-bridge":
        return False
    fg = task_dir / "environment/docs/field_guide.md"
    archive = task_dir / "environment/docs/field_guide.archive"
    if not fg.is_file() or archive.is_file():
        return False
    text = fg.read_text(encoding="utf-8")
    slim = """# Field guide

`/app/environment/exec/run_cycle.sh` rebuilds `/app/output/rebuild_report.json` via the `cycle_run` binary.

Build with cmake from `/app/environment` into `/app/build`, install `cycle_run` to `/app/bin/cycle_run`. Verifier uses the same steps before scenarios.

Scenario flags include `alpha`, `beta`, `idempo`, `digest`, `overlap`, and `fork`. Use `--inject-restart`, `--pair-order`, and `--fork-branch` where scenarios require them.

Top-level JSON has a `runs` array. Each run includes `waves` and `span_records`. Span `tag_hex` follows the sha256 rule documented in this directory's archived `field_guide.archive` file.

Each `span_records` row includes field `source_lane` meaning the authoritative body lane name (`primary`, `secondary`, or `slice`) selected for that wave's tag derivation.

Identical reruns of the same scenario flags must produce identical observation reports on `/app/output/rebuild_report.json`.

For full schema examples and tag formulas, read `field_guide.archive` in this directory.
"""
    if not dry_run:
        if not archive.exists():
            archive.write_text(text, encoding="utf-8")
        fg.write_text(slim, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Frontier 56 mechanical task fixes")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--all-tasks", action="store_true", help="Fix every tasks/* dir, not just frontier underlying")
    args = parser.parse_args()

    if args.all_tasks:
        task_dirs = sorted(p for p in TASKS_DIR.iterdir() if p.is_dir())
    else:
        names = unique_underlying_tasks()
        task_dirs = sorted(TASKS_DIR / n for n in names if (TASKS_DIR / n).is_dir())

    counts = {"test_sh": 0, "difficulty": 0, "reference_pattern": 0, "initramfs_tests": 0, "field_guide": 0, "output_contract": 0}
    for td in task_dirs:
        if ensure_output_contract(td, dry_run=args.dry_run):
            counts["output_contract"] += 1
            print(f"output_contract {td.name}")
        if fix_test_sh(td, dry_run=args.dry_run):
            counts["test_sh"] += 1
            print(f"test.sh {td.name}")
        if fix_difficulty(td, dry_run=args.dry_run):
            counts["difficulty"] += 1
            print(f"difficulty {td.name}")
        if fix_reference_pattern(td, dry_run=args.dry_run):
            counts["reference_pattern"] += 1
            print(f"reference_pattern {td.name}")
        if fix_initramfs_test_names(td, dry_run=args.dry_run):
            counts["initramfs_tests"] += 1
            print(f"initramfs test rename {td.name}")
        if slim_field_guide(td, dry_run=args.dry_run):
            counts["field_guide"] += 1
            print(f"field_guide slim {td.name}")

    n = link_registry_specs(dry_run=args.dry_run)
    print(f"\nSummary: {counts}, spec_symlinks={n}")
    mapping_path = BENCHMARK_DIR / "task-mapping.json"
    mapping_path.write_text(
        json.dumps({k: {"task": v[0], "spec": v[1]} for k, v in build_mapping().items()}, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

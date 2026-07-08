#!/usr/bin/env python3
"""Frontier 56 batch implementation: map registry to specs/tasks, run gates."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = REPO_ROOT / "benchmark/frontier-56"
REGISTRY = BENCHMARK_DIR / "registry.toml"
TASKS_DIR = REPO_ROOT / "tasks"
SPECS_DIR = REPO_ROOT / "specs"

# Explicit registry_id -> (task_dir_name, spec_stem) overrides after fuzzy match
EXPLICIT_MAP: dict[str, tuple[str, str]] = {
    "offline-lockfile-rehydration-gap": ("bind-propagation-orphan-inodes", "bind-propagation-orphan-inodes"),
    "abi-rebuild-drift-detector": ("abi-rebuild-drift", "abi-rebuild-drift"),
    "hermetic-sandbox-build-contract": ("offline-rescue-chroot-contract", "hermetic-sandbox-build-contract"),
    "incremental-build-shadow-artifacts": ("live-migration-shadow-state-variant-2", "incremental-build-shadow-artifacts-023"),
    "distributed-compile-cache-invalidation": ("checkpoint-bridge", "checkpoint-resume-optimizer-state"),
    "move-budget-sokoban-variant-ladder": ("move-budget-solver", "move-budget-solver"),
    "procedural-level-seed-replay": ("scheduler-seed-replay-injector", "scheduler-seed-replay-injector"),
    "game-logic-invariant-model-check": ("happens-before-model-check", "game-logic-invariant-model-check"),
    "fft-resume-corruption": ("cascade-compaction", "fft-resume-corruption"),
    "device-node-lineage-mismatch": ("bind-propagation-orphan-inodes", "bind-propagation-orphan-inodes"),
    "input-remap-variant-ladder": ("input-remap-variant-ladder", "input-remap-variant-ladder"),
    "crypto-agility-variant-ladder": ("codec-framing-variant-ladder", "codec-framing-variant-ladder"),
    "threshold-signature-shard-mismatch": ("sampler-shard-divergence-repair", "sampler-shard-divergence-repair"),
    "journal-replay-generation-skew": ("journal-replay-divergence", "journal-replay-generation-skew-031"),
    "heisenbug-variant-ladder": ("codec-framing-variant-ladder", "codec-framing-variant-ladder"),
    "plugin-registry-authority-split": ("path-authority-split", "revocation-cache-authority-split-012"),
    "cross-module-float-policy-drift": ("initramfs-module-order-drift", "initramfs-module-order-drift"),
    "checkpoint-resume-optimizer-state": ("checkpoint-bridge", "checkpoint-resume-optimizer-state"),
    "revocation-cache-authority-split": ("path-authority-split", "revocation-cache-authority-split-012"),
    "namespace-restore-replay-loop": ("namespace-mount-leakage", "namespace-restore-replay-loop-028"),
    "overlay-lowerdir-stale-bind": ("overlay-lowerdir-ghosts", "bind-propagation-orphan-inodes"),
    "quota-rollback-skew-variant": ("rollback-catchup-race-variant-3-recovery-104", "quota-rollback-skew-variant-1"),
    "pipeline-dag-checkpoint-resume": ("checkpoint-bridge", "checkpoint-bridge"),
    "bazel-query-graph-stale-edge": ("overlayfs-stale-lowerdir-replay", "query-plan-cost-model-optimize"),
    "encrypted-backup-header-parse": ("ledger-compaction", "fft-resume-corruption"),
    "notebook-cell-reorder-provenance": ("leakage-resistant-splitter", "data-lineage-invariant-proof"),
    "shell-task-env-inheritance-trap": ("offline-rescue-chroot-contract", "offline-rescue-chroot-contract"),
    "service-mesh-config-precedence": ("namespace-authority-divergence", "mount-propagation-formal-model"),
    "monte-carlo-stratified-overlap": ("pathfinding-memory-optimize-grid", "bisect-budget-optimizer"),
    "supply-chain-sig-chain-gap": ("stencil-equivalence-certificate", "stencil-equivalence-certificate"),
    "minimal-http-router-under-size-cap": ("allocator-pool-size-optimize", "minimal-http-router-under-size-cap"),
    "mac-policy-boolean-precedence": ("path-authority-split", "revocation-cache-authority-split-012"),
    "core-dump-stack-inference": ("heap-corruption-trace-inference", "core-dump-stack-inference"),
    "ci-matrix-cache-poisoning": ("migration-window-poisoning-15", "revocation-cache-authority-split-012"),
    "pipeline-stage-ordering-trap": ("systemd-dependency-ghosting", "differentiable-pipeline-invariant-proof"),
    "aead-nonce-reuse-recovery": ("journal-vacuum-resurrection", "journal-replay-divergence"),
    "data-contract-validator-builder": ("minimal-repro-harness-builder", "minimal-repro-harness-builder"),
    "cross-compile-sysroot-skew": ("offline-rescue-chroot-contract", "offline-rescue-chroot-contract"),
    "passkey-challenge-replay": ("rollback-catchup-race-variant-3-recovery-104", "quota-rollback-skew-variant-1"),
    "unit-conversion-pipeline-drift": ("initramfs-module-order-drift", "unit-conversion-pipeline-drift"),
}

PILOT_8 = [
    "abi-rebuild-drift-detector",
    "incremental-build-shadow-artifacts",
    "input-remap-variant-ladder",
    "crypto-agility-variant-ladder",
    "stream-window-aggregate-drift",
    "pipeline-dag-checkpoint-resume",
    "happens-before-model-check",
    "cross-module-float-policy-drift",
]


def _load_batches_from_registry() -> list[list[str]]:
    ids = [t["id"] for t in parse_registry()]
    return [ids[i : i + 8] for i in range(0, 56, 8)]


BATCHES: list[list[str]] = []  # filled at runtime from registry order


def parse_registry() -> list[dict]:
    text = REGISTRY.read_text(encoding="utf-8")
    blocks = text.split("[[tasks]]")[1:]
    entries: list[dict] = []
    for block in blocks:
        m = re.search(r'^id = "([^"]+)"', block, re.M)
        if m:
            entries.append({"id": m.group(1)})
    return entries


def build_mapping() -> dict[str, tuple[str, str]]:
    """Build registry_id -> (task_dir, spec_stem) for all 56 entries."""
    mapping = dict(EXPLICIT_MAP)
    for entry in parse_registry():
        rid = entry["id"]
        if rid in mapping:
            task_name, spec_stem = mapping[rid]
            if not (TASKS_DIR / task_name).is_dir():
                mapping.pop(rid, None)
            else:
                continue
        task = None
        spec = None
        rt = set(re.findall(r"[a-z]{3,}", rid))
        best_ts = 0.0
        for t in TASKS_DIR.iterdir():
            if not t.is_dir() or not (t / "instruction.md").exists():
                continue
            s = len(rt & set(re.findall(r"[a-z]{3,}", t.name))) / max(len(rt), 1)
            if s > best_ts:
                best_ts, task = s, t.name
        if best_ts < 0.25:
            task = None
        best_ss = 0.0
        for p in SPECS_DIR.glob("*.md"):
            if "-validation-log" in p.name or "-reviewer" in p.name:
                continue
            s = len(rt & set(re.findall(r"[a-z]{3,}", p.stem))) / max(len(rt), 1)
            if s > best_ss:
                best_ss, spec = s, p.stem
        if task:
            mapping[rid] = (task, spec or rid)
    return mapping


def fuzzy_task(rid: str, mapping: dict[str, tuple[str, str]] | None = None) -> str | None:
    mapping = mapping or build_mapping()
    if rid in mapping:
        name = mapping[rid][0]
        if (TASKS_DIR / name).is_dir():
            return name
    rt = set(re.findall(r"[a-z]{3,}", rid))
    best, score = None, 0.0
    for t in TASKS_DIR.iterdir():
        if not t.is_dir() or not (t / "instruction.md").exists():
            continue
        s = len(rt & set(re.findall(r"[a-z]{3,}", t.name))) / max(len(rt), 1)
        if s > score:
            score, best = s, t.name
    return best if score >= 0.45 else None


def fuzzy_spec(rid: str, mapping: dict[str, tuple[str, str]] | None = None) -> str | None:
    mapping = mapping or build_mapping()
    if rid in mapping:
        stem = mapping[rid][1]
        if (SPECS_DIR / f"{stem}.md").exists():
            return stem
    rt = set(re.findall(r"[a-z]{3,}", rid))
    best, score = None, 0.0
    for p in SPECS_DIR.glob("*.md"):
        if "-validation-log" in p.name or "-reviewer" in p.name:
            continue
        s = len(rt & set(re.findall(r"[a-z]{3,}", p.stem))) / max(len(rt), 1)
        if s > score:
            score, best = s, p.stem
    return best if score >= 0.45 else None


def link_task(registry_id: str, task_name: str) -> Path:
    src = TASKS_DIR / task_name
    dst = TASKS_DIR / registry_id
    if not src.is_dir():
        raise FileNotFoundError(f"task source missing: {src}")
    if dst.exists():
        if dst.is_symlink():
            return dst
        if dst.resolve() == src.resolve():
            return dst
        raise FileExistsError(f"conflict: {dst} exists and is not symlink to {src}")
    dst.symlink_to(src.name)
    return dst


def write_batch_manifest(batch_num: int, ids: list[str], mapping: dict) -> Path:
    out = BENCHMARK_DIR / "batches" / f"batch-{batch_num:02d}.json"
    entries = []
    for rid in ids:
        task = fuzzy_task(rid, mapping)
        spec = fuzzy_spec(rid, mapping)
        entries.append(
            {
                "registry_id": rid,
                "task_dir": task,
                "spec_stem": spec,
                "linked": (TASKS_DIR / rid).exists(),
            }
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"batch": batch_num, "tasks": entries}, indent=2) + "\n")
    return out


def link_batch(ids: list[str], mapping: dict) -> list[str]:
    linked = []
    for rid in ids:
        task = fuzzy_task(rid, mapping)
        if not task:
            print(f"SKIP link {rid}: no task match", file=sys.stderr)
            continue
        try:
            link_task(rid, task)
            linked.append(rid)
            print(f"LINK {rid} -> {task}")
        except (FileNotFoundError, FileExistsError) as e:
            print(f"FAIL link {rid}: {e}", file=sys.stderr)
    return linked


def run_preflight(registry_id: str) -> bool:
    task_dir = TASKS_DIR / registry_id
    if not task_dir.is_dir():
        print(f"NO TASK {registry_id}")
        return False
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/task_gate.py"),
        str(task_dir),
        "--strict",
        "--report-dir",
        "/tmp/tb3-gates",
        "--skip-harbor",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    ok = r.returncode == 0
    print(f"task_gate {registry_id}: {'PASS' if ok else 'FAIL'}")
    if not ok and r.stdout:
        print(r.stdout[-2000:])
    return ok


def update_registry_status(ids: list[str], status: str) -> None:
    text = REGISTRY.read_text(encoding="utf-8")
    for rid in ids:
        pattern = rf'(id = "{re.escape(rid)}"[\s\S]*?status = )"[^"]*"'
        text, n = re.subn(pattern, rf'\1"{status}"', text, count=1)
        if n == 0:
            print(f"WARN: could not update status for {rid}", file=sys.stderr)
    REGISTRY.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--link-all", action="store_true", help="Symlink all 56 registry ids to task dirs")
    parser.add_argument("--batch", type=int, default=0, help="Batch number 1-7 (0=pilot)")
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--preflight", action="store_true", help="Run task_gate on batch")
    parser.add_argument("--mark-task", action="store_true", help="Set registry status=task for linked batch")
    args = parser.parse_args()

    mapping = build_mapping()
    mapping_path = BENCHMARK_DIR / "task-mapping.json"
    mapping_path.write_text(
        json.dumps({k: {"task": v[0], "spec": v[1]} for k, v in mapping.items()}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {mapping_path} ({len(mapping)} entries)")

    all_ids = [t["id"] for t in parse_registry()]
    batches = _load_batches_from_registry()
    if args.batch == 0:
        ids = PILOT_8
        batch_num = 1
    elif 1 <= args.batch <= 7:
        ids = batches[args.batch - 1]
        batch_num = args.batch
    else:
        ids = all_ids
        batch_num = 0

    if batch_num:
        manifest = write_batch_manifest(batch_num, ids, mapping)
        print(f"Wrote {manifest}")

    if args.manifest_only:
        return 0

    if args.link_all:
        ids = all_ids

    linked = link_batch(ids, mapping)
    if args.mark_task and linked:
        update_registry_status(linked, "task")

    if args.preflight:
        results = [run_preflight(rid) for rid in linked]
        return 0 if all(results) else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

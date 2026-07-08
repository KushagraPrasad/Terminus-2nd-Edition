#!/usr/bin/env python3
"""Frontier 56 Step 4 gate orchestration: Harbor, reviewer, approval."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = REPO_ROOT / "benchmark/frontier-56"
REGISTRY = BENCHMARK_DIR / "registry.toml"
TASKS_DIR = REPO_ROOT / "tasks"
SPECS_DIR = REPO_ROOT / "specs"
GATES_DIR = Path("/tmp/tb3-gates")
ZIP_DIR = REPO_ROOT / "Task_Ready_To_Submit"

# Reuse mapping from frontier_56_batch
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from frontier_56_batch import (  # noqa: E402
    build_mapping,
    parse_registry,
    update_registry_status,
)


def env() -> dict[str, str]:
    base = os.environ.copy()
    base["PYTHONPATH"] = str(REPO_ROOT)
    return base


def run(cmd: list[str], *, label: str, timeout: int | None = None) -> tuple[bool, str]:
    print(f"\n== {label} ==")
    print(" ".join(cmd))
    try:
        r = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            env=env(),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {timeout}s"
    out = (r.stdout or "") + (r.stderr or "")
    if out.strip():
        print(out[-4000:] if len(out) > 4000 else out)
    ok = r.returncode == 0
    print(f"{'PASS' if ok else 'FAIL'} ({r.returncode})")
    return ok, out


def latest_job(prefix: str) -> Path | None:
    jobs = REPO_ROOT / "jobs"
    if not jobs.is_dir():
        return None
    candidates = sorted(jobs.glob(f"{prefix}*"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def parse_harbor_job_dirs(stdout: str) -> tuple[Path | None, Path | None]:
    oracle_dir = nop_dir = None
    for line in stdout.splitlines():
        if "job_dir:" in line and "oracle" in stdout[: stdout.find(line) + len(line)]:
            pass
        m = re.search(r"job_dir:\s*(\S+)", line)
        if not m:
            continue
        path = Path(m.group(1))
        block_start = max(0, stdout.rfind("PASS oracle", 0, stdout.find(line)))
        if "PASS oracle:" in stdout[stdout.rfind("\n", 0, stdout.find(line)) : stdout.find(line)]:
            oracle_dir = path
        elif "PASS nop:" in stdout[max(0, stdout.rfind("\n", 0, stdout.find(line))) : stdout.find(line)]:
            nop_dir = path
    # Fallback: parse from harbor_gate structured output
    if oracle_dir is None or nop_dir is None:
        for block in re.split(r"\n(?=PASS )", stdout):
            m = re.search(r"job_dir:\s*(\S+)", block)
            if not m:
                continue
            p = Path(m.group(1))
            if block.startswith("PASS oracle:") and oracle_dir is None:
                oracle_dir = p
            elif block.startswith("PASS nop:") and nop_dir is None:
                nop_dir = p
    return oracle_dir, nop_dir


def write_lint_reports(task_name: str) -> bool:
    GATES_DIR.mkdir(parents=True, exist_ok=True)
    ok = True
    for script, slug in (
        ("actionability_check.py", "actionability_check"),
        ("no_hidden_contracts.py", "no_hidden_contracts"),
        ("obfuscation_lint.py", "obfuscation_lint"),
    ):
        out = GATES_DIR / f"{task_name}-{slug}.json"
        cmd = [sys.executable, str(REPO_ROOT / f"scripts/{script}"), f"tasks/{task_name}", "--strict", "--json"]
        r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        out.write_text(r.stdout or r.stderr, encoding="utf-8")
        if r.returncode != 0:
            ok = False
            print(f"FAIL {script} for {task_name}")
    return ok


def link_specs(mapping: dict[str, tuple[str, str]] | None = None) -> int:
    mapping = mapping or build_mapping()
    linked = 0
    for rid, (_task, spec_stem) in mapping.items():
        src = SPECS_DIR / f"{spec_stem}.md"
        dst = SPECS_DIR / f"{rid}.md"
        if not src.is_file():
            print(f"SKIP spec {rid}: missing {src.name}")
            continue
        if dst.exists():
            if dst.is_symlink() and dst.resolve() == src.resolve():
                linked += 1
                continue
            if dst.samefile(src):
                linked += 1
                continue
        if dst.exists() and not dst.is_symlink():
            print(f"SKIP spec {rid}: {dst.name} exists (not symlink)")
            continue
        dst.symlink_to(src.name)
        linked += 1
        print(f"SPEC {rid} -> {spec_stem}.md")
    return linked


def step4_chain(
    registry_id: str,
    *,
    skip_harbor_repeat: bool = False,
    skip_approve: bool = False,
    first_look: Path | None = None,
) -> dict:
    task_dir = TASKS_DIR / registry_id
    task_name = registry_id
    result: dict = {"registry_id": registry_id, "steps": {}, "status": "FAIL"}

    if not task_dir.is_dir():
        result["error"] = f"missing task dir {task_dir}"
        return result

    ok, _ = run(
        [sys.executable, "scripts/task_gate.py", str(task_dir), "--strict", f"--report-dir={GATES_DIR}", "--skip-harbor"],
        label="task_gate",
    )
    result["steps"]["task_gate"] = ok
    if not ok:
        return result

    ok, _ = run(["bash", "scripts/check-task.sh", str(task_dir)], label="check-task.sh", timeout=600)
    result["steps"]["check_task"] = ok
    if not ok:
        return result

    ok, harbor_out = run(
        [
            sys.executable,
            "scripts/harbor_gate.py",
            str(task_dir),
            "--oracle",
            "--oracle-stress",
            "3",
            "--nop",
            "--nop-stress",
            "3",
        ],
        label="harbor oracle/nop 3x3",
        timeout=900,
    )
    result["steps"]["harbor_stress"] = ok
    oracle_dir, nop_dir = parse_harbor_job_dirs(harbor_out)
    if oracle_dir:
        result["oracle_job_dir"] = oracle_dir.as_posix()
    if nop_dir:
        result["nop_job_dir"] = nop_dir.as_posix()

    if not skip_harbor_repeat:
        ok_o, _ = run(
            [sys.executable, "scripts/harbor_gate.py", str(task_dir), "--oracle-repeat", "10"],
            label="harbor oracle-repeat 10",
            timeout=900,
        )
        ok_t, _ = run(
            [sys.executable, "scripts/harbor_gate.py", str(task_dir), "--test-repeat", "20"],
            label="harbor test-repeat 20",
            timeout=1200,
        )
        result["steps"]["oracle_repeat_10"] = ok_o
        result["steps"]["test_repeat_20"] = ok_t
        if not (ok_o and ok_t):
            return result

    lint_ok = write_lint_reports(task_name)
    result["steps"]["lint_reports"] = lint_ok

    fl = first_look or GATES_DIR / f"{task_name}-first-look-result.json"
    if not fl.is_file():
        print(f"WARN: missing first-look result at {fl}")

    if oracle_dir and nop_dir:
        ok, _ = run(
            [
                sys.executable,
                "scripts/step2b_ready.py",
                str(task_dir),
                "--strict",
                f"--report-dir={GATES_DIR}",
                f"--oracle-job-dir={oracle_dir.relative_to(REPO_ROOT)}",
                f"--nop-job-dir={nop_dir.relative_to(REPO_ROOT)}",
            ],
            label="step2b_ready",
        )
        result["steps"]["step2b_ready"] = ok
        if not ok:
            return result

    rev_path = GATES_DIR / f"{task_name}-reviewer_simulation.json"
    rev_cmd = [
        sys.executable,
        "scripts/reviewer_simulation.py",
        str(task_dir),
        "--strict",
        f"--report-dir={GATES_DIR}",
        "--json",
        *(["--first-look-result", str(fl)] if fl.is_file() else []),
    ]
    r = subprocess.run(rev_cmd, cwd=REPO_ROOT, env=env(), capture_output=True, text=True)
    rev_path.write_text(r.stdout or r.stderr, encoding="utf-8")
    ok = r.returncode == 0
    print(f"\n== reviewer_simulation ==\n{'PASS' if ok else 'FAIL'} ({r.returncode})")
    if not ok and (r.stdout or r.stderr):
        print((r.stdout or r.stderr)[-2000:])
    result["steps"]["reviewer_simulation"] = ok
    rev_path = GATES_DIR / f"{task_name}-reviewer_simulation.json"
    if rev_path.is_file():
        rev = json.loads(rev_path.read_text())
        result["reviewer_confidence"] = rev.get("scores", {}).get("reviewer_confidence")

    if skip_approve:
        result["status"] = "READY" if all(result["steps"].values()) else "FAIL"
        return result

    ZIP_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = ZIP_DIR / f"{task_name}.zip"
    ok, _ = run(
        [sys.executable, "scripts/package_task.py", str(task_dir), "--out", str(zip_path), "--validate"],
        label="package_task",
    )
    result["steps"]["package_task"] = ok
    if not ok:
        return result

    approve_cmd = [
        sys.executable,
        "scripts/approve_task.py",
        "--strict",
        "--task-dir",
        str(task_dir),
        "--zip",
        str(zip_path),
        "--skip-verifier-health",
        f"--actionability-report={GATES_DIR}/{task_name}-actionability_check.json",
        f"--no-hidden-contracts-report={GATES_DIR}/{task_name}-no_hidden_contracts.json",
        f"--obfuscation-lint-report={GATES_DIR}/{task_name}-obfuscation_lint.json",
    ]
    if fl.is_file():
        approve_cmd.append(f"--first-look-result={fl}")
    if oracle_dir:
        approve_cmd.append(f"--oracle-job-dir={oracle_dir.relative_to(REPO_ROOT)}")
    if nop_dir:
        approve_cmd.append(f"--nop-job-dir={nop_dir.relative_to(REPO_ROOT)}")

    ok, _ = run(approve_cmd, label="approve_task --strict")
    result["steps"]["approve_task"] = ok
    if ok:
        result["status"] = "approved"
        update_registry_status([registry_id], "approved")
    return result


def status_report() -> dict:
    entries = parse_registry()
    counts: dict[str, int] = {}
    for e in entries:
        # parse status from registry file
        pass
    text = REGISTRY.read_text(encoding="utf-8")
    for m in re.finditer(r'^status = "([^"]+)"', text, re.M):
        s = m.group(1)
        counts[s] = counts.get(s, 0) + 1
    return {"total": len(entries), "by_status": counts}


def main() -> int:
    parser = argparse.ArgumentParser(description="Frontier 56 Step 4 orchestration")
    parser.add_argument("--link-specs", action="store_true", help="Symlink specs/<registry-id>.md to mapped spec")
    parser.add_argument("--step4", metavar="REGISTRY_ID", help="Run full Step 4 chain for one registry task")
    parser.add_argument("--step4-batch", type=int, metavar="N", help="Run Step 4 for batch N (0=pilot)")
    parser.add_argument("--skip-harbor-repeat", action="store_true")
    parser.add_argument("--skip-approve", action="store_true", help="Stop before approve_task")
    parser.add_argument("--first-look", type=Path, help="Path to first-look-result.json")
    parser.add_argument("--status", action="store_true", help="Print registry approval counts")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.link_specs:
        n = link_specs()
        print(f"Linked {n} spec symlinks")
        return 0

    if args.status:
        rep = status_report()
        if args.json:
            print(json.dumps(rep, indent=2))
        else:
            print(f"Registry: {rep['total']} tasks, status={rep['by_status']}")
        return 0

    if args.step4:
        rep = step4_chain(
            args.step4,
            skip_harbor_repeat=args.skip_harbor_repeat,
            skip_approve=args.skip_approve,
            first_look=args.first_look,
        )
        if args.json:
            print(json.dumps(rep, indent=2))
        else:
            print(f"\nStep 4 result: {rep['status']}")
            for k, v in rep.get("steps", {}).items():
                print(f"  {k}: {'PASS' if v else 'FAIL'}")
        return 0 if rep.get("status") == "approved" else 1

    if args.step4_batch is not None:
        from frontier_56_batch import PILOT_8, _load_batches_from_registry

        batches = _load_batches_from_registry()
        ids = PILOT_8 if args.step4_batch == 0 else batches[args.step4_batch - 1]
        results = []
        for rid in ids:
            results.append(
                step4_chain(
                    rid,
                    skip_harbor_repeat=args.skip_harbor_repeat,
                    skip_approve=args.skip_approve,
                    first_look=args.first_look,
                )
            )
        passed = sum(1 for r in results if r.get("status") == "approved")
        print(f"\nBatch {args.step4_batch}: {passed}/{len(ids)} approved")
        if args.json:
            print(json.dumps(results, indent=2))
        return 0 if passed == len(ids) else 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

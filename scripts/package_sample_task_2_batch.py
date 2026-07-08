#!/usr/bin/env python3
"""Package sample_task_2 tasks into category-organized zips with rubric.txt included."""

from __future__ import annotations

import argparse
import ast
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SAMPLE_ROOT = REPO / "sample_task_2" / "sample_task_2"
PACKAGES = REPO / "sample_task_2" / "packages"

try:
    from scripts import package_task, validate_submission_zip
except ImportError:  # pragma: no cover
    import package_task
    import validate_submission_zip

FLAT_TEST_SH = """#!/bin/bash

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile."
    exit 1
fi

# Don't change anything below this line except for adding additional Python dependencies
# Harbor runs the verifier via bash -lc, which drops Dockerfile ENV PATH.
/opt/verifier/bin/pytest --ctrf /logs/verifier/ctrf.json /tests/test_outputs.py -rA

# Produce reward file (REQUIRED)
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
"""

SIGNAL = "When this part is complete, signal completion before moving on to the next part of the work."
PLATFORM_MAX_TIMEOUT_SEC = 1800
ALLOWED_SCORES = frozenset({1, 2, 3, 5})
FORBIDDEN_ROOT = frozenset(validate_submission_zip.FORBIDDEN_ROOT_FILES) - {"rubric.txt", "rubrics.txt"}


def discover_tasks() -> list[Path]:
    return [
        p.parent
        for p in sorted(SAMPLE_ROOT.rglob("task.toml"))
        if p.parent.parent.parent == SAMPLE_ROOT
    ]


def milestone_count(task_dir: Path) -> int:
    text = (task_dir / "task.toml").read_text(encoding="utf-8")
    match = re.search(r"number_of_milestones\s*=\s*(\d+)", text)
    return int(match.group(1)) if match else 0


def flatten_toml(text: str, ms_count: int) -> str:
    text = re.sub(r"number_of_milestones\s*=\s*\d+", "number_of_milestones = 0", text)
    text = re.sub(r"\n\[\[steps\]\][\s\S]*?(?=\n\[reference_pattern\]|\Z)", "\n", text)
    agent_timeout = min(PLATFORM_MAX_TIMEOUT_SEC, 600 * ms_count)
    verifier_timeout = min(PLATFORM_MAX_TIMEOUT_SEC, 433 * ms_count)
    if "[agent]" not in text:
        insert_at = text.find("[environment]")
        block = f"\n[agent]\ntimeout_sec = {agent_timeout}\n\n[verifier]\ntimeout_sec = {verifier_timeout}\n\n"
        if insert_at >= 0:
            text = text[:insert_at] + block + text[insert_at:]
        else:
            text = text.rstrip() + "\n" + block
    return text


def strip_signal(text: str) -> str:
    lines = [ln for ln in text.splitlines() if ln.strip() != SIGNAL]
    return "\n".join(lines).strip()


def flat_instruction(task_dir: Path, ms_count: int) -> str:
    parts: list[str] = []
    for idx in range(1, ms_count + 1):
        path = task_dir / "steps" / f"milestone_{idx}" / "instruction.md"
        if path.is_file():
            parts.append(strip_signal(path.read_text(encoding="utf-8")))
    if not parts:
        raise FileNotFoundError(f"missing milestone instructions in {task_dir}")
    intro = parts[0]
    if ms_count == 1:
        return intro + "\n"
    body = parts[-1]
    if intro == body:
        return intro + "\n"
    return f"{intro}\n\n{body}\n"


def method_to_function(method_src: str) -> str:
    tree = ast.parse(method_src)
    fn = tree.body[0]
    if not isinstance(fn, ast.FunctionDef):
        raise ValueError("expected function definition")
    fn.args.args = []
    return ast.unparse(fn).strip() + "\n"


def merge_tests(task_dir: Path, ms_count: int) -> str:
    chunks: list[str] = []
    for idx in range(1, ms_count + 1):
        path = task_dir / "steps" / f"milestone_{idx}" / "tests" / f"test_m{idx}.py"
        if not path.is_file():
            raise FileNotFoundError(path)
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text)
        if idx == 1:
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    break
                chunks.append(ast.unparse(node).strip() + "\n")
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):
                        chunks.append(method_to_function(ast.unparse(item)))
    return "\n".join(chunks).rstrip() + "\n"


def copy_environment(task_dir: Path, staging: Path) -> None:
    src = task_dir / "environment"
    dst = staging / "environment"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def stage_flat_task(task_dir: Path, staging: Path) -> None:
    ms_count = milestone_count(task_dir)
    if ms_count < 1:
        raise ValueError(f"{task_dir.name}: invalid milestone count")

    rubric_src = task_dir / "rubric.txt"
    if not rubric_src.is_file():
        raise FileNotFoundError(f"missing rubric.txt in {task_dir}")

    copy_environment(task_dir, staging)
    (staging / "task.toml").write_text(
        flatten_toml((task_dir / "task.toml").read_text(encoding="utf-8"), ms_count),
        encoding="utf-8",
    )
    (staging / "instruction.md").write_text(flat_instruction(task_dir, ms_count), encoding="utf-8")
    shutil.copy2(rubric_src, staging / "rubric.txt")

    solve_src = task_dir / "steps" / f"milestone_{ms_count}" / "solution" / f"solve{ms_count}.sh"
    if not solve_src.is_file():
        raise FileNotFoundError(solve_src)
    sol_dir = staging / "solution"
    sol_dir.mkdir(parents=True, exist_ok=True)
    solve_dst = sol_dir / "solve.sh"
    shutil.copy2(solve_src, solve_dst)
    solve_dst.chmod(0o755)

    tests_dir = staging / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    (tests_dir / "test_outputs.py").write_text(merge_tests(task_dir, ms_count), encoding="utf-8")
    test_sh = tests_dir / "test.sh"
    test_sh.write_text(FLAT_TEST_SH, encoding="utf-8")
    test_sh.chmod(0o755)


def validate_rubric(text: str) -> list[str]:
    failures: list[str] = []
    sections = re.split(r"^# Rubric \d+\s*$", text, flags=re.M)
    blocks = [block.strip() for block in sections[1:] if block.strip()]
    if not blocks:
        failures.append("rubric.txt has no # Rubric sections")
        return failures

    total_negatives = 0
    for idx, block in enumerate(blocks, start=1):
        positives = 0
        negatives = 0
        for line in block.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if not line.startswith("Agent "):
                failures.append(f"rubric {idx}: line must start with 'Agent ': {line[:60]}")
                continue
            match = re.search(r",\s*([+-])(\d+)\s*$", line)
            if not match:
                failures.append(f"rubric {idx}: line missing score suffix: {line[:60]}")
                continue
            sign, value = match.group(1), int(match.group(2))
            if value not in ALLOWED_SCORES:
                failures.append(f"rubric {idx}: score must be one of ±1,±2,±3,±5: {line[:60]}")
            if sign == "-":
                negatives += 1
                total_negatives += 1
            else:
                positives += value
        if positives < 10 or positives > 40:
            failures.append(f"rubric {idx}: positive total must be 10–40 (found {positives})")
        if negatives < 2:
            failures.append(f"rubric {idx}: needs at least 2 negative criteria (found {negatives})")

    if total_negatives < 3:
        failures.append(f"rubric needs at least 3 negative criteria overall (found {total_negatives})")
    return failures


def validate_sample_zip(zip_path: Path) -> tuple[bool, list[str]]:
    report = validate_submission_zip.build_report(zip_path)
    failures = list(report.get("failures", []))
    passes = list(report.get("passes", []))

    # Standard validator bans rubric.txt; sample_task_2 packages require it.
    failures = [
        f
        for f in failures
        if "forbidden archive-root file(s) present: rubric.txt" not in f
        and "forbidden archive-root file(s) present: rubrics.txt" not in f
    ]
    if "rubric.txt" in report.get("root_files", []):
        passes.append("rubric.txt present at archive root")
    else:
        failures.append("missing required archive-root file: rubric.txt")

    for forbidden in sorted(FORBIDDEN_ROOT & set(report.get("root_files", []))):
        failures.append(f"forbidden archive-root file present: {forbidden}")

    members = validate_submission_zip.inspect_archive(zip_path)
    names = {m["name"] for m in members}
    required = (
        "instruction.md",
        "task.toml",
        "rubric.txt",
        "environment/Dockerfile",
        "solution/solve.sh",
        "tests/test.sh",
        "tests/test_outputs.py",
    )
    for req in required:
        if req not in names:
            failures.append(f"missing required archive member: {req}")

    rubric_member = next((m for m in members if m["name"] == "rubric.txt" and not m["is_dir"]), None)
    if rubric_member:
        with zipfile.ZipFile(zip_path) as archive:
            rubric_text = archive.read("rubric.txt").decode("utf-8")
        failures.extend(validate_rubric(rubric_text))

    ok = not failures
    return ok, failures if failures else passes


def create_sample_zip(staging: Path, out_zip: Path) -> None:
    report = package_task.create_package(staging, out_zip)
    if report["status"] != "PASS":
        raise RuntimeError("; ".join(report.get("failures", ["package failed"])))

    rubric_src = staging / "rubric.txt"
    with zipfile.ZipFile(out_zip, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(rubric_src, "rubric.txt")


def package_task_dir(task_dir: Path, validate: bool) -> tuple[int, str]:
    slug = task_dir.name
    category = task_dir.parent.name
    out_zip = PACKAGES / category / f"{slug}.zip"
    out_zip.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"sample-task-2-{slug}-") as tmp:
        staging = Path(tmp) / slug
        staging.mkdir(parents=True)
        stage_flat_task(task_dir, staging)
        create_sample_zip(staging, out_zip)

    if not validate:
        return 0, ""

    ok, messages = validate_sample_zip(out_zip)
    output = "\n".join(messages)
    return (0 if ok else 1), output


def cleanup_flat_packages() -> None:
    for path in PACKAGES.glob("*.zip"):
        path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create category-organized sample_task_2 zips with rubric.txt."
    )
    parser.add_argument("--validate", action="store_true", help="Validate each archive")
    parser.add_argument("--slug", help="Package only this task slug")
    parser.add_argument(
        "--keep-flat",
        action="store_true",
        help="Keep legacy flat zips at packages/ root (default: remove them)",
    )
    args = parser.parse_args()

    tasks = discover_tasks()
    if args.slug:
        tasks = [t for t in tasks if t.name == args.slug]
        if not tasks:
            print(f"No task found for slug: {args.slug}", file=sys.stderr)
            return 1

    PACKAGES.mkdir(parents=True, exist_ok=True)
    if not args.keep_flat:
        cleanup_flat_packages()

    failures = 0
    for task_dir in tasks:
        rc, output = package_task_dir(task_dir, validate=args.validate)
        category = task_dir.parent.name
        status = "PASS" if rc == 0 else "FAIL"
        print(f"{category}/{task_dir.name}: {status}")
        if rc != 0:
            failures += 1
            print(output, file=sys.stderr)

    print(
        f"Packaged {len(tasks) - failures}/{len(tasks)} tasks -> "
        f"{PACKAGES.relative_to(REPO)}/<category>/<slug>.zip"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Generate sample_task_2/TaskIndex.md from validation_results.json."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESULTS = REPO / "sample_task_2" / "validation_results.json"
OUT = REPO / "sample_task_2" / "TaskIndex.md"


def main() -> None:
    if not RESULTS.is_file():
        OUT.write_text("# sample_task_2 Task Index\n\nRun `python3 scripts/validate_sample_task_2_batch.py` first.\n", encoding="utf-8")
        print(f"Wrote placeholder {OUT}")
        return
    data = json.loads(RESULTS.read_text(encoding="utf-8"))
    rows = data.get("tasks", [])
    lines = [
        "# sample_task_2 Task Index",
        "",
        f"Generated from `sample_task_2/Ideas.md`. Tasks: **{len(rows)}**.",
        "",
        "| Category | Slug | Milestones | Tests | Template | Harbor |",
        "|---|---|---:|---:|---|---|",
    ]
    for row in sorted(rows, key=lambda r: (r["category"], r["slug"])):
        tmpl = "OK" if row.get("template", {}).get("ok") else "FAIL"
        harbor = row.get("harbor_rc")
        if harbor == 0:
            harbor_s = "PASS"
        elif harbor == 1:
            harbor_s = "FAIL"
        else:
            harbor_s = "n/a"
        lines.append(
            f"| {row['category']} | `{row['slug']}` | {row.get('milestone_count', '?')} | "
            f"{row.get('test_count', '?')} | {tmpl} | {harbor_s} |"
        )
    lines.extend(["", "## Paths", "", "- Tasks: `sample_task_2/sample_task_2/<category>/<slug>/`", "- Evidence: `sample_task_2/evidence/<slug>/`", ""])
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()

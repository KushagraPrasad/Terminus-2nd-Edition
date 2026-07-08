#!/usr/bin/env python3
"""Generate rubric.txt for each sample_task_2 task."""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "sample_task_2" / "sample_task_2"

FOCUS: dict[str, str] = {
    "proprietary-log-format-inference": "record boundary and checksum rules",
    "query-plan-cost-model-optimize": "plan ranking under cardinality budget",
    "game-logic-invariant-model-check": "turn-rule obligations across cases",
    "ai-search-transposition-optimize": "search strength under memory budget",
    "checkpoint-resume-optimizer-state": "optimizer moment buffer threading",
    "differentiable-pipeline-invariant-proof": "gradient sum obligations across fused ops",
    "legacy-bytecode-vm-inference": "stack semantics across opcode widths",
    "typestate-protocol-proof": "session phase transition obligations",
    "core-dump-stack-inference": "unwind table and frame chain agreement",
    "bisect-budget-optimizer": "minimal repro under step budget",
    "pii-redaction-variant-ladder": "redaction closure across variant ladder cases",
    "schema-inference-variant-ladder": "nullable field ordering across variants",
    "regex-extraction-trace-inference": "capture group alignment across trace chunks",
    "data-lineage-invariant-proof": "fork edge agreement with durable journals",
    "stream-window-aggregate-drift": "window aggregate agreement under watermark lag",
    "procedural-level-variant-ladder": "spawn legality across generated variants",
    "input-remap-variant-ladder": "remap combo validity across profiles",
    "pathfinding-memory-optimize-grid": "admissible paths under memory budget",
    "spawn-cadence-variant-ladder": "cadence timing across variant waves",
    "collision-layer-variant-ladder": "overlap rules across layer masks",
    "ood-detection-variant-ladder": "shift detection across ladder slices",
    "prompt-injection-eval-ladder": "injection scoring across eval ladder cases",
    "calibration-isotonic-monotonic-proof": "monotonic calibration across bucket merges",
    "sampler-shard-divergence-repair": "shard epoch agreement after resume",
    "mixed-precision-replay-ladder": "numeric replay closure across ladder steps",
    "minimal-http-router-under-size-cap": "route table fit under size cap",
    "constraint-serializer-builder": "field tag completeness in serialized output",
    "allocator-pool-size-optimize": "reuse metrics under pool size budget",
    "wire-protocol-from-pcap-inference": "framing rules inferred from PCAP excerpts",
    "codec-framing-variant-ladder": "frame integrity across codec variants",
    "deterministic-chaos-injector": "idempotent recovery after injected faults",
    "minimal-repro-harness-builder": "race isolation under scheduler seed budget",
    "scheduler-seed-replay-injector": "yield ordering under seed replay",
    "watchdog-restart-boundary-debug": "state hygiene across restart boundaries",
    "async-fault-injection-ladder": "journal agreement across fault ladder steps",
}


def milestone_count(task_dir: Path) -> int:
    text = (task_dir / "task.toml").read_text(encoding="utf-8")
    m = re.search(r"number_of_milestones\s*=\s*(\d+)", text)
    return int(m.group(1)) if m else 3


def discover_runner(task_dir: Path) -> str:
    tools = task_dir / "environment" / "tools"
    for p in sorted(tools.glob("*_runner.py")):
        return f"python3 -m environment.tools.{p.stem}"
    return "python3 -m environment.tools.runner_q"


def rubric_block_index(ms: int, milestone_idx: int) -> int:
    """Map milestone index (0-based) to rubric block role."""
    if milestone_idx == 0:
        return 0
    if milestone_idx == ms - 1:
        return 3
    if ms >= 4 and milestone_idx == ms - 2:
        return 2
    return 1


def rubric_for(slug: str, ms: int, runner: str) -> str:
    focus = FOCUS.get(slug, "documented row gates and digest rules")
    blocks: list[list[str]] = [
        [
            f"Agent inspects primary helper modules under /app/environment before editing unrelated paths, +3",
            f"Agent runs {runner} to reproduce lab symptoms, +3",
            f"Agent traces ancestry closure and digest materialization instead of anchor-only summaries, +3",
            f"Agent documents helper-level closure findings before editing bundle code, +2",
            f"Agent hand-writes /app/output JSON without regenerating through the runner, -5",
            f"Agent edits tests, solution/, or verifier fixtures instead of environment source, -5",
            f"Agent relies on keyword grep without executing the documented runner command, -2",
        ],
        [
            f"Agent fixes bundle materialization to match documented digest and epoch rules, +3",
            f"Agent coordinates gate helpers with row-level closure checks, +3",
            f"Agent reconciles coupled helpers instead of patching a single module in isolation, +3",
            f"Agent reruns {runner} after each substantive helper change, +2",
            f"Agent patches only one helper while leaving coupled false-green gates broken, -3",
            f"Agent introduces nondeterministic ordering in regenerated output, -3",
            f"Agent skips rerunning the documented runner after helper edits, -2",
        ],
        [
            f"Agent validates {focus} across all shipped cases before finishing, +3",
            f"Agent honors single-case CLI replacement instead of appending stale rows, +3",
            f"Agent checks row gates against fixture truth for every case label, +3",
            f"Agent compares regenerated digests to expected materialization rules, +2",
            f"Agent leaves replay journal links ignored or archived rows treated as active, -3",
            f"Agent appends stale rows during single-case CLI runs, -3",
            f"Agent trusts cached output without rerunning the full matrix, -2",
        ],
        [
            f"Agent ensures repeated runner invocations are byte-stable without mutating fixtures, +3",
            f"Agent confirms overall_pass reflects the conjunction of row gates, +3",
            f"Agent verifies terminal matrix success before declaring completion, +3",
            f"Agent preserves fixture bytes across rerender checks, +2",
            f"Agent declares done after a local smoke check while terminal matrix still fails, -3",
            f"Agent mutates case fixtures to force a passing report, -3",
            f"Agent stops after a single passing case while other labels still fail, -2",
        ],
    ]
    lines: list[str] = []
    for i in range(ms):
        lines.append(f"# Rubric {i + 1}")
        lines.extend(blocks[rubric_block_index(ms, i)])
    return "\n".join(lines) + "\n"


def main() -> None:
    for toml in sorted(ROOT.rglob("task.toml")):
        if toml.parent.parent.parent != ROOT:
            continue
        slug = toml.parent.name
        ms = milestone_count(toml.parent)
        runner = discover_runner(toml.parent)
        out = toml.parent / "rubric.txt"
        out.write_text(rubric_for(slug, ms, runner), encoding="utf-8")
        print(out)


if __name__ == "__main__":
    main()

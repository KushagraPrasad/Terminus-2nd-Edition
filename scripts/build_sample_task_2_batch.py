#!/usr/bin/env python3
"""Generate sample_task_2 batch: hard milestone tasks with distinct domain engines."""

from __future__ import annotations

import json
import textwrap
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "sample_task_2" / "sample_task_2"

DOCKERFILE = """FROM python:3.11-slim-bookworm@sha256:cd67330292a51e2963156f74ff340455d66b2172e9190e99f40dff9357471177
WORKDIR /app
# verifier-bake-v2: offline pytest in /opt/verifier

RUN apt-get update && apt-get install -y --no-install-recommends \\
  tmux \\
  asciinema \\
  python3=3.11.2-1+b1 \\
  python3-venv=3.11.2-1+b1 \\
  curl=7.88.1-10+deb12u14 \\
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/verifier
RUN /opt/verifier/bin/pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5
ENV PATH=/opt/verifier/bin:${PATH}

ENV PYTHONPATH=/app
COPY . /app/environment
CMD ["python3", "-c", "print('Environment ready')"]
"""

TEST_SH = """#!/bin/bash

if [ "$PWD" = "/" ]; then
    echo "Error: No working directory set. Please set a WORKDIR in your Dockerfile."
    exit 1
fi

# Don't change anything below this line except for adding additional Python dependencies
# Harbor runs the verifier via bash -lc, which drops Dockerfile ENV PATH.
/opt/verifier/bin/pytest --ctrf /logs/verifier/ctrf.json /tests/test_m{idx}.py -rA

# Produce reward file (REQUIRED)
if [ $? -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
"""

SOLVE_WRAP = """#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
bash "$SCRIPT_DIR/solve{idx}.sh"
"""

SIGNAL = "When this part is complete, signal completion before moving on to the next part of the work."

FIELD_GUIDE = """# Field guide

Rows expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok, and overall_pass.

## Closure graph

- Start from case anchors and walk **forward** along parent links and allowed journal edges.
- Include only live records with `epoch <= max_epoch` (exclude `state == archived`).
- Journal edges use kinds `carry`, `recover`, or `handoff` with `generation <= max_epoch`; ignore other kinds and missing endpoints.

## Ordering and digest

- `materialized_ids` must be sorted by `(lane, id)` — the same ordering used for digest materialization.
- Digest input joins selected records with `|` between tuples: `id:epoch:lane:payload` (lane/id order within the selected set).
- `ancestry_pairs` lists retained parent→child pairs from the closure graph.
- `epoch_total` sums epochs of all materialized records.

## Row gates

- `closure_ok`, `digest_ok`, and `epoch_ok` must be true per row; `overall_pass` is their conjunction across all cases.
"""


def operator_notes(spec: TaskSpec) -> str:
    return (
        f"Use `python3 -m {spec.runner}` to regenerate the report.\n"
        f"Single-case mode: `--case <label>` **replaces** the output file with exactly one row for that case label (not a merged multi-row report).\n"
        f"Primary helpers live under `/app/environment` in the task-specific module tree (e.g. `{spec.mod_a}`); there is no separate `closure_helpers.py`.\n"
    )


@dataclass
class TaskSpec:
    slug: str
    category: str
    title: str
    tags: list[str]
    milestones: int
    task_shape: str
    evidence: str
    runner: str
    report_file: str
    mod_a: str
    mod_b: str
    mod_c: str
    mod_d: str
    sym_a: str
    sym_b: str
    sym_c: str
    sym_d: str
    test_split: list[list[str]]
    forbidden: list[str]


def report_stem(slug: str) -> str:
    return slug.replace("-", "_")


def cases_graph(slug: str) -> list[dict]:
    base = [
        {
            "label": "alpha",
            "max_epoch": 3,
            "anchors": ["r1"],
            "records": [
                {"id": "r1", "parent": "", "epoch": 1, "lane": "east", "payload": "p1", "state": "live"},
                {"id": "r2", "parent": "r1", "epoch": 2, "lane": "east", "payload": "p2", "state": "live"},
                {"id": "r3", "parent": "r2", "epoch": 3, "lane": "west", "payload": "p3", "state": "live"},
                {"id": "r4", "parent": "r1", "epoch": 4, "lane": "west", "payload": "p4", "state": "archived"},
            ],
            "journals": [
                {"src": "r2", "dst": "r3", "kind": "carry", "generation": 2},
            ],
        },
        {
            "label": "beta",
            "max_epoch": 2,
            "anchors": ["s1", "s2"],
            "records": [
                {"id": "s1", "parent": "", "epoch": 1, "lane": "north", "payload": "a1", "state": "live"},
                {"id": "s2", "parent": "", "epoch": 1, "lane": "south", "payload": "a2", "state": "live"},
                {"id": "s3", "parent": "s1", "epoch": 2, "lane": "north", "payload": "a3", "state": "live"},
            ],
            "journals": [
                {"src": "s1", "dst": "s3", "kind": "recover", "generation": 2},
                {"src": "s2", "dst": "s3", "kind": "handoff", "generation": 2},
            ],
        },
        {
            "label": "gamma",
            "max_epoch": 4,
            "anchors": ["t1"],
            "records": [
                {"id": "t1", "parent": "", "epoch": 2, "lane": "core", "payload": "z1", "state": "live"},
                {"id": "t2", "parent": "t1", "epoch": 3, "lane": "core", "payload": "z2", "state": "live"},
                {"id": "t3", "parent": "t2", "epoch": 4, "lane": "edge", "payload": "z3", "state": "live"},
            ],
            "journals": [],
        },
        {
            "label": "delta",
            "max_epoch": 3,
            "anchors": ["u1"],
            "records": [
                {"id": "u1", "parent": "", "epoch": 1, "lane": "laneA", "payload": "k1", "state": "live"},
                {"id": "u2", "parent": "u1", "epoch": 2, "lane": "laneB", "payload": "k2", "state": "live"},
                {"id": "u3", "parent": "u2", "epoch": 5, "lane": "laneB", "payload": "k3", "state": "live"},
            ],
            "journals": [
                {"src": "u1", "dst": "u2", "kind": "carry", "generation": 3},
            ],
        },
        {
            "label": "epsilon",
            "max_epoch": 2,
            "anchors": ["v1"],
            "records": [
                {"id": "v1", "parent": "", "epoch": 1, "lane": "main", "payload": "m1", "state": "live"},
                {"id": "v2", "parent": "v1", "epoch": 2, "lane": "main", "payload": "m2", "state": "live"},
            ],
            "journals": [
                {"src": "v1", "dst": "v2", "kind": "handoff", "generation": 1},
            ],
        },
    ]
    return base


TASKS: list[TaskSpec] = [
    TaskSpec(
        "proprietary-log-format-inference",
        "data-processing",
        "Proprietary Log Format Inference",
        ["binary-log", "inference", "decoder", "data-processing", "reverse-engineering"],
        4,
        "reverse_engineering",
        "production binary log shards with generation-specific length prefixes and checksum scope",
        "environment.tools.decode_runner",
        f"{report_stem('proprietary-log-format-inference')}_report.json",
        "environment/hdr/width_p.py",
        "environment/rec/field_q.py",
        "environment/sum/chk_r.py",
        "environment/fmt/mask_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_cross_row_gates_hold"],
            ["test_single_case_cli_and_determinism"],
        ],
        ["log", "decoder", "inference", "proprietary", "format"],
    ),
    TaskSpec(
        "query-plan-cost-model-optimize",
        "data-processing",
        "Query Plan Cost Model Optimize",
        ["query-plan", "optimizer", "cost-model", "data-processing", "budget"],
        3,
        "optimization_under_constraints",
        "warehouse planner underestimates join fanout under cardinality caps",
        "environment.tools.plan_runner",
        f"{report_stem('query-plan-cost-model-optimize')}_report.json",
        "environment/plan/cost_p.py",
        "environment/plan/rank_q.py",
        "environment/plan/gate_r.py",
        "environment/plan/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_single_case_cli_and_determinism", "test_overall_pass_conjunction", "test_deterministic_rerender"],
        ],
        ["query", "plan", "cost", "optimizer", "budget"],
    ),
    TaskSpec(
        "game-logic-invariant-model-check",
        "games",
        "Game Logic Invariant Model Check",
        ["game-logic", "invariants", "formal", "model-check", "rules"],
        3,
        "formal_reasoning",
        "turn-based engine accepts illegal captures when en passant window drifts",
        "environment.tools.rules_runner",
        f"{report_stem('game-logic-invariant-model-check')}_report.json",
        "environment/rules/move_p.py",
        "environment/rules/state_q.py",
        "environment/rules/gate_r.py",
        "environment/rules/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_single_case_cli_and_determinism", "test_overall_pass_conjunction", "test_deterministic_rerender"],
        ],
        ["game", "invariant", "model", "check", "rules"],
    ),
    TaskSpec(
        "ai-search-transposition-optimize",
        "games",
        "AI Search Transposition Optimize",
        ["transposition", "search", "optimization", "games", "hash-table"],
        4,
        "optimization_under_constraints",
        "deterministic search loses best move when table eviction breaks collision policy",
        "environment.tools.search_runner",
        f"{report_stem('ai-search-transposition-optimize')}_report.json",
        "environment/search/hash_p.py",
        "environment/search/table_q.py",
        "environment/search/gate_r.py",
        "environment/search/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_cross_row_gates_hold"],
            ["test_single_case_cli_and_determinism"],
        ],
        ["search", "transposition", "optimize", "hash", "table"],
    ),
    TaskSpec(
        "checkpoint-resume-optimizer-state",
        "machine-learning",
        "Checkpoint Resume Optimizer State",
        ["checkpoint", "resume", "optimizer", "machine-learning", "training"],
        3,
        "repair_existing_system",
        "training resume spikes loss when Adam bias correction uses stale global step",
        "environment.tools.train_runner",
        f"{report_stem('checkpoint-resume-optimizer-state')}_report.json",
        "environment/train/opt_p.py",
        "environment/train/sched_q.py",
        "environment/train/gate_r.py",
        "environment/train/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_single_case_cli_and_determinism", "test_overall_pass_conjunction", "test_deterministic_rerender"],
        ],
        ["checkpoint", "resume", "optimizer", "training", "state"],
    ),
    TaskSpec(
        "differentiable-pipeline-invariant-proof",
        "machine-learning",
        "Differentiable Pipeline Invariant Proof",
        ["differentiable", "pipeline", "invariants", "machine-learning", "gradients"],
        4,
        "formal_reasoning",
        "autograd pipeline violates documented gradient sum invariants across fused ops",
        "environment.tools.pipe_runner",
        f"{report_stem('differentiable-pipeline-invariant-proof')}_report.json",
        "environment/pipe/grad_p.py",
        "environment/pipe/inv_q.py",
        "environment/pipe/gate_r.py",
        "environment/pipe/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_cross_row_gates_hold"],
            ["test_single_case_cli_and_determinism"],
        ],
        ["differentiable", "pipeline", "invariant", "proof", "gradient"],
    ),
    TaskSpec(
        "legacy-bytecode-vm-inference",
        "software-engineering",
        "Legacy Bytecode VM Inference",
        ["bytecode", "vm", "inference", "software-engineering", "interpreter"],
        4,
        "reverse_engineering",
        "stack VM opcode widths change mid-image without magic header bump",
        "environment.tools.vm_runner",
        f"{report_stem('legacy-bytecode-vm-inference')}_report.json",
        "environment/vm/stack_p.py",
        "environment/vm/op_q.py",
        "environment/vm/gate_r.py",
        "environment/vm/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_cross_row_gates_hold"],
            ["test_single_case_cli_and_determinism"],
        ],
        ["bytecode", "vm", "inference", "stack", "opcode"],
    ),
    TaskSpec(
        "typestate-protocol-proof",
        "software-engineering",
        "Typestate Protocol Proof",
        ["typestate", "protocol", "proof", "software-engineering", "transitions"],
        3,
        "formal_reasoning",
        "RPC layer accepts requests in wrong session phase after idle timeout",
        "environment.tools.proto_runner",
        f"{report_stem('typestate-protocol-proof')}_report.json",
        "environment/proto/state_p.py",
        "environment/proto/trans_q.py",
        "environment/proto/gate_r.py",
        "environment/proto/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_single_case_cli_and_determinism", "test_overall_pass_conjunction", "test_deterministic_rerender"],
        ],
        ["typestate", "protocol", "proof", "transition", "session"],
    ),
    TaskSpec(
        "core-dump-stack-inference",
        "debugging",
        "Core Dump Stack Inference",
        ["core-dump", "stack", "unwind", "debugging", "inference"],
        4,
        "reverse_engineering",
        "unwind tables disagree with frame pointer chain on compact cores",
        "environment.tools.stack_runner",
        f"{report_stem('core-dump-stack-inference')}_report.json",
        "environment/unwind/frame_p.py",
        "environment/unwind/table_q.py",
        "environment/unwind/gate_r.py",
        "environment/unwind/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_cross_row_gates_hold"],
            ["test_single_case_cli_and_determinism"],
        ],
        ["core", "dump", "stack", "unwind", "inference"],
    ),
    TaskSpec(
        "bisect-budget-optimizer",
        "debugging",
        "Bisect Budget Optimizer",
        ["bisect", "budget", "optimizer", "debugging", "repro"],
        3,
        "optimization_under_constraints",
        "git bisect harness exhausts step budget before isolating flaky commit",
        "environment.tools.bisect_runner",
        f"{report_stem('bisect-budget-optimizer')}_report.json",
        "environment/bisect/part_p.py",
        "environment/bisect/policy_q.py",
        "environment/bisect/gate_r.py",
        "environment/bisect/fmt_s.py",
        "fn_p", "fn_q", "fn_r", "fn_s",
        [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_single_case_cli_and_determinism", "test_overall_pass_conjunction", "test_deterministic_rerender"],
        ],
        ["bisect", "budget", "optimizer", "repro", "commit"],
    ),
]


def test_split_for(milestones: int) -> list[list[str]]:
    if milestones >= 4:
        return [
            ["test_helper_closure_ignores_bad_links"],
            ["test_rows_match_fixture_truth"],
            ["test_cross_row_gates_hold"],
            ["test_single_case_cli_and_determinism"],
        ]
    return [
        ["test_helper_closure_ignores_bad_links"],
        ["test_rows_match_fixture_truth"],
        [
            "test_single_case_cli_and_determinism",
            "test_overall_pass_conjunction",
            "test_deterministic_rerender",
        ],
    ]


def make_spec(
    slug: str,
    category: str,
    title: str,
    tags: list[str],
    milestones: int,
    task_shape: str,
    evidence: str,
    mod_prefix: str,
    runner_stem: str,
    forbidden: list[str],
) -> TaskSpec:
    return TaskSpec(
        slug,
        category,
        title,
        tags,
        milestones,
        task_shape,
        evidence,
        f"environment.tools.{runner_stem}",
        f"{report_stem(slug)}_report.json",
        f"environment/{mod_prefix}/slot_a.py",
        f"environment/{mod_prefix}/bundle_b.py",
        f"environment/{mod_prefix}/guard_c.py",
        f"environment/{mod_prefix}/mask_d.py",
        "fn_a",
        "fn_b",
        "fn_c",
        "fn_d",
        test_split_for(milestones),
        forbidden,
    )


EXTRA_TASKS: list[TaskSpec] = [
    # data-processing (+5)
    make_spec(
        "pii-redaction-variant-ladder",
        "data-processing",
        "PII Redaction Variant Ladder",
        ["pii", "redaction", "variant-ladder", "data-processing", "privacy"],
        4,
        "adversarial_generalization",
        "redaction pipeline keeps stale tokens when variant ladder ordering drifts",
        "redact",
        "redact_runner",
        ["pii", "redaction", "variant", "ladder", "privacy"],
    ),
    make_spec(
        "schema-inference-variant-ladder",
        "data-processing",
        "Schema Inference Variant Ladder",
        ["schema", "inference", "variant-ladder", "data-processing", "typing"],
        4,
        "reverse_engineering",
        "schema inference mis-orders nullable fields across variant ladder cases",
        "schema",
        "schema_runner",
        ["schema", "inference", "variant", "ladder", "typing"],
    ),
    make_spec(
        "regex-extraction-trace-inference",
        "data-processing",
        "Regex Extraction Trace Inference",
        ["regex", "extraction", "trace", "data-processing", "inference"],
        3,
        "reverse_engineering",
        "regex extractor drops capture groups when trace spans cross chunk boundaries",
        "regex",
        "regex_runner",
        ["regex", "extraction", "trace", "inference", "capture"],
    ),
    make_spec(
        "data-lineage-invariant-proof",
        "data-processing",
        "Data Lineage Invariant Proof",
        ["lineage", "invariant", "proof", "data-processing", "provenance"],
        3,
        "formal_reasoning",
        "lineage graph reports closed ancestry while fork edges disagree with durable journals",
        "lineage",
        "lineage_runner",
        ["lineage", "invariant", "proof", "provenance", "graph"],
    ),
    make_spec(
        "stream-window-aggregate-drift",
        "data-processing",
        "Stream Window Aggregate Drift",
        ["stream", "window", "aggregate", "data-processing", "drift"],
        3,
        "optimization_under_constraints",
        "tumbling window aggregates drift when watermark lag crosses shard boundaries",
        "stream",
        "stream_runner",
        ["stream", "window", "aggregate", "watermark", "drift"],
    ),
    # games (+5)
    make_spec(
        "procedural-level-variant-ladder",
        "games",
        "Procedural Level Variant Ladder",
        ["procedural", "level", "variant-ladder", "games", "generation"],
        4,
        "adversarial_generalization",
        "procedural generator emits illegal spawn tiles on later variant ladder steps",
        "level",
        "level_runner",
        ["procedural", "level", "variant", "ladder", "spawn"],
    ),
    make_spec(
        "input-remap-variant-ladder",
        "games",
        "Input Remap Variant Ladder",
        ["input", "remap", "variant-ladder", "games", "controls"],
        3,
        "adversarial_generalization",
        "input remap table accepts out-of-order combos across variant ladder profiles",
        "remap",
        "remap_runner",
        ["input", "remap", "variant", "ladder", "controls"],
    ),
    make_spec(
        "pathfinding-memory-optimize-grid",
        "games",
        "Pathfinding Memory Optimize Grid",
        ["pathfinding", "memory", "optimization", "games", "grid"],
        4,
        "optimization_under_constraints",
        "grid pathfinder exceeds memory budget while breaking admissible heuristic guarantees",
        "path",
        "path_runner",
        ["pathfinding", "memory", "optimize", "grid", "heuristic"],
    ),
    make_spec(
        "spawn-cadence-variant-ladder",
        "games",
        "Spawn Cadence Variant Ladder",
        ["spawn", "cadence", "variant-ladder", "games", "timing"],
        3,
        "adversarial_generalization",
        "spawn cadence drifts across variant ladder waves while local counters look stable",
        "spawn",
        "spawn_runner",
        ["spawn", "cadence", "variant", "ladder", "timing"],
    ),
    make_spec(
        "collision-layer-variant-ladder",
        "games",
        "Collision Layer Variant Ladder",
        ["collision", "layer", "variant-ladder", "games", "physics"],
        3,
        "formal_reasoning",
        "collision layers disagree on overlap when variant ladder masks swap mid-tick",
        "collision",
        "collision_runner",
        ["collision", "layer", "variant", "ladder", "overlap"],
    ),
    # machine-learning (+5)
    make_spec(
        "ood-detection-variant-ladder",
        "machine-learning",
        "OOD Detection Variant Ladder",
        ["ood", "detection", "variant-ladder", "machine-learning", "robustness"],
        4,
        "adversarial_generalization",
        "OOD detector accepts shifted batches on later variant ladder slices",
        "ood",
        "ood_runner",
        ["ood", "detection", "variant", "ladder", "robustness"],
    ),
    make_spec(
        "prompt-injection-eval-ladder",
        "machine-learning",
        "Prompt Injection Eval Ladder",
        ["prompt", "injection", "eval-ladder", "machine-learning", "safety"],
        3,
        "adversarial_generalization",
        "eval harness scores injected prompts as benign on intermediate ladder cases",
        "inject",
        "inject_runner",
        ["prompt", "injection", "eval", "ladder", "safety"],
    ),
    make_spec(
        "calibration-isotonic-monotonic-proof",
        "machine-learning",
        "Calibration Isotonic Monotonic Proof",
        ["calibration", "isotonic", "monotonic", "machine-learning", "proof"],
        3,
        "formal_reasoning",
        "isotonic calibration breaks monotonicity after bucket merge on resume",
        "calib",
        "calib_runner",
        ["calibration", "isotonic", "monotonic", "proof", "bucket"],
    ),
    make_spec(
        "sampler-shard-divergence-repair",
        "machine-learning",
        "Sampler Shard Divergence Repair",
        ["sampler", "shard", "divergence", "machine-learning", "training"],
        3,
        "repair_existing_system",
        "distributed sampler shards disagree on epoch boundaries after resume",
        "sampler",
        "sampler_runner",
        ["sampler", "shard", "divergence", "training", "epoch"],
    ),
    make_spec(
        "mixed-precision-replay-ladder",
        "machine-learning",
        "Mixed Precision Replay Ladder",
        ["mixed-precision", "replay", "ladder", "machine-learning", "numeric"],
        4,
        "optimization_under_constraints",
        "mixed-precision replay ladder diverges when loss scaling skips micro-batch edges",
        "mprec",
        "mprec_runner",
        ["mixed", "precision", "replay", "ladder", "scaling"],
    ),
    # software-engineering (+5)
    make_spec(
        "minimal-http-router-under-size-cap",
        "software-engineering",
        "Minimal HTTP Router Under Size Cap",
        ["http", "router", "size-cap", "software-engineering", "embedded"],
        3,
        "constrained_build",
        "embedded router exceeds size cap while dropping trailing route table bytes",
        "router",
        "router_runner",
        ["http", "router", "size", "embedded", "route"],
    ),
    make_spec(
        "constraint-serializer-builder",
        "software-engineering",
        "Constraint Serializer Builder",
        ["serializer", "constraints", "builder", "software-engineering", "encoding"],
        4,
        "constrained_build",
        "constraint serializer omits field tags required by downstream validator arms",
        "serial",
        "serial_runner",
        ["serializer", "constraint", "builder", "encoding", "field"],
    ),
    make_spec(
        "allocator-pool-size-optimize",
        "software-engineering",
        "Allocator Pool Size Optimize",
        ["allocator", "pool", "optimize", "software-engineering", "memory"],
        3,
        "optimization_under_constraints",
        "pool allocator fragments under size-class budget while reporting healthy reuse",
        "alloc",
        "alloc_runner",
        ["allocator", "pool", "optimize", "memory", "fragment"],
    ),
    make_spec(
        "wire-protocol-from-pcap-inference",
        "software-engineering",
        "Wire Protocol From PCAP Inference",
        ["wire-protocol", "pcap", "inference", "software-engineering", "parser"],
        4,
        "reverse_engineering",
        "PCAP excerpts imply inconsistent length-prefix rules across connection arms",
        "pcap",
        "pcap_runner",
        ["wire", "protocol", "pcap", "inference", "framing"],
    ),
    make_spec(
        "codec-framing-variant-ladder",
        "software-engineering",
        "Codec Framing Variant Ladder",
        ["codec", "framing", "variant-ladder", "software-engineering", "binary"],
        3,
        "adversarial_generalization",
        "codec framing accepts truncated frames on later variant ladder profiles",
        "codec",
        "codec_runner",
        ["codec", "framing", "variant", "ladder", "binary"],
    ),
    # debugging (+5)
    make_spec(
        "deterministic-chaos-injector",
        "debugging",
        "Deterministic Chaos Injector",
        ["chaos", "injector", "deterministic", "debugging", "fault"],
        4,
        "constrained_build",
        "chaos injector repeats destructive step without idempotent recovery logging",
        "chaos",
        "chaos_runner",
        ["chaos", "injector", "deterministic", "fault", "recovery"],
    ),
    make_spec(
        "minimal-repro-harness-builder",
        "debugging",
        "Minimal Repro Harness Builder",
        ["minimal-repro", "harness", "builder", "debugging", "concurrency"],
        3,
        "constrained_build",
        "minimal repro harness hides race until scheduler seed budget is exhausted",
        "repro",
        "repro_runner",
        ["minimal", "repro", "harness", "race", "scheduler"],
    ),
    make_spec(
        "scheduler-seed-replay-injector",
        "debugging",
        "Scheduler Seed Replay Injector",
        ["scheduler", "seed", "replay", "debugging", "injector"],
        3,
        "optimization_under_constraints",
        "scheduler seed replay diverges when injector reorders yield points",
        "sched",
        "sched_runner",
        ["scheduler", "seed", "replay", "injector", "yield"],
    ),
    make_spec(
        "watchdog-restart-boundary-debug",
        "debugging",
        "Watchdog Restart Boundary Debug",
        ["watchdog", "restart", "boundary", "debugging", "recovery"],
        3,
        "repair_existing_system",
        "watchdog restart leaves half-upgraded state across boundary transitions",
        "watch",
        "watch_runner",
        ["watchdog", "restart", "boundary", "recovery", "state"],
    ),
    make_spec(
        "async-fault-injection-ladder",
        "debugging",
        "Async Fault Injection Ladder",
        ["async", "fault", "injection", "debugging", "ladder"],
        4,
        "adversarial_generalization",
        "async fault ladder reports green locally while durable journals disagree",
        "fault",
        "fault_runner",
        ["async", "fault", "injection", "ladder", "journal"],
    ),
]

TASKS.extend(EXTRA_TASKS)


def mod_path_to_pkg(path: str) -> str:
    return path.replace("/", ".").replace(".py", "")


def broken_slot_py(spec: TaskSpec) -> str:
    return textwrap.dedent(
        f'''
        from __future__ import annotations

        def {spec.sym_a}(records: list[dict], journals: list[dict], anchors: list[str], limit: int) -> dict:
            active = {{str(r.get("id", "")): r for r in records if r.get("state") != "archived"}}
            seen: set[str] = set()
            stack = [a for a in anchors if a in active]
            pairs: set[tuple[str, str]] = set()
            while stack:
                item_x = stack.pop(0)
                if item_x in seen:
                    continue
                seen.add(item_x)
                parent = str(active.get(item_x, {{}}).get("parent", ""))
                if parent and parent in active:
                    pairs.add((parent, item_x))
                    if parent not in seen:
                        stack.append(parent)
            return {{"ids": sorted(seen), "pairs": sorted([list(p) for p in pairs])}}
        '''
    ).strip() + "\n"


def broken_bundle_py(spec: TaskSpec) -> str:
    d_mod = mod_path_to_pkg(spec.mod_d)
    return textwrap.dedent(
        f'''
        from __future__ import annotations
        import hashlib
        from {d_mod} import {spec.sym_d}

        def {spec.sym_b}(records: list[dict], ids: list[str]) -> dict:
            by_id = {{str(r.get("id", "")): r for r in records}}
            selected = [by_id[i] for i in ids if i in by_id]
            text = "|".join({spec.sym_d}(r) for r in selected)
            return {{
                "materialized_ids": [str(r.get("id", "")) for r in selected],
                "digest_hex": hashlib.sha256(text.encode()).hexdigest(),
                "epoch_total": sum(int(r.get("epoch", 0)) for r in selected[:2]),
            }}
        '''
    ).strip() + "\n"


def broken_guard_py(spec: TaskSpec) -> str:
    return textwrap.dedent(
        f'''
        from __future__ import annotations

        def {spec.sym_c}(case: dict, view: dict, bundle: dict) -> dict:
            anchor_count = len([x for x in case.get("anchors", []) if x in set(bundle.get("materialized_ids", []))])
            ok = anchor_count == len(case.get("anchors", []))
            return {{
                "closure_ok": ok,
                "digest_ok": ok,
                "epoch_ok": ok,
            }}
        '''
    ).strip() + "\n"


def mask_py(spec: TaskSpec) -> str:
    return textwrap.dedent(
        f'''
        from __future__ import annotations

        def {spec.sym_d}(row: dict) -> str:
            return str(row.get("payload", ""))
        '''
    ).strip() + "\n"


def emit_py(spec: TaskSpec) -> str:
    b_mod = mod_path_to_pkg(spec.mod_b)
    c_mod = mod_path_to_pkg(spec.mod_c)
    return textwrap.dedent(
        f'''
        from __future__ import annotations
        from {b_mod} import {spec.sym_b}
        from {c_mod} import {spec.sym_c}

        def fn_emit(case: dict, view: dict) -> tuple[dict, dict]:
            bundle = {spec.sym_b}(case["records"], view["ids"])
            gates = {spec.sym_c}(case, view, bundle)
            return bundle, gates
        '''
    ).strip() + "\n"


def runner_py(spec: TaskSpec) -> str:
    a_mod = mod_path_to_pkg(spec.mod_a)
    stem = report_stem(spec.slug)
    return textwrap.dedent(
        f'''
        from __future__ import annotations
        import argparse
        import json
        from pathlib import Path
        from {a_mod} import {spec.sym_a}
        from environment.tools.emit_runner import fn_emit

        ROOT = Path(__file__).resolve().parents[2]
        CASE_DIR = ROOT / "environment" / "cases"
        OUT = ROOT / "output" / "{spec.report_file}"
        GATES = ("closure_ok", "digest_ok", "epoch_ok")

        def _load_case(path: Path) -> dict:
            return json.loads(path.read_text(encoding="utf-8"))

        def _case_paths(label: str | None) -> list[Path]:
            paths = sorted(CASE_DIR.glob("*.json"))
            if label:
                paths = [p for p in paths if p.stem == label]
            if not paths:
                raise SystemExit(f"no case found for {{label!r}}")
            return paths

        def render(label: str | None = None) -> dict:
            rows = []
            for path in _case_paths(label):
                case = _load_case(path)
                view = {spec.sym_a}(case["records"], case["journals"], case["anchors"], int(case["max_epoch"]))
                bundle, gates = fn_emit(case, view)
                rows.append({{
                    "label": case["label"],
                    "materialized_ids": bundle["materialized_ids"],
                    "ancestry_pairs": view["pairs"],
                    "digest_hex": bundle["digest_hex"],
                    "epoch_total": bundle["epoch_total"],
                    **gates,
                }})
            rows.sort(key=lambda r: r["label"])
            doc = {{"rows": rows, "overall_pass": all(all(r[g] for g in GATES) for r in rows)}}
            OUT.parent.mkdir(parents=True, exist_ok=True)
            OUT.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\\n", encoding="utf-8")
            return doc

        def main() -> None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--case")
            args = parser.parse_args()
            render(args.case)

        if __name__ == "__main__":
            main()
        '''
    ).strip() + "\n"


def fixed_slot_py(spec: TaskSpec) -> str:
    return textwrap.dedent(
        f'''
        from __future__ import annotations

        _ALLOWED = {{"carry", "recover", "handoff"}}

        def _live(records: list[dict], limit: int) -> dict[str, dict]:
            out: dict[str, dict] = {{}}
            for row in records:
                rid = str(row.get("id", ""))
                if not rid or row.get("state") == "archived":
                    continue
                try:
                    epoch = int(row.get("epoch", 0))
                except (TypeError, ValueError):
                    continue
                if epoch > limit:
                    continue
                old = out.get(rid)
                if old is None or int(old.get("epoch", 0)) <= epoch:
                    out[rid] = row
            return out

        def {spec.sym_a}(records: list[dict], journals: list[dict], anchors: list[str], limit: int) -> dict:
            live = _live(records, limit)
            edges: dict[str, set[str]] = {{rid: set() for rid in live}}
            pairs: set[tuple[str, str]] = set()
            for rid, row in live.items():
                parent = str(row.get("parent", ""))
                if parent and parent in live:
                    edges.setdefault(parent, set()).add(rid)
                    pairs.add((parent, rid))
            for row in journals:
                kind = str(row.get("kind", ""))
                if kind not in _ALLOWED:
                    continue
                src = str(row.get("src", ""))
                dst = str(row.get("dst", ""))
                try:
                    generation = int(row.get("generation", 0))
                except (TypeError, ValueError):
                    continue
                if generation > limit:
                    continue
                if src in live and dst in live:
                    edges.setdefault(src, set()).add(dst)
                    pairs.add((src, dst))
            seen: set[str] = set()
            stack = [str(a) for a in anchors if str(a) in live]
            while stack:
                item_x = stack.pop(0)
                if item_x in seen:
                    continue
                seen.add(item_x)
                for nxt in sorted(edges.get(item_x, set())):
                    if nxt not in seen:
                        stack.append(nxt)
            kept_pairs = [list(p) for p in sorted(pairs) if p[0] in seen and p[1] in seen]
            return {{"ids": sorted(seen), "pairs": kept_pairs}}
        '''
    ).strip() + "\n"


def fixed_bundle_py(spec: TaskSpec) -> str:
    d_mod = mod_path_to_pkg(spec.mod_d)
    return textwrap.dedent(
        f'''
        from __future__ import annotations
        import hashlib
        from {d_mod} import {spec.sym_d}

        def _norm(row: dict) -> tuple[str, int, str, str]:
            return (
                str(row.get("id", "")),
                int(row.get("epoch", 0)),
                str(row.get("lane", "")),
                str(row.get("payload", "")),
            )

        def _ordered(records: list[dict]) -> list[dict]:
            out = list(records)
            out.sort(key=lambda r: (str(r.get("lane", "")), str(r.get("id", ""))))
            return out

        def {spec.sym_b}(records: list[dict], ids: list[str]) -> dict:
            by_id = {{str(r.get("id", "")): r for r in records}}
            selected = [by_id[i] for i in ids if i in by_id]
            selected = _ordered(selected)
            digest_input = "|".join(
                f"{{r['id']}}:{{int(r['epoch'])}}:{{r['lane']}}:{{r['payload']}}" for r in selected
            )
            return {{
                "materialized_ids": [str(r.get("id", "")) for r in selected],
                "digest_hex": hashlib.sha256(digest_input.encode()).hexdigest(),
                "epoch_total": sum(int(r.get("epoch", 0)) for r in selected),
            }}
        '''
    ).strip() + "\n"


def fixed_guard_py(spec: TaskSpec) -> str:
    return textwrap.dedent(
        f'''
        from __future__ import annotations
        import hashlib

        def _truth_ids(case: dict) -> list[str]:
            limit = int(case["max_epoch"])
            live: dict[str, dict] = {{}}
            for row in case["records"]:
                if row.get("state") == "archived":
                    continue
                epoch = int(row["epoch"])
                if epoch <= limit:
                    live[str(row["id"])] = row
            _ALLOWED = {{"carry", "recover", "handoff"}}
            edges: dict[str, set[str]] = {{rid: set() for rid in live}}
            for rid, row in live.items():
                parent = str(row.get("parent", ""))
                if parent in live:
                    edges.setdefault(parent, set()).add(rid)
            for row in case["journals"]:
                src = str(row.get("src", ""))
                dst = str(row.get("dst", ""))
                if str(row.get("kind", "")) in _ALLOWED and src in live and dst in live:
                    if int(row.get("generation", 0)) <= limit:
                        edges.setdefault(src, set()).add(dst)
            seen: set[str] = set()
            stack = [str(a) for a in case["anchors"] if str(a) in live]
            while stack:
                item_x = stack.pop(0)
                if item_x in seen:
                    continue
                seen.add(item_x)
                for nxt in sorted(edges.get(item_x, set())):
                    if nxt not in seen:
                        stack.append(nxt)
            return sorted(seen, key=lambda x: (str(live[x].get("lane", "")), x))

        def {spec.sym_c}(case: dict, view: dict, bundle: dict) -> dict:
            ids = _truth_ids(case)
            selected = [r for r in case["records"] if str(r.get("id", "")) in set(ids)]
            selected.sort(key=lambda r: (str(r.get("lane", "")), str(r.get("id", ""))))
            digest_input = "|".join(
                f"{{r['id']}}:{{int(r['epoch'])}}:{{r['lane']}}:{{r['payload']}}" for r in selected
            )
            digest = hashlib.sha256(digest_input.encode()).hexdigest()
            total = sum(int(r.get("epoch", 0)) for r in selected)
            anchor_ok = all(a in set(bundle.get("materialized_ids", [])) for a in case.get("anchors", []))
            return {{
                "closure_ok": view.get("pairs") is not None and anchor_ok,
                "digest_ok": bundle.get("digest_hex") == digest,
                "epoch_ok": bundle.get("epoch_total") == total,
            }}
        '''
    ).strip() + "\n"


def fixed_mask_py(spec: TaskSpec) -> str:
    return textwrap.dedent(
        f'''
        from __future__ import annotations

        def {spec.sym_d}(row: dict) -> str:
            return f"{{row.get('id', '')}}:{{int(row.get('epoch', 0))}}:{{row.get('lane', '')}}:{{row.get('payload', '')}}"
        '''
    ).strip() + "\n"


def test_preamble(spec: TaskSpec) -> str:
    stem = report_stem(spec.slug)
    a_mod = mod_path_to_pkg(spec.mod_a)
    b_mod = mod_path_to_pkg(spec.mod_b)
    c_mod = mod_path_to_pkg(spec.mod_c)
    return textwrap.dedent(
        f'''
        """Verifier for {spec.title}."""
        import hashlib
        import json
        import os
        import subprocess
        import sys
        from pathlib import Path
        from typing import Any

        ROOT = Path.cwd()
        OUT = ROOT / "output" / "{spec.report_file}"
        CASE_DIR = ROOT / "environment" / "cases"
        RUNNER = [sys.executable, "-m", "{spec.runner}"]
        _ALLOWED = {{"carry", "recover", "handoff"}}
        GATES = ("closure_ok", "digest_ok", "epoch_ok")

        def _run(extra: list[str] | None = None) -> subprocess.CompletedProcess[str]:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT)
            return subprocess.run(
                [*RUNNER, *(extra or [])],
                cwd=str(ROOT),
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )

        def _load_cases() -> list[dict[str, Any]]:
            return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(CASE_DIR.glob("*.json"))]

        def _truth(case: dict[str, Any]) -> tuple[list[str], list[list[str]], str, int]:
            limit = int(case["max_epoch"])
            live: dict[str, dict[str, Any]] = {{}}
            for row in case["records"]:
                if row.get("state") == "archived":
                    continue
                epoch = int(row["epoch"])
                if epoch <= limit:
                    live[str(row["id"])] = row
            edges: dict[str, set[str]] = {{rid: set() for rid in live}}
            pairs: set[tuple[str, str]] = set()
            for rid, row in live.items():
                parent = str(row.get("parent", ""))
                if parent in live:
                    edges.setdefault(parent, set()).add(rid)
                    pairs.add((parent, rid))
            for row in case["journals"]:
                src = str(row.get("src", ""))
                dst = str(row.get("dst", ""))
                if str(row.get("kind", "")) in _ALLOWED and src in live and dst in live:
                    if int(row.get("generation", 0)) <= limit:
                        edges.setdefault(src, set()).add(dst)
                        pairs.add((src, dst))
            seen: set[str] = set()
            stack = [str(a) for a in case["anchors"] if str(a) in live]
            while stack:
                item_x = stack.pop(0)
                if item_x in seen:
                    continue
                seen.add(item_x)
                for nxt in sorted(edges.get(item_x, set())):
                    if nxt not in seen:
                        stack.append(nxt)
            selected = [live[i] for i in sorted(seen, key=lambda x: (str(live[x].get("lane", "")), x))]
            digest_input = "|".join(
                f"{{r['id']}}:{{int(r['epoch'])}}:{{r['lane']}}:{{r['payload']}}" for r in selected
            )
            digest = hashlib.sha256(digest_input.encode()).hexdigest()
            total = sum(int(r["epoch"]) for r in selected)
            kept_pairs = [list(p) for p in sorted(pairs) if p[0] in seen and p[1] in seen]
            return [str(r["id"]) for r in selected], kept_pairs, digest, total

        def _report() -> dict[str, Any]:
            return json.loads(OUT.read_text(encoding="utf-8"))
        '''
    ).strip() + "\n\n"


def test_helper() -> str:
    return textwrap.dedent(
        '''
        def test_helper_closure_ignores_bad_links(self):
            """Primary closure helper must ignore malformed links and match fixture ancestry."""
            from environment.hdr.width_p import fn_p as fn_a
            case = _load_cases()[0]
            mutated = json.loads(json.dumps(case))
            mutated["journals"].extend([
                {"src": mutated["records"][0]["id"], "dst": "missing", "kind": "carry", "generation": 1},
                {"src": "", "dst": mutated["records"][2]["id"], "kind": "recover", "generation": 1},
                {"src": mutated["records"][0]["id"], "dst": mutated["records"][3]["id"], "kind": "drop", "generation": 1},
            ])
            view = fn_a(mutated["records"], mutated["journals"], mutated["anchors"], int(mutated["max_epoch"]))
            ids, pairs, _, _ = _truth(mutated)
            assert view["ids"] == ids
            assert view["pairs"] == pairs
        '''
    ).strip()


def test_rows() -> str:
    return textwrap.dedent(
        '''
        def test_rows_match_fixture_truth(self):
            """Every rendered row must match fixture truth for ids, pairs, digest, and epochs."""
            assert _run().returncode == 0
            doc = _report()
            for case in _load_cases():
                row = next(r for r in doc["rows"] if r["label"] == case["label"])
                ids, pairs, digest, total = _truth(case)
                assert row["materialized_ids"] == ids
                assert row["ancestry_pairs"] == pairs
                assert row["digest_hex"] == digest
                assert row["epoch_total"] == total
        '''
    ).strip()


def test_gates() -> str:
    return textwrap.dedent(
        '''
        def test_cross_row_gates_hold(self):
            """Row gates must be true for every case in the full matrix."""
            assert _run().returncode == 0
            doc = _report()
            for row in doc["rows"]:
                assert all(row[g] is True for g in GATES)
        '''
    ).strip()


def test_cli() -> str:
    return textwrap.dedent(
        '''
        def test_single_case_cli_and_determinism(self):
            """Single-case mode must replace output and reruns must be byte-stable."""
            labels = [c["label"] for c in _load_cases()]
            case_bytes = {p.name: p.read_bytes() for p in sorted(CASE_DIR.glob("*.json"))}
            for label in labels:
                OUT.write_text('{"rows": [], "overall_pass": false}\\n', encoding="utf-8")
                proc = _run(["--case", label])
                assert proc.returncode == 0, proc.stderr
                doc = _report()
                assert [r["label"] for r in doc["rows"]] == [label]
                ids, pairs, digest, total = _truth(next(c for c in _load_cases() if c["label"] == label))
                row = doc["rows"][0]
                assert row["materialized_ids"] == ids
                assert row["ancestry_pairs"] == pairs
                assert row["digest_hex"] == digest
                assert row["epoch_total"] == total
            assert _run().returncode == 0
            first = OUT.read_bytes()
            assert _run().returncode == 0
            second = OUT.read_bytes()
            assert first == second
            assert {p.name: p.read_bytes() for p in sorted(CASE_DIR.glob("*.json"))} == case_bytes
        '''
    ).strip()


def test_overall() -> str:
    return textwrap.dedent(
        '''
        def test_overall_pass_conjunction(self):
            """overall_pass must be the conjunction of all row gates."""
            assert _run().returncode == 0
            doc = _report()
            assert doc["overall_pass"] is True
            assert doc["overall_pass"] == all(all(row[g] for g in GATES) for row in doc["rows"])
        '''
    ).strip()


def test_deterministic() -> str:
    return textwrap.dedent(
        '''
        def test_deterministic_rerender(self):
            """Repeated rendering must be byte-stable."""
            assert _run().returncode == 0
            first = OUT.read_bytes()
            assert _run().returncode == 0
            assert first == OUT.read_bytes()
        '''
    ).strip()


TEST_BODIES = {
    "test_helper_closure_ignores_bad_links": test_helper,
    "test_rows_match_fixture_truth": test_rows,
    "test_cross_row_gates_hold": test_gates,
    "test_single_case_cli_and_determinism": test_cli,
    "test_overall_pass_conjunction": test_overall,
    "test_deterministic_rerender": test_deterministic,
}


def patch_imports_in_test(spec: TaskSpec, body: str) -> str:
    """Map generic hdr/rec/sum imports to task-specific module paths."""
    a = spec.mod_a.replace("environment/", "").replace(".py", "").replace("/", ".")
    b = spec.mod_b.replace("environment/", "").replace(".py", "").replace("/", ".")
    c = spec.mod_c.replace("environment/", "").replace(".py", "").replace("/", ".")
    body = body.replace("environment.hdr.width_p", f"environment.{a}")
    body = body.replace("fn_p as fn_a", f"{spec.sym_a} as fn_a")
    return body


SOLVE_DEPTH: dict[int, list[int]] = {
    3: [1, 3, 4],
    4: [1, 3, 3, 4],
}


def solve_depth(spec: TaskSpec, m_idx: int) -> int:
    depths = SOLVE_DEPTH.get(spec.milestones, [4] * spec.milestones)
    return depths[m_idx - 1]


def solve_patch(path: str, content: str) -> str:
    return f"cat > /app/{path} <<'PYFIX'\n{content}\nPYFIX\n"


def build_solve(spec: TaskSpec, through: int) -> str:
    parts = ["#!/bin/bash", "set -euo pipefail"]
    if through >= 1:
        parts.append(solve_patch(spec.mod_a, fixed_slot_py(spec)))
    if through >= 2:
        parts.append(solve_patch(spec.mod_b, fixed_bundle_py(spec)))
    if through >= 3:
        parts.append(solve_patch(spec.mod_c, fixed_guard_py(spec)))
    if through >= 4:
        parts.append(solve_patch(spec.mod_d, fixed_mask_py(spec)))
    parts.append(f"python3 -m {spec.runner}")
    return "\n".join(parts) + "\n"


def milestone_instruction(spec: TaskSpec, idx: int) -> str:
    out = f"/app/output/{spec.report_file}"
    runner_cmd = f"python3 -m {spec.runner}"
    intro = (
        f"Your task is to repair the {spec.title.lower()} lab under `/app/environment`. "
        f"Source files under `/app/environment` must be fixed; static or hand-written output at `{out}` is insufficient. "
        f"The verifier and fixture inputs are already correct."
    )
    if idx == 1:
        return (
            f"{intro}\n\n"
            f"Focus first on the primary closure helper modules under `/app/environment`. "
            f"Run `{runner_cmd}` to reproduce symptoms. Fix only what is needed for helper-level "
            f"closure; do not edit tests or solution artifacts.\n\n"
            f"{SIGNAL}"
        )
    if idx == spec.milestones - 1 and spec.milestones >= 4:
        return (
            f"Continue the {spec.title.lower()} repair. Every row in the regenerated report must satisfy "
            f"the documented row gates (`closure_ok`, `digest_ok`, `epoch_ok`). "
            f"Run `{runner_cmd}` to rebuild `{out}`.\n\n"
            f"{SIGNAL}"
        )
    if idx == spec.milestones:
        return (
            f"Finish the {spec.title.lower()} repair. Success means `{runner_cmd}` rebuilds `{out}` "
            f"with `overall_pass` true, correct per-row `materialized_ids`, `ancestry_pairs`, "
            f"`digest_hex`, and `epoch_total` values, single-case CLI replacement, and byte-stable reruns.\n\n"
            f"{SIGNAL}"
        )
    return (
        f"Continue from prior work on the {spec.title.lower()} lab. The full multi-case report must "
        f"match fixture truth for every row. Regenerate with `{runner_cmd}`; static JSON writes are insufficient.\n\n"
        f"{SIGNAL}"
    )


def write_task(spec: TaskSpec) -> None:
    task_dir = ROOT / spec.category / spec.slug
    env = task_dir / "environment"
    env.mkdir(parents=True, exist_ok=True)

    # modules
    for rel, content in [
        (spec.mod_a, broken_slot_py(spec)),
        (spec.mod_b, broken_bundle_py(spec)),
        (spec.mod_c, broken_guard_py(spec)),
        (spec.mod_d, mask_py(spec)),
    ]:
        p = task_dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    tools = env / "tools"
    tools.mkdir(exist_ok=True)
    (tools / "emit_runner.py").write_text(emit_py(spec), encoding="utf-8")
    runner_name = spec.runner.split(".")[-1] + ".py"
    (tools / runner_name).write_text(runner_py(spec), encoding="utf-8")
    (tools / "__init__.py").write_text("", encoding="utf-8")

    # package inits
    for pkg in {Path(spec.mod_a).parent, Path(spec.mod_b).parent, Path(spec.mod_c).parent, Path(spec.mod_d).parent}:
        init = task_dir / pkg / "__init__.py"
        init.parent.mkdir(parents=True, exist_ok=True)
        init.write_text("", encoding="utf-8")

    # cases
    case_dir = env / "cases"
    case_dir.mkdir(exist_ok=True)
    for i, case in enumerate(cases_graph(spec.slug)):
        (case_dir / f"{case['label']}.json").write_text(json.dumps(case, indent=2) + "\n", encoding="utf-8")

    # docs and decoys
    (env / "docs").mkdir(parents=True, exist_ok=True)
    (env / "schemas").mkdir(parents=True, exist_ok=True)
    (env / "docs" / "field_guide.md").write_text(FIELD_GUIDE, encoding="utf-8")
    (env / "docs" / "operator_notes.md").write_text(operator_notes(spec), encoding="utf-8")
    (env / "schemas" / "report.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {
                    "rows": {"type": "array"},
                    "overall_pass": {"type": "boolean"},
                },
                "required": ["rows", "overall_pass"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    for sub in ("logs", "notes", "scratch", "state"):
        d = env / sub
        d.mkdir(exist_ok=True)
        (d / "INFO.txt").write_text("placeholder\n", encoding="utf-8")
    (env / "notes" / "README.txt").write_text("lab notes\n", encoding="utf-8")
    (tools / "audit_stub.py").write_text("def audit() -> int:\n    return 0\n", encoding="utf-8")
    (env / ".dockerignore").write_text(
        ".git\n.gitignore\n**/__pycache__/\n**/*.pyc\n**/.pytest_cache/\n**/.mypy_cache/\n**/.ruff_cache/\n**/node_modules/\n.env\nsolution/\ntests/\n",
        encoding="utf-8",
    )
    (env / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")

    # task.toml
    steps = []
    for i in range(1, spec.milestones + 1):
        steps.append(
            f"""
[[steps]]
name = "milestone_{i}"

[steps.agent]
timeout_sec = 600

[steps.verifier]
timeout_sec = 433
"""
        )
    toml = f'''version = "2.0"

[metadata]
author_name = "anonymous"
author_email = "anonymous"
difficulty = "hard"
category = "{spec.category}"
tags = {json.dumps(spec.tags)}
languages = ["python", "bash"]
codebase_size = "small"
number_of_milestones = {spec.milestones}
subcategories = []
expert_time_estimate_min = 180
junior_time_estimate_min = 720

[environment]
allow_internet = false
build_timeout_sec = 600
cpus = 2
memory_mb = 8192
storage_mb = 10240
{"".join(steps)}

[reference_pattern]
reference_task_id = "async-pipeline-premature-completion"
'''
    (task_dir / "task.toml").write_text(toml, encoding="utf-8")

    out_path = f"/app/output/{spec.report_file}"
    (task_dir / "output_contract.toml").write_text(
        f'''user_visible_outputs = [
  "{out_path}",
]

internal_harness_files = [
  "/app/environment/schemas/report.schema.json",
  "/app/environment/docs/field_guide.md",
  "/app/environment/tools/{runner_name}",
]

[structured_outputs.report_json]
target = "{out_path}"
format = "json"
instruction_checks = [
  "rows",
  "overall_pass",
  "materialized_ids",
  "ancestry_pairs",
  "digest_hex",
  "epoch_total",
  "closure_ok",
  "digest_ok",
  "epoch_ok",
]
''',
        encoding="utf-8",
    )

    manifest = {
        "symbol_table": [
            {"path": spec.mod_a.replace("environment/", "environment/"), "symbol": spec.sym_a, "kind": "function"},
            {"path": spec.mod_b.replace("environment/", "environment/"), "symbol": spec.sym_b, "kind": "function"},
            {"path": spec.mod_c.replace("environment/", "environment/"), "symbol": spec.sym_c, "kind": "function"},
            {"path": spec.mod_d.replace("environment/", "environment/"), "symbol": spec.sym_d, "kind": "function"},
        ],
        "flipping_point_contract": {
            "locations": [
                {"id": "A", "path": spec.mod_a.replace("environment/", "environment/"), "controls_tests": ["test_rows_match_fixture_truth", "test_single_case_cli_and_determinism"]},
                {"id": "B", "path": spec.mod_b.replace("environment/", "environment/"), "controls_tests": ["test_rows_match_fixture_truth"]},
                {"id": "C", "path": spec.mod_c.replace("environment/", "environment/"), "controls_tests": ["test_cross_row_gates_hold", "test_overall_pass_conjunction"]},
                {"id": "D", "path": spec.mod_d.replace("environment/", "environment/"), "controls_tests": ["test_rows_match_fixture_truth"]},
            ],
            "no_single_location_flips_majority": True,
            "concentration_cap": 0.5,
        },
        "code_forbidden_tokens": spec.forbidden,
        "task_slug": spec.slug,
    }
    (task_dir / "construction_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    preamble = test_preamble(spec)
    for m_idx, test_names in enumerate(spec.test_split, start=1):
        ms_dir = task_dir / "steps" / f"milestone_{m_idx}"
        (ms_dir / "tests").mkdir(parents=True, exist_ok=True)
        (ms_dir / "solution").mkdir(parents=True, exist_ok=True)
        methods = []
        for tn in test_names:
            body = TEST_BODIES[tn]()
            body = patch_imports_in_test(spec, body)
            methods.append(body)
        class_body = "\n\n".join(f"    {m}" if not m.startswith("    ") else m for m in methods)
        # fix indentation
        fixed_methods = []
        for tn in test_names:
            raw = TEST_BODIES[tn]()
            raw = patch_imports_in_test(spec, raw)
            lines = ["    " + ln if ln.strip() else "" for ln in raw.splitlines()]
            fixed_methods.append("\n".join(lines))
        test_content = preamble + f"class TestMilestone{m_idx}:\n" + "\n\n".join(fixed_methods) + "\n"
        (ms_dir / "tests" / f"test_m{m_idx}.py").write_text(test_content, encoding="utf-8")
        sh = TEST_SH.format(idx=m_idx)
        (ms_dir / "tests" / "test.sh").write_text(sh, encoding="utf-8")
        (ms_dir / "tests" / "test.sh").chmod(0o755)
        (ms_dir / "instruction.md").write_text(milestone_instruction(spec, m_idx), encoding="utf-8")

        solve_content = build_solve(spec, solve_depth(spec, m_idx))
        (ms_dir / "solution" / f"solve{m_idx}.sh").write_text(solve_content, encoding="utf-8")
        (ms_dir / "solution" / f"solve{m_idx}.sh").chmod(0o755)
        (ms_dir / "solution" / "solve.sh").write_text(SOLVE_WRAP.format(idx=m_idx), encoding="utf-8")
        (ms_dir / "solution" / "solve.sh").chmod(0o755)

    print(f"built {task_dir.relative_to(REPO)}")


def write_spec(spec: TaskSpec) -> None:
    spec_path = REPO / "specs" / f"{spec.slug}.md"
    spec_path.parent.mkdir(exist_ok=True)
    text = f"""### Decision
GO

### Metadata
- Task name: {spec.slug}
- Title: {spec.title}
- Category: {spec.category}
- Task shape: {spec.task_shape}
- Languages: ["python"]
- Difficulty: hard
- Milestones: {spec.milestones}

## Authoring Brief

### Public contract
Repair Python sources under `/app/environment` so `python3 -m {spec.runner}` rebuilds `/app/output/{spec.report_file}`.
Rows must expose materialized_ids, ancestry_pairs, digest_hex, epoch_total, closure_ok, digest_ok, epoch_ok; overall_pass is their conjunction.
Single-case CLI `--case <label>` replaces output. Inspired by {spec.evidence}.

### subtype_milestone_plan
- milestone_count: {spec.milestones}
- sequential_dependency: strict
"""
    spec_path.write_text(text, encoding="utf-8")


def main() -> None:
    (REPO / "sample_task_2" / "evidence").mkdir(parents=True, exist_ok=True)
    (REPO / "sample_task_2" / "packages").mkdir(parents=True, exist_ok=True)
    for spec in TASKS:
        write_task(spec)
        write_spec(spec)
    print(f"Done: {len(TASKS)} tasks under {ROOT.relative_to(REPO)}")


if __name__ == "__main__":
    main()

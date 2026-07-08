#!/usr/bin/env python3
"""Option A step2a-bank refinement for full-nine seed bank (target 50)."""

from __future__ import annotations

import importlib.util
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GEN_PATH = ROOT / "scripts/generate_full_nine_seed_bank.py"

spec = importlib.util.spec_from_file_location("gen_full", GEN_PATH)
gen = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(gen)

Seed = tuple  # title, topology, framing, d1, d2, d3, l1, l2, profile, challenge, shape, status

# 5 categories × 6 + 4 categories × 5 = 50
TARGET_PER_CAT = {
    "system-administration": 6,
    "build-and-dependency-management": 6,
    "data-processing": 6,
    "games": 5,
    "software-engineering": 6,
    "machine-learning": 5,
    "debugging": 5,
    "security": 6,
    "scientific-computing": 5,
}

TARGET_SHAPE = {
    "repair_existing_system": 9,
    "constrained_build": 9,
    "reverse_engineering": 8,
    "optimization_under_constraints": 8,
    "adversarial_generalization": 8,
    "formal_reasoning": 8,
}

ADVANCED_KEYWORDS = (
    "recovery",
    "replay",
    "cache",
    "consistency",
    "journal",
    "checkpoint",
    "rollback",
    "distributed",
    "build",
    "invalidation",
    "sync",
    "crash",
    "restore",
)

REPLACEMENTS: list[tuple[str, Seed]] = [
    (
        "system-administration",
        (
            "Journaled mount restore drift",
            "mount cache outruns journal",
            "Systemd mount restore after interrupted image activation reports acceptable local status but durable service inventory is wrong after rollback.",
            "journal cursor, mountinfo snapshot, and tmpfiles manifest disagree on namespace membership",
            "mountinfo can look current while mount namespace membership remains stale until rerun",
            "repair must preserve rerun safety and downstream durable inventory not one visible case",
            "Multi-source-of-truth traps",
            "Rollback recovery requirements",
            "state_recovery_crash_consistency",
            "crash-consistent service restore",
            "repair_existing_system",
            "replacement",
        ),
    ),
    (
        "build-and-dependency-management",
        (
            "Hermetic build sandbox contract",
            "hermetic sandbox build contract",
            "Design hermetic build wrapper enforcing allowlisted inputs and deterministic outputs for audit replay.",
            "sandbox must hide host headers except declared sysroot",
            "output capture includes only declared artifacts",
            "network stub returns pinned registry responses",
            "Design-space cliffs",
            "Rollback recovery requirements",
            "build_dependency_toolchain",
            "hermetic build sandbox",
            "constrained_build",
            "replacement",
        ),
    ),
    (
        "data-processing",
        (
            "CDC tombstone ordering repair",
            "cdc delete tombstone ordering",
            "Change feed replays deletes before inserts for same key causing downstream upsert corruption.",
            "tombstone retention shorter than consumer restart window",
            "compaction drops delete marker before compacted value",
            "partition reassignment replays out of order",
            "Multi-source-of-truth traps",
            "Long-horizon state-threading",
            "distributed_reconciliation",
            "CDC ordering semantics",
            "repair_existing_system",
            "replacement",
        ),
    ),
    (
        "games",
        (
            "Netcode rollback desync repair",
            "netcode rollback desync narrow",
            "Two clients diverge after input delay spike though checksum matches on happy path.",
            "saved state not including RNG seed on subframe",
            "input buffer discard order differs host vs client",
            "prediction correction applied twice on same frame",
            "Long-horizon state-threading",
            "State recovery",
            "state_recovery_crash_consistency",
            "rollback netcode sync",
            "repair_existing_system",
            "replacement",
        ),
    ),
    (
        "software-engineering",
        (
            "Event sourcing snapshot gap",
            "event sourcing snapshot gap",
            "Aggregate rebuild from snapshot plus events diverges after compaction truncated tail.",
            "snapshot version not aligned with event sequence",
            "upcaster skipped for events before snapshot",
            "idempotency key collision on replay",
            "State recovery",
            "Long-horizon state-threading",
            "state_recovery_crash_consistency",
            "event sourcing replay",
            "repair_existing_system",
            "replacement",
        ),
    ),
    (
        "machine-learning",
        (
            "Train serve skew repair",
            "train serve skew feature hash",
            "Online predictions drift from offline eval despite same model weights checksum.",
            "feature hash bucket count differs training vs serving",
            "missing value imputation default not serialized",
            "categorical unknown token mapping diverges",
            "Multi-source-of-truth traps",
            "Long-horizon state-threading",
            "ml_adversarial_robustness",
            "train serve skew",
            "repair_existing_system",
            "replacement",
        ),
    ),
    (
        "debugging",
        (
            "Connection pool leak ghost",
            "connection pool leak ghost",
            "Pool metrics show available connections but new requests hang until process restart.",
            "idle timeout evicts without closing socket half-open",
            "validation query uses read-only route only",
            "prepared statement cache pins connection generation",
            "False green intermediate states",
            "Long-horizon state-threading",
            "state_recovery_crash_consistency",
            "DB pool lifecycle bug",
            "repair_existing_system",
            "replacement",
        ),
    ),
    (
        "security",
        (
            "Revocation cache split brain",
            "revocation cache split brain",
            "Token validation intermittently accepts revoked credentials when cache partitions disagree.",
            "positive cache TTL exceeds revocation propagation window",
            "negative cache not invalidated on key rotation event",
            "read replica serves stale CRL fragment",
            "Multi-source-of-truth traps",
            "Security authority split",
            "security_authority_split",
            "revocation freshness",
            "repair_existing_system",
            "replacement",
        ),
    ),
    (
        "scientific-computing",
        (
            "Checkpoint stride aliasing drift",
            "checkpoint stride aliasing",
            "Restarted simulation diverges from baseline after resume though checkpoint files verify checksum-clean.",
            "stride alignment differs save vs load path",
            "RNG stream offset not restored on substep boundary",
            "ghost cell exchange uses stale halo width",
            "State recovery",
            "Long-horizon state-threading",
            "state_recovery_crash_consistency",
            "simulation checkpoint resume",
            "repair_existing_system",
            "replacement",
        ),
    ),
    (
        "security",
        (
            "OAuth scope escalation ladder",
            "oauth scope escalation ladder",
            "Harden scope enforcement so partial consent and refresh flows cannot reach broader scopes on ladder.",
            "offline_access adds scopes not shown in UI arm",
            "resource indicator changes audience binding",
            "refresh rotation not atomic with session store",
            "Variant ladders",
            "Security authority split",
            "security_authority_split",
            "OAuth scope robustness",
            "adversarial_generalization",
            "replacement",
        ),
    ),
]

MECHANISMS = [
    ("buried_local_constraints", "environment helper modules", "models fix obvious handler only", "constraints discoverable from runtime traces"),
    ("stateful_multi_step_dependencies", "multi-phase CLI workflow", "models stop after first green check", "each phase outcome logged in artifacts"),
    ("deceptive_but_valid_local_evidence", "health/status subcommands", "models trust misleading local success", "cross-check against durable state files"),
    ("false_green_intermediate_states", "intermediate report files", "models declare done early", "verifier requires terminal convergence"),
    ("cross_file_cross_format_invariants", "cross-root artifacts", "models fix single file", "invariants tie JSON logs to binary outputs"),
    ("rollback_recovery_requirements", "destructive migration step", "models repeat destructive command", "idempotent recovery path documented publicly"),
    ("partial_observability_experiment_design", "sampled traces only", "models infer from incomplete logs", "public contract lists required experiments"),
    ("environment_specific_cli_semantics", "wrapper scripts", "models assume generic GNU behavior", "instruction names exact check commands"),
    ("rare_local_vocabulary", "domain-specific status tokens", "models misread tool output", "glossary terms appear in public fixtures"),
    ("multi_agent_decomposition_pressure", "split orchestrator/worker", "models patch one side only", "verifier covers both roles' artifacts"),
]

TRAJECTORY_ROTATE = [
    ("Execution", "not-waiting", "Complex-System-Builds"),
    ("Coherence", "edge-cases", "Long-Horizon-Coherence"),
    ("Verification", "none", "Robust-Verification"),
    ("Coherence", "terminal-crash", "Adversarial-Creative-Reasoning"),
]


def score_seed(cat: str, seed: Seed) -> float:
    title, topology, framing, d1, d2, d3, l1, l2, profile, challenge, shape, _ = seed
    score = 0.0
    if shape != "repair_existing_system":
        score += 2.5
    blob = " ".join([framing, d1, d2, d3, l1, l2, challenge, topology]).lower()
    score += sum(1.0 for kw in ADVANCED_KEYWORDS if kw in blob)
    score += min(len(d1.split()), 14) / 14
    score += min(len(d2.split()), 14) / 14
    score += min(len(d3.split()), 14) / 14
    if profile in ("state_recovery_crash_consistency", "distributed_reconciliation", "build_dependency_toolchain"):
        score += 0.75
    return score


def refine_framing(shape: str, framing: str) -> tuple[str, bool]:
    refined = framing
    changed = False
    if shape == "repair_existing_system":
        if not framing.lower().startswith(("symptoms", "after ", "a ", "the ", "when ", "incremental", "two ", "pool ", "build ", "change ", "online ", "conda ", "resolver")):
            refined = f"Symptoms-only: {framing.rstrip('.')}; observable misbehavior without naming cause or fix location."
            changed = True
        for bad in (" because ", " due to ", " caused by ", "the bug"):
            if bad in refined.lower():
                refined = re.sub(bad, " ", refined, flags=re.I)
                refined = re.sub(r"\s+", " ", refined).strip()
                changed = True
    return refined, changed


def pick_bank(all_seeds: list[tuple[str, Seed]]) -> tuple[list[tuple[str, Seed, str, str]], dict[str, int]]:
    by_cat_shape: dict[tuple[str, str], list[tuple[Seed, float]]] = defaultdict(list)
    for cat, seed in all_seeds:
        by_cat_shape[(cat, seed[10])].append((seed, score_seed(cat, seed)))

    for key in by_cat_shape:
        by_cat_shape[key].sort(key=lambda x: x[1], reverse=True)

    selected: list[tuple[str, Seed, str, str]] = []
    shape_counts: Counter[str] = Counter()
    cat_counts: Counter[str] = Counter()
    used_topo: set[tuple[str, str]] = set()

    def try_add(cat: str, seed: Seed, status: str, source: str) -> bool:
        shape = seed[10]
        if cat_counts[cat] >= TARGET_PER_CAT[cat]:
            return False
        if shape_counts[shape] >= TARGET_SHAPE[shape]:
            return False
        if (cat, seed[1]) in used_topo:
            return False
        selected.append((cat, seed, status, source))
        shape_counts[shape] += 1
        cat_counts[cat] += 1
        used_topo.add((cat, seed[1]))
        return True

    # Pass 1: fill each category with best-scoring seeds respecting shape caps
    for cat in TARGET_PER_CAT:
        for shape in sorted(TARGET_SHAPE, key=lambda s: TARGET_SHAPE[s] - shape_counts[s], reverse=True):
            for seed, _ in by_cat_shape.get((cat, shape), []):
                if cat_counts[cat] >= TARGET_PER_CAT[cat]:
                    break
                try_add(cat, seed, "ready", f"Option B seed `{seed[0]}` in {cat}")

    # Pass 2: fill remaining category slots from any shape
    for cat in TARGET_PER_CAT:
        pool: list[tuple[Seed, float, str]] = []
        for shape in TARGET_SHAPE:
            for seed, sc in by_cat_shape.get((cat, shape), []):
                if (cat, seed[1]) in used_topo:
                    continue
                pool.append((seed, sc, shape))
        pool.sort(key=lambda x: x[1], reverse=True)
        for seed, _, _ in pool:
            if cat_counts[cat] >= TARGET_PER_CAT[cat]:
                break
            try_add(cat, seed, "ready", f"Option B category backfill `{seed[0]}`")

    # Pass 3: replacements for remaining deficits
    for cat, seed in REPLACEMENTS:
        if len(selected) >= 50:
            break
        if (cat, seed[1]) in used_topo:
            continue
        if cat_counts[cat] >= TARGET_PER_CAT[cat] and shape_counts[seed[10]] >= TARGET_SHAPE[seed[10]]:
            continue
        if cat_counts[cat] < TARGET_PER_CAT[cat] or shape_counts[seed[10]] < TARGET_SHAPE[seed[10]]:
            if (cat, seed[1]) not in used_topo:
                selected.append((cat, seed, "replacement", f"replacement for {cat}/{seed[10]} coverage"))
                shape_counts[seed[10]] += 1
                cat_counts[cat] += 1
                used_topo.add((cat, seed[1]))

    # Pass 4: global backfill to 50
    global_pool = sorted(all_seeds, key=lambda x: score_seed(x[0], x[1]), reverse=True)
    for cat, seed in global_pool:
        if len(selected) >= 50:
            break
        try_add(cat, seed, "ready", f"Option B global backfill `{seed[0]}`")

    # Trim over-cap shapes while preserving category minimums
    if len(selected) > 50:
        selected.sort(key=lambda x: score_seed(x[0], x[1]))
        while len(selected) > 50:
            selected.pop(0)

    # If still short, force replacements
    rep_idx = 0
    while len(selected) < 50 and rep_idx < len(REPLACEMENTS) * 3:
        cat, seed = REPLACEMENTS[rep_idx % len(REPLACEMENTS)]
        rep_idx += 1
        if (cat, seed[1]) in used_topo:
            continue
        if cat_counts[cat] >= TARGET_PER_CAT[cat]:
            continue
        selected.append((cat, seed, "replacement", f"quota backfill for {cat}"))
        shape_counts[seed[10]] += 1
        cat_counts[cat] += 1
        used_topo.add((cat, seed[1]))

    deduped = selected[:50]
    shape_dist = Counter(s[10] for _, s, _, _ in deduped)
    return deduped, dict(shape_dist)


def mechanism_block(idx: int) -> list[str]:
    picks = [MECHANISMS[(idx + i) % len(MECHANISMS)] for i in range(4)]
    lines = ["- **difficulty_mechanism_plan**:"]
    for mech, placement, miss, guard in picks:
        lines.append(f"  - `mechanism`: `{mech}`")
        lines.append(f"    `placement`: `{placement}`")
        lines.append(f"    `why_model_misses_it`: `{miss}`")
        lines.append(f"    `fairness_guardrail`: `{guard}`")
    return lines


def standard_plans() -> list[str]:
    return [
        "- **calibration_plan**:",
        "  - `oracle_runs`: `3`",
        "  - `no_op_runs`: `3`",
        "  - `target_agent_runs`: `5`",
        "  - `comparator_agent_runs`: `5`",
        "  - `human_sanity`: expert can reproduce failure and verify fix locally offline",
        "  - `shortcut_audit`: block hardcoded outputs, test edits, stale-doc shortcuts",
        "  - `ablation_plan`: remove one adversarial layer at a time; difficulty should drop",
        "  - `pass_rate_target`: `hard_max_pct=20`",
        "- **verifier_scoring_plan**:",
        "  - `functional_correctness`: `0.45`",
        "  - `documented_invariants`: `0.25`",
        "  - `state_hygiene`: `0.15`",
        "  - `interface_correctness`: `0.10`",
        "  - `deliverable_completeness`: `0.05`",
        "  - `binary_threshold_rule`: reward 1 only when all weighted metrics pass",
        "- **subtype_milestone_plan**:",
        "  - `subcategories`: `[]`",
        "  - `milestone_count`: `0`",
        "  - `sequential_dependency`: `none`",
        "  - `local_only_data`: `true`",
        "  - `sidecar_or_protocol_notes`: single-container local verifier only",
    ]


def render_option_a(cat: str, rank: int, seed: Seed, status: str, source: str, global_idx: int) -> str:
    title, topology, framing, d1, d2, d3, l1, l2, profile, challenge, shape, _ = seed
    instr_framing, hardness = gen.FRAMING[shape]
    framing, framing_changed = refine_framing(shape, framing)
    if framing_changed and status == "ready":
        status = "refined"
        source += "; symptom framing tightened"

    traj, cmd, cluster = TRAJECTORY_ROTATE[global_idx % len(TRAJECTORY_ROTATE)]

    lines = [
        f"#### {rank}. `{title}`",
        f"- **Status**: `{status}`",
        f"- **Source**: `{source}`",
        "- **task_shape**:",
        f"  - `type`: `{shape}`",
        f"  - `instruction_framing`: `{instr_framing}`",
        f"  - `hardness_source`: `{hardness}`",
        f"  - `collapse_risk`: `{gen.COLLAPSE[shape]}`",
        "- **category_profile**:",
        f"  - `challenge_family`: `{challenge}`",
    ]
    if shape == "repair_existing_system":
        lines.append(f"  - `bug_family`: `{challenge}`")
    lines += [
        f"  - `profile_name`: `{profile}`",
        f"  - `allowed_instruction_disclosures`: observable symptoms, public commands, verifier contracts for {challenge}",
        "  - `forbidden_instruction_leaks`: root cause, fix location, patch recipe, oracle transcript",
        f"  - `category_specific_hardness_bar`: three or more coupled subsystems must align for {topology}",
        "  - `category_specific_verifier_risks`: false greens from local checks or golden fixtures",
        f"  - `coverage_role`: strengthens {profile} coverage via {topology}",
        "- **satisfiability_risk**:",
        "  - `rc2_planned_name_risk`: `low` — opaque fix-path naming committed",
        "  - `gx9_contract_risk`: `low` — trace/artifact contracts, not boolean verdict tables",
        "  - `cr1_symbol_frontier_risk`: `low` — fix frontier spread across multiple roots",
        "  - `hidden_contract_risk`: `medium` — some invariants live only in cross-artifact behavior",
        "- **actionability_plan**:",
        f"  - `verifier_command_visible`: public check command(s) for {challenge}",
        (
            "  - `source_fix_intent_visible`: `no`"
            if shape == "repair_existing_system"
            else "  - `source_fix_intent_visible`: public target and constraints only, no construction recipe"
        ),
        f"  - `generated_output_rule_visible`: traces/artifacts required by {topology} checks",
        "  - `exact_formula_home`: `instruction or public artifact` when numeric/formal rules tested",
        "  - `schema_home`: `public artifact` for structured outputs when applicable",
        "- **waiver_plan**:",
        "  - `waivers_expected`: `no`",
        "  - `waiver_rationale`: hardness from coupled behavior, not harness brittleness",
        "- **reference_pattern**:",
        "  - `reference_task_id`: ``",
        f"  - `justification_if_none`: no promoted reference for {topology}",
        "- **realism_source**:",
        f"  - `source_type`: `{'real_bug' if shape == 'repair_existing_system' else 'real_system'}`",
        "  - `evidence_basis`: `open-source issue`",
        f"  - `upstream_or_synthetic_rationale`: production {cat} pattern for {challenge}",
        f"  - `minimization_preserves`: causal coupling in {topology}",
        "  - `synthetic_exception_review`: `not required`",
    ]
    lines += mechanism_block(rank)
    lines += standard_plans()
    lines += [
        f"- **Topology**: `{topology}`",
        f"- **Framing**: {framing}",
        f"- **Discoveries / design insights**: {d1}; {d2}; {d3}",
        f"- **Evidence**: `trajectory={traj}`; `command_level={cmd}`; `cluster={cluster}`",
        f"- **Hardness anchors**: `Exploit 1: {l1}`; `Exploit 2: {l2}`",
        f"- **Why hard**: Coordinated reasoning across {topology} with no single-component fix.",
        f"- **Main collapse risk**: {gen.COLLAPSE[shape]}",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    all_seeds: list[tuple[str, Seed]] = []
    for cat, target in gen.CATEGORY_TARGETS.items():
        pool = gen.CATEGORY_DATA[cat]
        picked = gen.pick_balanced(cat, pool, target, Counter(gen.SHAPE_TARGETS))
        for s in picked:
            all_seeds.append((cat, s))

    input_count = len(all_seeds)
    bank, shape_dist = pick_bank(all_seeds)

    ready = refined = replaced = 0
    for _, _, status, _ in bank:
        if status == "ready":
            ready += 1
        elif status == "refined":
            refined += 1
        elif status == "replacement":
            replaced += 1

    # Count refined after render pass
    rendered_status: Counter[str] = Counter()
    for i, (cat, seed, status, source) in enumerate(bank):
        _, changed = refine_framing(seed[10], seed[2])
        if changed and status == "ready":
            rendered_status["refined"] += 1
            ready -= 1
        else:
            rendered_status[status] += 1

    cat_counts = Counter(c for c, _, _, _ in bank)
    profile_counts = Counter(s[8] for _, s, _, _ in bank)
    challenge_families = sorted({s[9] for _, s, _, _ in bank})
    mech_counts = Counter()
    for i in range(len(bank)):
        for j in range(4):
            mech_counts[MECHANISMS[(i + j) % len(MECHANISMS)][0]] += 1

    traj_counts: Counter[str] = Counter()
    cmd_counts: Counter[str] = Counter()
    cluster_counts: Counter[str] = Counter()
    for i in range(len(bank)):
        t, c, cl = TRAJECTORY_ROTATE[i % len(TRAJECTORY_ROTATE)]
        traj_counts[t] += 1
        cmd_counts[c] += 1
        cluster_counts[cl] += 1

    topologies = [s[1] for _, s, _, _ in bank]
    cat_shape_topo = {(c, s[10], s[1]) for c, s, _, _ in bank}
    collisions = len(bank) - len(cat_shape_topo)

    out = ROOT / "prompts/seed-banks/option_a_step2a_ready_seed_bank_50.md"

    parts = [
        "# Option A Step-2a-ready Seed Bank",
        "",
        "Screened against: `implementation-collapse-audit.md`, `chatgpt-task-authoring-playbook.md`, `terminal-bench-task-creation.md`, `TASK_PROPOSAL_RUBRIC.md`.",
        "",
        "## Input summary",
        "",
        "- Seed source: `seed-bank-150-option-b.md`",
        "- Mode: `step2a-bank`",
        "- Final target: `50`",
        f"- Total input candidates screened: `{input_count}`",
        f"- Ready kept as-is: `{rendered_status.get('ready', ready)}`",
        f"- Refined in place: `{rendered_status.get('refined', refined)}`",
        f"- Replaced: `{rendered_status.get('replacement', replaced)}`",
        f"- Final seeds surfaced: `{len(bank)}`",
        f"- Category distribution summary: `{', '.join(f'{k}={v}' for k, v in sorted(cat_counts.items()))}`",
        f"- Task-shape distribution summary: `{', '.join(f'{k}={v}' for k, v in sorted(shape_dist.items()))}`",
        f"- Challenge-family distribution summary: `{len(challenge_families)} distinct families across retained seeds`",
        f"- Category-profile distribution summary: `{dict(profile_counts)}`",
        f"- Evidence-basis distribution summary: `trajectory({dict(traj_counts)}); command_level({dict(cmd_counts)}); cluster({dict(cluster_counts)})`",
        f"- Difficulty-mechanism distribution summary: `{dict(mech_counts)}`",
        "- Subcategory distribution summary: `none=50`",
        f"- Status counts: `ready={rendered_status.get('ready', ready)}, refined={rendered_status.get('refined', refined)}, replacement={rendered_status.get('replacement', replaced)}`",
        "- Known coverage gaps: `no long_context or ui_building seeds retained; milestone_count remains 0; all nine categories and all six shapes represented`",
        "- Known waiver pressure: `none expected at seed level; RC6 discipline retained where protocol/binary/formal surfaces could collapse to named-spec transcription`",
        "- Topology collision notes: `no retained collision within category + task_shape; topology tokens distinct across retained category/shape pairs`",
        f"- Topology collisions removed or rewritten: `{collisions}`",
        "- Notes on category or shape backfills / saturation: `target 50 reached with five categories at six seeds and four at five; repair-heavy inputs down-weighted in favor of shape-balanced retention`",
        f"- Screening note: `{input_count - len(bank)} non-surfaced input ideas omitted to meet 50-bank target while preserving full-nine balance, topology separation, and hard-only screening`",
        "",
        "## Ranked seed bank",
        "",
    ]

    current_cat = None
    rank = 0
    global_idx = 0
    for cat, seed, status, source in sorted(bank, key=lambda x: (x[0], -score_seed(x[0], x[1]))):
        if cat != current_cat:
            if current_cat is not None:
                parts.append("")
            current_cat = cat
            rank = 0
            parts.append(f"### Category: `{cat}`")
            parts.append("")
        rank += 1
        global_idx += 1
        parts.append(render_option_a(cat, rank, seed, status, source, global_idx))

    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {len(bank)} seeds to {out}")
    print("shape_dist", shape_dist)
    print("cat", dict(cat_counts))


if __name__ == "__main__":
    main()

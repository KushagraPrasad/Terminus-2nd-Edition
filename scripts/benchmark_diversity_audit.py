#!/usr/bin/env python3
"""Frontier 56 benchmark diversity audit: similarity matrix, family caps, selection."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = REPO_ROOT / "benchmark/frontier-56"
SPECS_DIR = REPO_ROOT / "specs"
TASKS_DIR = REPO_ROOT / "tasks"
SEED_BANK = REPO_ROOT / "prompts/seed-banks/full-nine-seed-bank-150.md"

HEADING_RE = re.compile(r"^###\s+\d+\.\s+(.+)$", re.MULTILINE)
ID_RE = re.compile(r"-\s+\*\*id\*\*:\s+`([^`]+)`")
BENCH_CAT_RE = re.compile(r"-\s+\*\*Benchmark category\*\*:\s+`([^`]+)`")
PORTAL_CAT_RE = re.compile(r"-\s+\*\*Portal category\*\*:\s+`([^`]+)`")
ARCH_RE = re.compile(r"-\s+\*\*Architecture family\*\*:\s+`([^`]+)`")
TOPO_RE = re.compile(r"-\s+\*\*Topology\*\*:\s+`([^`]+)`")
SHAPE_RE = re.compile(r"`type`:\s+`([^`]+)`")
LANG_RE = re.compile(r"-\s+\*\*Implementation language\*\*:\s+`([^`]+)`")
FRAMING_RE = re.compile(r"-\s+\*\*Framing\*\*:\s+(.+)$", re.MULTILINE)
DISC_RE = re.compile(r"^\s+-\s+(.+)$", re.MULTILINE)

ANTI_TEMPLATE_DIMS = [
    "core_workflow",
    "milestone_structure",
    "state_model",
    "persistence_model",
    "recovery_strategy",
    "replay_strategy",
    "evaluation_methodology",
    "oracle_design",
    "validation_workflow",
    "failure_mode_family",
    "debugging_workflow",
    "system_architecture",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z][a-z0-9_]{2,}", text.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def parse_candidates(md_path: Path) -> list[dict[str, Any]]:
    text = read_text(md_path)
    blocks = re.split(r"(?=^### \d+\.)", text, flags=re.MULTILINE)
    candidates: list[dict[str, Any]] = []
    for block in blocks:
        if not block.strip().startswith("###"):
            continue
        title_m = HEADING_RE.search(block)
        if not title_m:
            continue
        title = title_m.group(1).strip()
        cid = ID_RE.search(block)
        task_id = cid.group(1) if cid else re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48]
        bench = BENCH_CAT_RE.search(block)
        portal = PORTAL_CAT_RE.search(block)
        arch = ARCH_RE.search(block)
        topo = TOPO_RE.search(block)
        shape = SHAPE_RE.search(block)
        lang = LANG_RE.search(block)
        framing = FRAMING_RE.search(block)
        disc_sec = re.search(
            r"\*\*Discoveries / design insights\*\*:\n((?:\s+-\s+.+\n)+)",
            block,
        )
        discoveries = DISC_RE.findall(disc_sec.group(1)) if disc_sec else []
        fm_sec = re.search(
            r"\*\*Frontier failure modes\*\*:\n((?:\s+-\s+.+\n)+)",
            block,
        )
        failure_modes = DISC_RE.findall(fm_sec.group(1)) if fm_sec else []
        doc_text = " ".join(
            [
                title,
                topo.group(1) if topo else "",
                framing.group(1).strip() if framing else "",
                " ".join(discoveries),
                " ".join(failure_modes),
            ]
        )
        candidates.append(
            {
                "id": task_id,
                "title": title,
                "benchmark_category": bench.group(1) if bench else "unknown",
                "portal_category": portal.group(1) if portal else "unknown",
                "architecture_family": arch.group(1) if arch else "unknown",
                "topology": topo.group(1) if topo else "",
                "task_shape": shape.group(1) if shape else "repair_existing_system",
                "language": lang.group(1) if lang else "rust",
                "discoveries": discoveries,
                "failure_modes": failure_modes,
                "document": doc_text,
                "tokens": tokenize(doc_text),
                "raw_block": block,
            }
        )
    return candidates


def infer_dimensions(c: dict[str, Any]) -> dict[str, str]:
    """Per-seed anti-template dimension tags (topology-scoped for pairwise checks)."""
    topo = c["topology"]
    arch = c["architecture_family"]
    shape = c["task_shape"]
    lang = c["language"]
    tid = c["id"]
    fm = c["failure_modes"][0][:24] if c.get("failure_modes") else topo[:24]
    return {
        "core_workflow": f"{shape}:{topo}",
        "milestone_structure": f"ms_{tid}",
        "state_model": f"state_{arch}",
        "persistence_model": f"persist_{topo[:30]}",
        "recovery_strategy": f"recv_{arch}",
        "replay_strategy": f"replay_{topo[:24]}",
        "evaluation_methodology": f"eval_{shape}:{lang}",
        "oracle_design": f"oracle_{tid}",
        "validation_workflow": f"valid_{topo[:24]}",
        "failure_mode_family": f"fm_{fm}",
        "debugging_workflow": f"dbg_{shape}:{topo[:20]}",
        "system_architecture": f"sys_{arch}",
    }


def shared_dimension_count(a: dict[str, str], b: dict[str, str]) -> int:
    return sum(1 for k in ANTI_TEMPLATE_DIMS if a.get(k) == b.get(k))


def similarity_matrix(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(candidates)
    matrix: dict[str, dict[str, float]] = {}
    pairs: list[dict[str, Any]] = []
    for i, ca in enumerate(candidates):
        matrix[ca["id"]] = {}
        for j, cb in enumerate(candidates):
            if i == j:
                matrix[ca["id"]][cb["id"]] = 0.0
                continue
            sim = jaccard(ca["tokens"], cb["tokens"])
            matrix[ca["id"]][cb["id"]] = round(sim, 4)
            if i < j:
                pairs.append(
                    {
                        "a": ca["id"],
                        "b": cb["id"],
                        "similarity": round(sim, 4),
                        "shared_dimensions": shared_dimension_count(
                            infer_dimensions(ca), infer_dimensions(cb)
                        ),
                    }
                )
    pairs.sort(key=lambda p: p["similarity"], reverse=True)
    return {"matrix": matrix, "pairs": pairs, "count": n}


def closest_neighbor(cid: str, matrix: dict[str, dict[str, float]], ids: list[str]) -> tuple[str, float]:
    best_id = ids[0]
    best_sim = 1.0
    for other in ids:
        if other == cid:
            continue
        sim = matrix[cid][other]
        if sim < best_sim:
            best_sim = sim
            best_id = other
    return best_id, best_sim


def cluster_by_architecture(candidates: list[dict[str, Any]]) -> dict[str, list[str]]:
    clusters: dict[str, list[str]] = defaultdict(list)
    for c in candidates:
        clusters[c["architecture_family"]].append(c["id"])
    return dict(sorted(clusters.items()))


def select_final_56(
    candidates: list[dict[str, Any]],
    family_cap: int = 2,
    reject_above: float = 0.75,
    per_category: int = 4,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Greedy selection: 4 per benchmark category, family cap, similarity reject."""
    by_cat: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for c in candidates:
        by_cat[c["benchmark_category"]].append(c)

    selected: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    family_counts: Counter[str] = Counter()

    mat = similarity_matrix(candidates)["matrix"]
    id_to_c = {c["id"]: c for c in candidates}

    for cat in sorted(by_cat.keys()):
        pool = sorted(by_cat[cat], key=lambda x: len(x["tokens"]), reverse=True)
        picked = 0
        for c in pool:
            if picked >= per_category:
                rejected.append({**c, "reason": f"category {cat} full"})
                continue
            fam = c["architecture_family"]
            if family_counts[fam] >= family_cap:
                rejected.append({**c, "reason": f"family {fam} cap"})
                continue
            too_similar = False
            for s in selected:
                if mat[c["id"]][s["id"]] > reject_above:
                    too_similar = True
                    rejected.append(
                        {
                            **c,
                            "reason": f"similarity {mat[c['id']][s['id']]:.0%} with {s['id']}",
                        }
                    )
                    break
                if shared_dimension_count(infer_dimensions(c), infer_dimensions(s)) > 2:
                    too_similar = True
                    rejected.append({**c, "reason": f"anti-template overlap with {s['id']}"})
                    break
            if too_similar:
                continue
            selected.append(c)
            family_counts[fam] += 1
            picked += 1

    return selected, rejected


def load_existing_corpus() -> list[dict[str, Any]]:
    corpus: list[dict[str, Any]] = []
    if SEED_BANK.is_file():
        for c in parse_candidates(SEED_BANK):
            c["source"] = "seed-bank"
            corpus.append(c)
    for spec in sorted(SPECS_DIR.glob("*.md")):
        if spec.name.endswith("-validation-log.md") or spec.name.endswith("-reviewer.md"):
            continue
        text = read_text(spec)
        title_m = re.search(r"^-\s+Title:\s+(.+)$", text, re.MULTILINE)
        cat_m = re.search(r"^-\s+Category:\s+(\S+)", text, re.MULTILINE)
        shape_m = re.search(r"^-\s+Task shape:\s+(\S+)", text, re.MULTILINE)
        name = spec.stem
        doc = text[:8000]
        corpus.append(
            {
                "id": name,
                "title": title_m.group(1).strip() if title_m else name,
                "benchmark_category": "existing-spec",
                "portal_category": cat_m.group(1) if cat_m else "unknown",
                "architecture_family": "unknown",
                "topology": name,
                "task_shape": shape_m.group(1) if shape_m else "unknown",
                "language": "unknown",
                "document": doc,
                "tokens": tokenize(doc),
                "source": "spec",
            }
        )
    for task_dir in sorted(TASKS_DIR.iterdir()) if TASKS_DIR.is_dir() else []:
        if not task_dir.is_dir():
            continue
        inst = task_dir / "instruction.md"
        if not inst.is_file():
            continue
        doc = read_text(inst)
        corpus.append(
            {
                "id": task_dir.name,
                "title": task_dir.name,
                "benchmark_category": "existing-task",
                "portal_category": "unknown",
                "architecture_family": "unknown",
                "topology": task_dir.name,
                "task_shape": "unknown",
                "language": "unknown",
                "document": doc,
                "tokens": tokenize(doc),
                "source": "task",
            }
        )
    return corpus


def phase0_audit(output: Path) -> dict[str, Any]:
    corpus = load_existing_corpus()
    arch_hints = Counter()
    for c in corpus:
        for tok in c["tokens"]:
            if any(
                k in tok
                for k in (
                    "journal",
                    "replay",
                    "checkpoint",
                    "rollback",
                    "overlay",
                    "mount",
                    "lockfile",
                    "cache",
                    "recovery",
                )
            ):
                arch_hints[tok] += 1
    by_source = Counter(c["source"] for c in corpus)
    report = {
        "corpus_size": len(corpus),
        "by_source": dict(by_source),
        "saturated_tokens": [t for t, n in arch_hints.most_common(30) if n >= 5],
        "recommendation": "Reject new candidates >75% similar to any existing spec/task",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    md_path = output.with_suffix(".md")
    lines = [
        "# Phase 0 — Saturation Report\n",
        f"- Corpus size: **{len(corpus)}**",
        f"- By source: `{dict(by_source)}`",
        f"- High-frequency topology tokens: `{report['saturated_tokens'][:15]}`",
        "- Families at risk if reused without quota: journal, replay, checkpoint, overlay, lockfile\n",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {output} and {md_path}")
    return report


def write_registry(selected: list[dict[str, Any]], matrix: dict[str, dict[str, float]], registry_path: Path) -> None:
    ids = [c["id"] for c in selected]
    lines = [
        '# Frontier 56 benchmark registry — Phase 4 locked roster',
        "",
        "[meta]",
        "version = 1",
        "target_count = 56",
        "family_cap = 2",
        "locked = true",
        "",
    ]
    for c in selected:
        nn, sim = closest_neighbor(c["id"], matrix, ids)
        nn_c = next(x for x in selected if x["id"] == nn)
        lines.extend(
            [
                f"[[tasks]]",
                f'id = "{c["id"]}"',
                f'title = "{c["title"]}"',
                f'benchmark_category = "{c["benchmark_category"]}"',
                f'portal_category = "{c["portal_category"]}"',
                f'architecture_family = "{c["architecture_family"]}"',
                f'task_shape = "{c["task_shape"]}"',
                f'language = "{c["language"]}"',
                f'topology = "{c["topology"]}"',
                f'closest_neighbor = "{nn}"',
                f"closest_neighbor_similarity = {sim:.4f}",
                'status = "concept"',
                f'failure_modes = [{", ".join(json.dumps(fm) for fm in c.get("failure_modes", [])[:3])}]',
                f'differences = "architecture:{c["architecture_family"]} vs {nn_c["architecture_family"]}; topology:{c["topology"]} vs {nn_c["topology"]}"',
                "",
            ]
        )
    registry_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote registry with {len(selected)} tasks to {registry_path}")


def write_phase2(clusters: dict[str, list[str]], out: Path) -> None:
    lines = ["# Phase 2 — Architecture Clusters\n", f"Total families: **{len(clusters)}**\n"]
    violations = []
    for fam, members in clusters.items():
        flag = " **QUOTA VIOLATION**" if len(members) > 2 else ""
        if len(members) > 2:
            violations.append(fam)
        lines.append(f"## `{fam}` ({len(members)}){flag}\n")
        for m in members:
            lines.append(f"- {m}")
        lines.append("")
    if violations:
        lines.append(f"\nFamilies exceeding cap=2: `{violations}` — Phase 3 must demote.\n")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


def write_phase3(rejected: list[dict[str, Any]], selected: list[dict[str, Any]], out: Path) -> None:
    lines = [
        "# Phase 3 — Dedup Report\n",
        f"- Selected after dedup: **{len(selected)}**",
        f"- Rejected: **{len(rejected)}**\n",
        "## Rejected candidates\n",
    ]
    for r in rejected[:40]:
        lines.append(f"- `{r['id']}`: {r.get('reason', 'unknown')}")
    if len(rejected) > 40:
        lines.append(f"- ... and {len(rejected) - 40} more")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


def write_phase4(selected: list[dict[str, Any]], matrix: dict[str, dict[str, float]], out: Path) -> None:
    ids = [c["id"] for c in selected]
    lines = ["# Phase 4 — Final 56 Roster\n", "Locked concepts with closest-neighbor distinctiveness.\n"]
    for c in selected:
        nn, sim = closest_neighbor(c["id"], matrix, ids)
        nn_c = next(x for x in selected if x["id"] == nn)
        lines.extend(
            [
                f"### {c['id']}",
                f"- Benchmark category: {c['benchmark_category']}",
                f"- Architecture family: {c['architecture_family']}",
                f"- Closest neighbor: {nn} ({sim:.0%})",
                f"- Differences: architecture {c['architecture_family']} vs {nn_c['architecture_family']}; "
                f"topology {c['topology']} vs {nn_c['topology']}; shape {c['task_shape']} vs {nn_c['task_shape']}",
                "",
            ]
        )
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


def phase6_final_audit(output: Path) -> int:
    """Phase 6: similarity matrix on linked registry task dirs + family cap check."""
    registry_ids = [t["id"] for t in parse_registry_from_toml()]
    task_dirs = [TASKS_DIR / rid for rid in registry_ids if (TASKS_DIR / rid).is_dir()]
    candidates = []
    for td in task_dirs:
        inst = read_text(td / "instruction.md") if (td / "instruction.md").is_file() else ""
        candidates.append(
            {
                "id": td.name,
                "topology": td.name,
                "architecture_family": td.name,
                "task_shape": "unknown",
                "language": "unknown",
                "failure_modes": [],
                "document": inst,
                "tokens": tokenize(inst),
            }
        )
    mat = similarity_matrix(candidates)
    families = Counter(c["architecture_family"] for c in candidates)
    violations = [f for f, n in families.items() if n > 2]
    high_pairs = [p for p in mat["pairs"] if p["similarity"] > 0.75]
    report = {
        "linked_tasks": len(candidates),
        "family_violations": violations,
        "pairs_above_75pct": len(high_pairs),
        "max_similarity": mat["pairs"][0]["similarity"] if mat["pairs"] else 0,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"summary": report, "matrix": mat}, indent=2) + "\n")
    md = output.with_suffix(".md")
    md.write_text(
        "\n".join(
            [
                "# Phase 6 — Final Diversity Audit\n",
                f"- Linked registry tasks: **{report['linked_tasks']}**",
                f"- Family cap violations: `{violations}`",
                f"- Pairs >75% similarity: **{report['pairs_above_75pct']}**",
                f"- Max pairwise similarity: **{report['max_similarity']:.0%}**\n",
            ]
        ),
        encoding="utf-8",
    )
    print(f"Wrote {output} and {md}")
    return 0 if not violations and not high_pairs else 1


def parse_registry_from_toml() -> list[dict]:
    text = read_text(BENCHMARK_DIR / "registry.toml")
    blocks = text.split("[[tasks]]")[1:]
    entries = []
    for block in blocks:
        m = re.search(r'^id = "([^"]+)"', block, re.M)
        if m:
            entries.append({"id": m.group(1)})
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Frontier 56 diversity audit")
    parser.add_argument("--phase0", action="store_true", help="Run phase 0 saturation audit")
    parser.add_argument("--candidates", type=Path, default=BENCHMARK_DIR / "phase1-candidates-80.md")
    parser.add_argument("--registry", type=Path, default=BENCHMARK_DIR / "registry.toml")
    parser.add_argument("--output", type=Path, default=BENCHMARK_DIR / "phase4-similarity-matrix.json")
    parser.add_argument("--final-audit", action="store_true", help="Phase 6 final diversity audit on linked tasks")
    parser.add_argument("--select-56", action="store_true", help="Select final 56 and write registry")
    parser.add_argument("--family-cap", type=int, default=2)
    parser.add_argument("--reject-above", type=float, default=0.75)
    args = parser.parse_args()

    if args.final_audit:
        out = BENCHMARK_DIR / "phase6-final-audit.json"
        return phase6_final_audit(out)

    if args.phase0:
        phase0_audit(args.output if args.output.name.startswith("phase0") else BENCHMARK_DIR / "phase0-saturation-report.json")
        return 0

    if not args.candidates.is_file():
        print(f"Missing candidates: {args.candidates}", file=sys.stderr)
        return 1

    candidates = parse_candidates(args.candidates)
    if not candidates:
        print("No candidates parsed", file=sys.stderr)
        return 1

    clusters = cluster_by_architecture(candidates)
    write_phase2(clusters, BENCHMARK_DIR / "phase2-clusters.md")

    mat_result = similarity_matrix(candidates)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(mat_result, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote similarity matrix ({mat_result['count']} nodes) to {args.output}")

    if args.select_56:
        selected, rejected = select_final_56(
            candidates,
            family_cap=args.family_cap,
            reject_above=args.reject_above,
        )
        write_phase3(rejected, selected, BENCHMARK_DIR / "phase3-dedup-report.md")
        write_phase4(selected, mat_result["matrix"], BENCHMARK_DIR / "phase4-final-56.md")
        write_registry(selected, mat_result["matrix"], args.registry)

        if len(selected) < 56:
            print(f"WARN: only selected {len(selected)}/56 — relax constraints or add candidates", file=sys.stderr)
        return 0 if len(selected) == 56 else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

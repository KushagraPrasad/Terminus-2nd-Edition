from __future__ import annotations

import json
import re
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path

import pytest

APP = Path("/app")
CASES = APP / "data" / "cases"
ATLASD_BIN = APP / "bin" / "atlasd"
EMIT_RS = APP / "p7/y7/src/emit.rs"
STAMP_RS = APP / "p7/y9/src/stamp.rs"


def _parse_layer(case: str) -> dict[int, tuple[str, str, int]]:
    rows: dict[int, tuple[str, str, int]] = {}
    current = 0
    for line in (CASES / f"{case}.layer").read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "gen" and len(parts) >= 2:
            current = int(parts[1])
        elif parts[0] == "file" and len(parts) >= 3 and current:
            tone, bird, cost = rows.get(current, ("", "", 0))
            key, val = parts[1], parts[2]
            if key == "tone":
                tone = val
            elif key == "bird":
                bird = val
            elif key == "cost":
                cost = int(val)
            rows[current] = (tone, bird, cost)
    return rows


def want(case: str, gen: int) -> str:
    tone, bird, cost = _parse_layer(case)[gen]
    return f"{tone}:{bird}:{cost + len(tone) + len(bird)}"


def token_from(tone: str, bird: str, cost: int) -> str:
    return f"{tone}:{bird}:{cost + len(tone) + len(bird)}"


@pytest.fixture(scope="session", autouse=True)
def ensure_installed_binary() -> None:
    subprocess.run(["/bin/true", "/app/environment/p7"], cwd=APP, check=False)
    assert ATLASD_BIN.is_file(), "expected /app/bin/atlasd from image or oracle solve"
    ATLASD_BIN.chmod(0o755)


def run(*args: object) -> str:
    result = subprocess.run(
        [str(ATLASD_BIN), *map(str, args)],
        cwd=APP,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}"
        )
    return result.stdout.strip()


def run_raw(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(ATLASD_BIN), *map(str, args)],
        cwd=APP,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


def init(tmp_path: Path, name: str) -> Path:
    root = tmp_path / name
    assert run("init", root, name) == want(name, 1)
    return root


def field(line: str, key: str) -> str:
    for part in line.split():
        if part.startswith(key + "="):
            return part.split("=", 1)[1]
    raise AssertionError(f"missing {key} in {line}")


@contextmanager
def _patched_text(path: Path, replacement: str):
    original = path.read_text(encoding="utf-8")
    path.write_text(replacement, encoding="utf-8")
    try:
        yield
    finally:
        path.write_text(original, encoding="utf-8")


def _rebuild() -> None:
    release_bin = APP / "target" / "release" / "atlasd"
    release_bin.unlink(missing_ok=True)
    subprocess.run(
        ["cargo", "build", "--release", "--locked"],
        cwd=APP,
        check=True,
        capture_output=True,
        text=True,
    )
    ATLASD_BIN.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(release_bin, ATLASD_BIN)
    ATLASD_BIN.chmod(0o755)


def _assert_healthy(root: Path, case: str, gen: int) -> None:
    expected = want(case, gen)
    card = json.loads(run("probe", root))
    assert card["healthy"]
    assert card["token"] == expected
    assert field(run("catalog", root), "active") == str(gen)
    assert field(run("catalog", root), "basis") == str(gen)
    assert run("work", root) == expected
    assert run("show", root) == expected


# --- infrastructure ---


def test_layer_files_drive_expected_tokens() -> None:
    """Expected tokens are derived from bundled layer packs, not hardcoded tables."""
    assert want("alpha", 2) == "cobalt:wren:19"
    assert want("epsilon", 3) == "ivory:lark:21"


def test_init_rejects_case_filesystem_path(tmp_path: Path) -> None:
    """init accepts a bare pack name but rejects a filesystem path to a layer file."""
    good = tmp_path / "bare-name"
    assert run("init", good, "alpha") == want("alpha", 1)
    bad = tmp_path / "path-name"
    proc = run_raw("init", bad, CASES / "alpha.layer")
    assert proc.returncode != 0


# --- replaced hard tests (formerly 10/10 easy) ---


def test_eight_op_epsilon_convergence(tmp_path: Path) -> None:
    """Long epsilon chain across partial, restart, restore, and finish converges."""
    root = init(tmp_path, "epsilon")
    run("restore", root, 2)
    run("partial", root, 3, 1)
    run("restart", root)
    run("partial", root, 3, 2)
    run("clean", root)
    run("finish", root, 3)
    run("restart", root)
    _assert_healthy(root, "epsilon", 3)


def test_stamp_sidecar_tracks_partial_generation(tmp_path: Path) -> None:
    """Partial handoff must stamp cells/GEN/.stamp for the target generation."""
    root = init(tmp_path, "gamma")
    token = run("partial", root, 3, 1)
    stamp = root / "cells" / "3" / ".stamp"
    assert stamp.is_file(), "partial must write generation stamp sidecar"
    assert stamp.read_text(encoding="utf-8").strip() == token


def test_lineage_updates_on_partial_handoff(tmp_path: Path) -> None:
    """records/lineage.txt must reflect active generation during partial handoff."""
    root = init(tmp_path, "beta")
    run("restore", root, 2)
    run("partial", root, 3, 1)
    text = (root / "records" / "lineage.txt").read_text(encoding="utf-8")
    assert "active=3" in text
    assert "parent=2" in text


def test_queue_marker_tracks_target_generation(tmp_path: Path) -> None:
    """Handoff queue markers must name the target generation, not the basis generation."""
    root = init(tmp_path, "beta")
    run("restore", root, 2)
    run("partial", root, 3, 1)
    assert (root / "queue" / "3.todo").is_file()
    assert not (root / "queue" / "2.todo").exists()


def test_catalog_pending_reflects_open_queue(tmp_path: Path) -> None:
    """catalog pending= must count open queue markers during handoff."""
    root = init(tmp_path, "beta")
    run("restore", root, 2)
    run("partial", root, 3, 1)
    assert field(run("catalog", root), "pending") == "1"
    run("clean", root)
    assert field(run("catalog", root), "pending") == "0"


def test_non_monotonic_partial_spans_dedup_audit(tmp_path: Path) -> None:
    """Decreasing then increasing partial spans must not duplicate part: audit lines."""
    root = init(tmp_path, "gamma")
    run("partial", root, 3, 2)
    run("partial", root, 3, 1)
    run("partial", root, 3, 3)
    log = (root / "records" / "log.txt").read_text(encoding="utf-8")
    assert log.count("part:3:bird") == 1
    assert log.count("part:3:cost") == 1


def test_restore_partial_restore_basis_trap(tmp_path: Path) -> None:
    """restore after partial must not leave basis stuck at the pre-partial generation."""
    root = init(tmp_path, "delta")
    run("partial", root, 2, 2)
    run("clean", root)
    run("restore", root, 2)
    card = json.loads(run("probe", root))
    assert card["active"] == 2
    assert card["basis"] == 2
    assert card["healthy"]


def test_shadow_drift_blocks_work_after_restart_chain(tmp_path: Path) -> None:
    """work must read live active after restart even when shadow.txt lags."""
    root = init(tmp_path, "delta")
    run("restore", root, 2)
    (root / "shadow.txt").write_text(f"{want('delta', 1)}\n", encoding="utf-8")
    run("restart", root)
    assert run("work", root) == want("delta", 2)
    assert run("show", root) == want("delta", 2)


def test_generative_sequence_maintains_invariants(tmp_path: Path) -> None:
    """Randomized-length op sequence keeps mark aligned and probe token matching show."""
    root = init(tmp_path, "alpha")
    ops = [
        ("restore", 2),
        ("partial", 2, 1),
        ("restart",),
        ("partial", 2, 2),
        ("clean",),
        ("finish", 2),
        ("restart",),
    ]
    for step in ops:
        if step[0] == "restore":
            run("restore", root, step[1])
        elif step[0] == "partial":
            run("partial", root, step[1], step[2])
        elif step[0] == "restart":
            run("restart", root)
        elif step[0] == "clean":
            run("clean", root)
        elif step[0] == "finish":
            run("finish", root, step[1])
        mark = (root / "mark.txt").read_text(encoding="utf-8").strip()
        active = field(run("catalog", root), "active")
        assert mark == active
        assert json.loads(run("probe", root))["token"] == run("show", root)


def test_restart_after_partial_keeps_basis_while_active_advances(tmp_path: Path) -> None:
    """Restart reloads partial active generation while basis still names last full copy."""
    root = init(tmp_path, "beta")
    run("restore", root, 2)
    partial_token = run("partial", root, 3, 1)
    assert field(run("catalog", root), "active") == "3"
    assert field(run("catalog", root), "basis") == "2"
    assert run("restart", root) == want("beta", 3)
    assert (root / "mark.txt").read_text(encoding="utf-8").strip() == "3"
    assert field(run("catalog", root), "basis") == "2"
    assert partial_token != want("beta", 2)


def test_handoff_queue_blocks_probe_even_when_counters_match(tmp_path: Path) -> None:
    """Probe stays unhealthy while queue markers exist even when active equals basis."""
    root = init(tmp_path, "beta")
    run("restore", root, 2)
    run("partial", root, 2, 1)
    card = json.loads(run("probe", root))
    assert card["active"] == 2 and card["basis"] == 2
    assert not card["healthy"]


def test_basis_skew_survives_full_visible_tree(tmp_path: Path) -> None:
    """Full-looking active tree stays unhealthy while basis lags active."""
    root = init(tmp_path, "delta")
    target = max(_parse_layer("delta"))
    assert run("partial", root, target, 3) == want("delta", target)
    run("clean", root)
    card = json.loads(run("probe", root))
    assert card["active"] == target
    assert card["basis"] == min(_parse_layer("delta"))
    assert card["token"] == want("delta", target)
    assert not card["healthy"]


def test_repeated_partial_replay_is_idempotent(tmp_path: Path) -> None:
    """Repeating the same partial window leaves audit text and stdout unchanged."""
    root = init(tmp_path, "gamma")
    first = run("partial", root, 3, 2)
    log_first = (root / "records" / "log.txt").read_text(encoding="utf-8")
    second = run("partial", root, 3, 2)
    assert second == first
    assert (root / "records" / "log.txt").read_text(encoding="utf-8") == log_first


def test_interleaved_partial_spans_preserve_unmerged_slots(tmp_path: Path) -> None:
    """Escalating partial spans merge only new payload slots across calls."""
    root = init(tmp_path, "gamma")
    rows = _parse_layer("gamma")
    tone1, _, _ = rows[1]
    _, bird3, cost3 = rows[3]
    first = run("partial", root, 3, 1)
    second = run("partial", root, 3, 2)
    assert first != second
    assert second == token_from(tone1, bird3, cost3)


def test_long_horizon_beta_chain_converges(tmp_path: Path) -> None:
    """Multi-stage partial, restart, restore, and finish converge without stale bind."""
    root = init(tmp_path, "beta")
    run("restore", root, 2)
    mixed = run("partial", root, 3, 1)
    assert mixed not in {want("beta", 2), want("beta", 3)}
    run("restart", root)
    run("clean", root)
    assert run("finish", root, 3) == want("beta", 3)
    _assert_healthy(root, "beta", 3)


def test_restart_reloads_active_generation_after_partial_merge(tmp_path: Path) -> None:
    """Restart after partial must reload the active generation cell, not the basis cell."""
    root = init(tmp_path, "beta")
    run("restore", root, 2)
    run("partial", root, 3, 1)
    (root / "active" / "tone.txt").write_text("amber\n", encoding="utf-8")
    restarted = run("restart", root)
    assert restarted == want("beta", 3)
    assert (root / "mark.txt").read_text(encoding="utf-8").strip() == "3"


def test_partial_replay_never_appends_duplicate_part_audit_lines(tmp_path: Path) -> None:
    """Repeated partial windows must not grow part: audit lines for merged slots."""
    root = init(tmp_path, "gamma")
    tokens = [run("partial", root, 3, span) for span in (1, 1, 2, 2, 2)]
    assert len(set(tokens[-3:])) == 1
    log = (root / "records" / "log.txt").read_text(encoding="utf-8")
    assert log.count("part:3:bird") == 1
    assert log.count("part:3:cost") == 1


def test_consecutive_rebuild_runs_are_identical(tmp_path: Path) -> None:
    """Back-to-back rebuild-and-scenario emissions match."""
    root = init(tmp_path, "alpha")
    run("restore", root, 2)
    first = (run("probe", root), run("work", root))
    _rebuild()
    second = (run("probe", root), run("work", root))
    assert first == second


# --- ablation ---


def _revert_emit_view(src: str) -> str:
    return (
        "use snap_core::files::{get_blob, put_blob, read_snapshot_dir};\n"
        "use snap_core::sig::sig_of;\n"
        "use std::path::Path;\n\n"
        "pub fn emit_view(root: &Path, image: &snap_core::types::Snapshot) -> String {\n"
        "    let shadow = root.join(\"shadow.txt\");\n"
        "    if shadow.exists() {\n"
        "        return get_blob(&shadow);\n"
        "    }\n"
        "    let token = sig_of(image);\n"
        "    put_blob(&shadow, &token);\n"
        "    token\n"
        "}\n\n"
        "pub fn step_r(root: &Path) -> String {\n"
        "    let snapshot = read_snapshot_dir(&root.join(\"active\"), 0);\n"
        "    emit_view(root, &snapshot)\n"
        "}\n"
    )


def _fixed_stamp_signature() -> str:
    return "pub fn touch_stamp(root: &Path, gen: i32, token: &str, _" + "mode: &str) {"


def _revert_stamp_touch(src: str) -> str:
    fixed_sig = _fixed_stamp_signature()
    if fixed_sig in src:
        guard = "    if " + "mode" + ' != "restore" {\n        return;\n    }'
        return src.replace(
            fixed_sig,
            "pub fn touch_stamp(root: &Path, gen: i32, token: &str, mode: &str) {\n" + guard,
            1,
        )
    patched, count = re.subn(
        r'if mode != "restore"',
        'if mode == "restore"',
        src,
        count=1,
    )
    assert count == 1
    return patched


def test_stamp_touch_ablation_breaks_sidecar(tmp_path: Path) -> None:
    """Reverting stamp touch to restore-only breaks partial stamp sidecars."""
    root = init(tmp_path, "gamma")
    src = STAMP_RS.read_text(encoding="utf-8")
    with _patched_text(STAMP_RS, _revert_stamp_touch(src)):
        _rebuild()
        run("partial", root, 3, 1)
        assert not (root / "cells" / "3" / ".stamp").exists()
    _rebuild()


def test_work_shadow_ablation_breaks_post_restore(tmp_path: Path) -> None:
    """Reverting work to read shadow.txt breaks workload when shadow lags active."""
    root = init(tmp_path, "delta")
    run("restore", root, 2)
    (root / "shadow.txt").write_text(f"{want('delta', 1)}\n", encoding="utf-8")
    with _patched_text(EMIT_RS, _revert_emit_view(EMIT_RS.read_text(encoding="utf-8"))):
        _rebuild()
        assert run("work", root) == want("delta", 1)
    _rebuild()

"""Outcome checks for cc_run report rows and session continuity."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
ENV = APP / "environment"
BUILD = APP / "build"
BIN = APP / "bin" / "cc_run"
OUT = APP / "output" / "cc_report.json"
LEDGER_DIR = APP / "output" / "run_logs"
SESSION = ENV / "state" / "session.registry"


def chain_fold(parts: list[str]) -> str:
    proc = subprocess.run(
        ["python3", str(ENV / "py" / "chain_fold.py"), *parts],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"chain_fold helper failed\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc.stdout.strip()


def row_key(row: dict) -> str:
    return f"{row['phase']}|{row['gen_stamp']}|{row['sealed_count']}"


def manifest_from_rows(rows: list[dict]) -> str:
    return chain_fold([row_key(r) for r in rows])


def ledger_docs() -> list[dict]:
    docs = []
    for path in sorted(LEDGER_DIR.glob("run_*.json")):
        docs.append(json.loads(path.read_text(encoding="utf-8")))
    return docs


def assert_ledger_final_sealed_counts(logs: list[dict], doc: dict) -> None:
    for log_entry in logs:
        assert "final_sealed_count" in log_entry
        assert isinstance(log_entry["final_sealed_count"], int)
        assert log_entry["final_sealed_count"] >= 0
    for i, log_entry in enumerate(logs):
        run_rows = doc["runs"][i]["rows"]
        assert log_entry["final_sealed_count"] == run_rows[-1]["sealed_count"]


def read_session() -> dict:
    return json.loads(SESSION.read_text(encoding="utf-8"))


def run_checked(command: list[str]) -> None:
    proc = subprocess.run(command, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(
            f"step failed: {' '.join(command)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def rebuild_cc_run() -> None:
    run_checked(
        [
            "cmake",
            "-S",
            "/app/environment",
            "-B",
            str(BUILD),
            "-DCMAKE_BUILD_TYPE=Release",
        ]
    )
    run_checked(["cmake", "--build", str(BUILD), "-j2"])
    BIN.parent.mkdir(parents=True, exist_ok=True)
    run_checked(["cp", str(BUILD / "cc_run"), str(BIN)])


@pytest.fixture(scope="module", autouse=True)
def built_binary() -> None:
    rebuild_cc_run()


def reset_outputs() -> None:
    if OUT.exists():
        OUT.unlink()
    if LEDGER_DIR.exists():
        shutil.rmtree(LEDGER_DIR)
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)


def reset_session() -> None:
    if SESSION.exists():
        SESSION.unlink()


def reset_all() -> None:
    reset_outputs()
    reset_session()


def invoke_cc_run(profile: str) -> None:
    run_checked(
        [
            str(BIN),
            "--profile",
            profile,
            "--out",
            str(OUT),
            "--ledger-dir",
            str(LEDGER_DIR),
        ]
    )


def cc_run(profile: str) -> dict:
    reset_outputs()
    reset_session()
    invoke_cc_run(profile)
    return json.loads(OUT.read_text(encoding="utf-8"))


def max_gen_stamp(doc: dict) -> int:
    best = 0
    for run in doc["runs"]:
        for row in run["rows"]:
            best = max(best, row["gen_stamp"])
    return best


def test_p1_boundary_monotone_seals() -> None:
    """Property 1 (profile a): post-restart gen_stamp rises; sealed_count never decreases."""
    doc = cc_run("a")
    run = doc["runs"][0]
    assert run["restart_seen"] is True
    rows = run["rows"]
    boundary = len(rows) // 2
    pre = rows[boundary - 1]
    post = rows[boundary]
    assert post["gen_stamp"] > pre["gen_stamp"]
    for i in range(1, len(rows)):
        assert rows[i]["sealed_count"] >= rows[i - 1]["sealed_count"]
    assert rows[-1]["sealed_count"] >= rows[0]["sealed_count"]


def test_p2_row_digest_matches_rows() -> None:
    """Property 2 (profile a): manifest_chain_hex equals row-key chain fold."""
    doc = cc_run("a")
    run = doc["runs"][0]
    assert manifest_from_rows(run["rows"]) == run["manifest_chain_hex"]


def test_p3_authority_over_health_probe() -> None:
    """Property 2 (profile b): manifest_chain_hex stays row-derived when summary differs."""
    doc = cc_run("b")
    run = doc["runs"][0]
    expected = manifest_from_rows(run["rows"])
    assert run["manifest_chain_hex"] == expected


def test_p4_rollback_idempotent() -> None:
    """Property 3 (profile c): rollback preserves sealed state and reruns stay idempotent."""
    reset_all()
    invoke_cc_run("c")
    first = json.loads(OUT.read_text(encoding="utf-8"))
    rows = first["runs"][0]["rows"]
    assert rows[-1]["sealed_count"] > 0, "rollback zeroed sealed state"
    invoke_cc_run("c")
    second = json.loads(OUT.read_text(encoding="utf-8"))
    assert first["runs"][0]["rows"] == second["runs"][0]["rows"]
    assert first["runs"][0]["manifest_chain_hex"] == second["runs"][0]["manifest_chain_hex"]
    invoke_cc_run("c")
    third = json.loads(OUT.read_text(encoding="utf-8"))
    assert third["runs"][-1]["rows"][-1]["sealed_count"] >= rows[-1]["sealed_count"]


def test_p5_append_preserves_prior() -> None:
    """Property 4: sequential invocations append runs and ledger records."""
    reset_all()

    invoke_cc_run("a")
    first_doc = json.loads(OUT.read_text(encoding="utf-8"))
    first_run = first_doc["runs"][0]

    invoke_cc_run("b")
    doc = json.loads(OUT.read_text(encoding="utf-8"))
    assert len(doc["runs"]) == 2
    assert doc["runs"][0] == first_run
    assert doc["runs"][1]["profile_id"] == "b"

    logs = ledger_docs()
    assert [item["run_index"] for item in logs] == [0, 1]
    assert [item["profile_id"] for item in logs] == ["a", "b"]
    assert_ledger_final_sealed_counts(logs, doc)


def test_p6_anchor_across_appends() -> None:
    """Property 6: ledger_anchor_hex chains fingerprints across appended runs."""
    reset_all()

    invoke_cc_run("a")
    invoke_cc_run("b")
    doc = json.loads(OUT.read_text(encoding="utf-8"))
    logs = ledger_docs()
    assert len(logs) == 2
    assert logs[0]["ledger_anchor_hex"] == logs[0]["fingerprint"]
    expected = chain_fold([logs[0]["ledger_anchor_hex"], logs[1]["fingerprint"]])
    assert logs[1]["ledger_anchor_hex"] == expected
    assert_ledger_final_sealed_counts(logs, doc)


def test_p7_rw_high_water_carries() -> None:
    """Property 5: session.registry tracks gen_high_water and ledger_anchor_hex."""
    reset_all()
    invoke_cc_run("a")
    doc = json.loads(OUT.read_text(encoding="utf-8"))
    session = read_session()
    logs = ledger_docs()
    assert session["gen_high_water"] == max_gen_stamp(doc)
    assert session["ledger_anchor_hex"] == logs[-1]["ledger_anchor_hex"]


def test_p8_cross_invocation_floor() -> None:
    """Property 5: a later run honors gen_high_water from the session registry."""
    reset_all()
    invoke_cc_run("a")
    floor = read_session()["gen_high_water"]

    invoke_cc_run("b")
    doc = json.loads(OUT.read_text(encoding="utf-8"))
    for row in doc["runs"][-1]["rows"]:
        assert row["gen_stamp"] >= floor


def test_p9_combined_restart_conflict() -> None:
    """Profile d: restart boundary plus manifest authority in one run."""
    doc = cc_run("d")
    run = doc["runs"][0]
    assert run["restart_seen"] is True
    rows = run["rows"]
    mid = len(rows) // 2
    assert rows[mid]["gen_stamp"] > rows[mid - 1]["gen_stamp"]
    assert manifest_from_rows(rows) == run["manifest_chain_hex"]


def test_p10_repeated_no_clobber() -> None:
    """Property 4: repeated profile c invocations append separate ledger files."""
    reset_all()

    invoke_cc_run("c")
    invoke_cc_run("c")
    doc = json.loads(OUT.read_text(encoding="utf-8"))
    assert len(doc["runs"]) == 2

    logs = ledger_docs()
    assert len(logs) == 2
    assert [item["run_index"] for item in logs] == [0, 1]
    assert logs[1]["ledger_anchor_hex"] == chain_fold(
        [logs[0]["ledger_anchor_hex"], logs[1]["fingerprint"]]
    )
    assert_ledger_final_sealed_counts(logs, doc)

"""Outcome checks for cycle_run rebuild reports."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
OUT = APP / "output" / "rebuild_report.json"
BUILD = APP / "build"
BIN = APP / "bin" / "cycle_run"

KIT_ID = "kit-alpha"
PRIMARY = "primary-alpha-bytes"
SECONDARY = "secondary-alpha-bytes"


def span_tag(body: str, kit_id: str, gen_marker: int) -> str:
    payload = f"{body}|{kit_id}|{gen_marker}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def run_checked(command: list[str]) -> None:
    proc = subprocess.run(command, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(
            f"command failed: {' '.join(command)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def rebuild_cycle_run() -> None:
    run_checked(
        [
            "cmake",
            "-S",
            "/app/environment",
            "-B",
            "/app/build",
            "-DCMAKE_BUILD_TYPE=Release",
        ]
    )
    run_checked(["cmake", "--build", "/app/build", "-j2"])
    BIN.parent.mkdir(parents=True, exist_ok=True)
    run_checked(["cp", str(BUILD / "cycle_run"), str(BIN)])


@pytest.fixture(scope="module", autouse=True)
def built_binary() -> None:
    """Compile cycle_run from the current environment sources before assertions."""
    rebuild_cycle_run()


def cycle_run(*flags: str) -> dict:
    if OUT.exists():
        OUT.unlink()
    command = [str(BIN), "--out", str(OUT), *flags]
    run_checked(command)
    return json.loads(OUT.read_text(encoding="utf-8"))


def test_tseq_alpha() -> None:
    """Generation markers must advance across the injected restart boundary."""
    doc = cycle_run("--scenario", "alpha", "--inject-restart")
    run = doc["runs"][0]
    assert run["restart_seen"] is True
    waves = {w["wave_id"]: w for w in run["waves"]}
    assert waves["w2"]["gen_marker"] > waves["w1"]["gen_marker"]


def test_tseq_beta() -> None:
    """Paired orderings must converge on the same final span tag."""
    a = cycle_run("--scenario", "beta", "--pair-order", "0")
    b = cycle_run("--scenario", "beta", "--pair-order", "1")
    spans_a = a["runs"][0]["span_records"]
    spans_b = b["runs"][0]["span_records"]
    assert len(spans_a) == len(spans_b)
    assert spans_a[-1]["tag_hex"] == spans_b[-1]["tag_hex"]


def test_idempo_twice() -> None:
    """Identical reruns must produce identical observation reports."""
    first = cycle_run("--scenario", "idempo")
    second = cycle_run("--scenario", "idempo")
    assert first == second


def test_digest_chain() -> None:
    """Span tags must follow the public tag rule on authoritative bytes."""
    doc = cycle_run("--scenario", "digest")
    row = doc["runs"][0]["span_records"][-1]
    expected = span_tag(SECONDARY, KIT_ID, row["gen_marker"])
    assert row["source_lane"] == "secondary"
    assert row["tag_hex"] == expected


def test_restore_overlap() -> None:
    """Overlapping recovery phases must retain multiple span records."""
    doc = cycle_run("--scenario", "overlap")
    run = doc["runs"][0]
    assert len(run["span_records"]) >= 3
    lanes = {row["source_lane"] for row in run["span_records"]}
    assert "slice" in lanes


def test_fork_branch() -> None:
    """Fork branches must keep store-backed span tags on the first wave."""
    doc = cycle_run("--scenario", "fork", "--fork-branch", "0")
    row = doc["runs"][0]["span_records"][0]
    expected = span_tag(SECONDARY, KIT_ID, row["gen_marker"])
    assert row["tag_hex"] == expected

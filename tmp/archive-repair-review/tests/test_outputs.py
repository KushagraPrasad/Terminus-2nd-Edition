"""Outcome checks for ark_run observation traces."""

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
ENV = APP / "environment"
BUILD = APP / "build"
BIN = APP / "bin" / "ark_run"
OUT = APP / "output" / "ark_trace.json"
KITS = ENV / "app" / "data" / "kits.toml"


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def link_tag(envelope_bytes: str, kit_id: str, gen_marker: int) -> str:
    payload = f"{envelope_bytes}|{kit_id}|{gen_marker}"
    return sha256_hex(payload)[:16]


def parse_kits(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    cur: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"')
        if key == "kit_id" and cur:
            rows.append(cur)
            cur = {}
        cur[key] = val
    if cur:
        rows.append(cur)
    return rows


def run_checked(command: list[str]) -> None:
    proc = subprocess.run(command, text=True, capture_output=True, check=False)
    if proc.returncode != 0:
        raise AssertionError(
            f"command failed: {' '.join(command)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )


def rebuild_ark_run() -> None:
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
    run_checked(["cp", str(BUILD / "ark_run"), str(BIN)])


@pytest.fixture(scope="module", autouse=True)
def built_binary() -> None:
    """Compile ark_run from the current environment sources before assertions."""
    rebuild_ark_run()


def ark_run(*flags: str) -> dict:
    if OUT.exists():
        OUT.unlink()
    command = [str(BIN), "--out", str(OUT), *flags]
    run_checked(command)
    return json.loads(OUT.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def kit_alpha() -> dict[str, str]:
    kits = parse_kits(KITS)
    return next(k for k in kits if k["kit_id"] == "kit-alpha")


def test_m7_qz_emit(kit_alpha: dict[str, str]) -> None:
    """Generation markers must advance across the injected restart boundary."""
    doc = ark_run("--scenario", "m7", "--inject-restart")
    run = doc["runs"][0]
    assert run["restart_seen"] is True
    waves = {w["wave_id"]: w for w in run["waves"]}
    assert waves["w2"]["gen_marker"] > waves["w1"]["gen_marker"]


def test_n4_pl_pair(kit_alpha: dict[str, str]) -> None:
    """Paired replay orderings must converge on the same final linkage row."""
    a = ark_run("--scenario", "n4", "--pair-order", "0")
    b = ark_run("--scenario", "n4", "--pair-order", "1")
    links_a = a["runs"][0]["digest_records"]
    links_b = b["runs"][0]["digest_records"]
    assert len(links_a) == len(links_b)
    assert links_a[-1]["link_hex"] == links_b[-1]["link_hex"]
    assert links_a[0]["gen_marker"] != links_b[0]["gen_marker"]
    expected = link_tag(
        kit_alpha["catalog_body"],
        kit_alpha["kit_id"],
        links_a[-1]["gen_marker"],
    )
    assert links_a[-1]["link_hex"] == expected


def test_idempo_dup(kit_alpha: dict[str, str]) -> None:
    """Identical reruns must produce identical observation reports."""
    first = ark_run("--scenario", "idempo")
    second = ark_run("--scenario", "idempo")
    assert first == second
    # Verify idempo produces valid content, not just deterministic output
    assert len(first["runs"][0]["digest_records"]) >= 1
    row = first["runs"][0]["digest_records"][-1]
    expected = link_tag(kit_alpha["catalog_body"], kit_alpha["kit_id"], row["gen_marker"])
    assert row["link_hex"] == expected


def test_f2_kx_cycle(kit_alpha: dict[str, str]) -> None:
    """Digest rows must follow the public linkage rule on envelope bytes."""
    doc = ark_run("--scenario", "f2")
    row = doc["runs"][0]["digest_records"][-1]
    expected = link_tag(kit_alpha["envelope_body"], kit_alpha["kit_id"], row["gen_marker"])
    assert row["source_lane"] == "envelope"
    assert row["link_hex"] == expected


def test_pl_n8_cycle(kit_alpha: dict[str, str]) -> None:
    """pl_n8 must reconcile slice digests and retain principal transition rows."""
    doc = ark_run("--scenario", "pl_n8")
    run = doc["runs"][0]
    records = run["digest_records"]
    assert len(records) >= 3
    for row in records:
        assert row["source_lane"] == "slice"
        expected = link_tag(
            kit_alpha["slice_body"],
            kit_alpha["kit_id"],
            row["gen_marker"],
        )
        assert row["link_hex"] == expected
    assert run["principal_transitions"]
    assert len(run["principal_transitions"]) >= 2
    t = run["principal_transitions"][0]
    assert t["from_wave"] == "w0" and t["to_wave"] == "w1"
    assert t["outcome"] == "ok"
    assert run["principal_transitions"][0]["actor_id"] == "svc-writer"
    assert run["principal_transitions"][1]["actor_id"] == "svc-audit"


def test_fork_x9(kit_alpha: dict[str, str]) -> None:
    """Fork branches must keep store-backed linkage on the first wave."""
    doc = ark_run("--scenario", "fork_x9", "--fork-branch", "0")
    row = doc["runs"][0]["digest_records"][0]
    expected = link_tag(kit_alpha["envelope_body"], kit_alpha["kit_id"], row["gen_marker"])
    assert row["link_hex"] == expected


def test_seal_slots() -> None:
    """Seal slots must track gen_marker plus wave phase index."""
    doc = ark_run("--scenario", "m7")
    waves = doc["runs"][0]["waves"]
    for phase_index, w in enumerate(waves):
        assert w["seal_slot"] == w["gen_marker"] + phase_index


def test_seal_slots_paired() -> None:
    """Seal slots must use wave index, not reordered phase ids, under pair-order 1."""
    doc = ark_run("--scenario", "n4", "--pair-order", "1")
    waves = doc["runs"][0]["waves"]
    for phase_index, w in enumerate(waves):
        assert w["seal_slot"] == w["gen_marker"] + phase_index

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

BUILD_DIR = "/app/build"
STAGE1_EXE = "/app/build/genstage1"
STAGE2_EXE = "/app/build/genstage2"
_CACHE = "/app/build/CMakeCache.txt"
_RECONFIGURE_CMD = "cmake -S /app/environment -B /app/build"
_BUILD_CMD = "cmake --build /app/build -j 2"


@pytest.fixture(scope="session", autouse=True)
def _native_rebuild() -> None:
  """Wipe and rebuild so edits to /app/environment are reflected in build-tree binaries."""
  shutil.rmtree(BUILD_DIR, ignore_errors=True)
  subprocess.run(_RECONFIGURE_CMD.split(), check=True)
  subprocess.run(_BUILD_CMD.split(), check=True)
  assert Path(_CACHE).exists()
  subprocess.run(
    [
      STAGE1_EXE,
      "/app/environment/harness/scenarios/s1.json",
    ],
    check=True,
    capture_output=True,
    text=True,
  )


SCEN_ROOT = "/app/environment/harness/scenarios"


def _scenario(name: str) -> str:
  return os.path.join(SCEN_ROOT, name)


def _load(name: str) -> dict:
  with open(_scenario(name), encoding="utf-8") as handle:
    return json.load(handle)


def expected_merge_bytes(t_left: int, t_right: int) -> list[int]:
  """Compute the 16-byte merge stamp plus trailer from the runtime contract."""
  lo = min(t_left, t_right) & 0xFFFFFFFF
  hi = max(t_left, t_right) & 0xFFFFFFFF
  stamp = ((lo << 32) ^ hi) & ((1 << 64) - 1)
  trailer = (t_left + t_right) & 0xFFFFFFFF
  out = [0] * 16
  for i in range(8):
    out[i] = (stamp >> (8 * i)) & 0xFF
  for i in range(8):
    out[8 + i] = (trailer >> (8 * i)) & 0xFF
  return out


def expected_seam(buf_len: int, epoch_tag: int) -> tuple[int, int]:
  """Compute the stage-one seam tuple from the byte extent and first-byte tag."""
  return (buf_len // 8, epoch_tag + 1)


def expected_carry(epoch: int, carry_seed: int, seam0: int, seam1: int) -> list[int]:
  """Compute stage-two carry bytes using the replayed stage-one seam pair."""
  merged0 = expected_merge_bytes(epoch + seam0, ((carry_seed + 1) & 0xFF) + seam1)[0]
  out = [(carry_seed + i) & 0xFF for i in range(8)]
  out[0] ^= epoch & 0xFF
  out[0] ^= merged0 & 0xFF
  return out


def run_stage1_text(scenario_path: str) -> str:
  proc = subprocess.run(
    [STAGE1_EXE, scenario_path],
    check=True,
    capture_output=True,
    text=True,
  )
  return proc.stdout.strip()


def run_stage1(scenario_path: str) -> dict:
  return json.loads(run_stage1_text(scenario_path))


def test_qgh_digest_s1() -> None:
  """User-visible digest must mirror the native pipeline for s1."""
  sys.path.insert(0, "/app/environment")
  from harness.run_sim import write_digest  # noqa: PLC0415

  scen = _scenario("s1.json")
  data = _load("s1.json")
  write_digest("/app/output/qgh_digest.json", scen)
  stage1 = run_stage1(scen)
  stage2 = run_stage2(run_stage1_text(scen), scen)
  with open("/app/output/qgh_digest.json", encoding="utf-8") as handle:
    digest = json.load(handle)
  merged8 = stage1["merged"][:8]
  want_stamp = "".join(f"{b:02x}" for b in merged8)
  tail = stage2["carry"][-4:]
  want_tail = "".join(f"{b:02x}" for b in tail)
  assert digest["stamp_area_hex"] == want_stamp
  assert digest["seam_lo"] == int(stage1["seam0"])
  assert digest["seam_hi"] == int(stage1["seam1"])
  assert digest["carry_tail_hex"] == want_tail
  want_carry = expected_carry(
    int(data["epoch"]),
    int(data["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  assert stage2["carry"][0] == want_carry[0]


def run_stage2(stage1_text: str, scenario_path: str) -> dict:
  with tempfile.NamedTemporaryFile(
    mode="w",
    delete=False,
    suffix=".json",
    encoding="utf-8",
  ) as tmp:
    tmp.write(stage1_text)
    tmp_path = tmp.name
  try:
    proc = subprocess.run(
      [STAGE2_EXE, tmp_path, scenario_path],
      check=True,
      capture_output=True,
      text=True,
    )
    return json.loads(proc.stdout.strip())
  finally:
    os.unlink(tmp_path)


def test_qgh_a1() -> None:
  """Stage-one merge stamp bytes for s1 must match the packed min/max contract."""
  scen = _scenario("s1.json")
  data = _load("s1.json")
  got = run_stage1(scen)
  want = expected_merge_bytes(int(data["t_left"]), int(data["t_right"]))
  assert got["merged"][:8] == want[:8]


def test_qgh_a2() -> None:
  """Overlap-heavy markers in s2 still produce the canonical eight-byte stamp prefix."""
  scen = _scenario("s2.json")
  data = _load("s2.json")
  got = run_stage1(scen)
  want = expected_merge_bytes(int(data["t_left"]), int(data["t_right"]))
  assert got["merged"][:8] == want[:8]


def test_qgh_a3() -> None:
  """Signed marker ordering in s7 must still use min/max before the uint32 stamp fold."""
  scen = _scenario("s7.json")
  data = _load("s7.json")
  got = run_stage1(scen)
  want = expected_merge_bytes(int(data["t_left"]), int(data["t_right"]))
  assert got["merged"][:8] == want[:8]


def test_qgh_a4() -> None:
  """Stage-one trailer lane for s2 must store the summed marker pair in little-endian form."""
  scen = _scenario("s2.json")
  data = _load("s2.json")
  got = run_stage1(scen)
  want = expected_merge_bytes(int(data["t_left"]), int(data["t_right"]))
  assert got["merged"][8:16] == want[8:16]


def test_qgh_b1() -> None:
  """Span seam indices for s3 must follow floor(len/8) and epoch byte + 1."""
  scen = _scenario("s3.json")
  data = _load("s3.json")
  got = run_stage1(scen)
  want = expected_seam(int(data["buf_len"]), int(data["epoch_tag"]))
  assert (got["seam0"], got["seam1"]) == want


def test_qgh_b2() -> None:
  """Partial sweep sizing in s4 must still yield the canonical seam tuple."""
  scen = _scenario("s4.json")
  data = _load("s4.json")
  got = run_stage1(scen)
  want = expected_seam(int(data["buf_len"]), int(data["epoch_tag"]))
  assert (got["seam0"], got["seam1"]) == want


def test_qgh_c1() -> None:
  """Carry folding must use the stage-one seam pair as part of the handoff stamp for s5."""
  scen = _scenario("s5.json")
  data = _load("s5.json")
  text = run_stage1_text(scen)
  stage1 = json.loads(text)
  got = run_stage2(text, scen)
  want = expected_carry(
    int(data["epoch"]),
    int(data["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  assert got["carry"] == want


def test_qgh_c2() -> None:
  """Stress s6: carry tail bytes stay aligned while the prefix uses the stage-one handoff."""
  scen = _scenario("s6.json")
  data = _load("s6.json")
  text = run_stage1_text(scen)
  stage1 = json.loads(text)
  got = run_stage2(text, scen)
  want = expected_carry(
    int(data["epoch"]),
    int(data["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  assert got["carry"] == want
  assert got["carry"][7] == (int(data["carry_seed"]) + 7) & 0xFF


def test_qgh_c3() -> None:
  """Carry folding must follow the seam fields present in the stage-one JSON handoff."""
  scen = _scenario("s5.json")
  data = _load("s5.json")
  stage1 = json.loads(run_stage1_text(scen))
  stage1["seam0"] += 2
  stage1["seam1"] += 5
  text = json.dumps(stage1)
  got = run_stage2(text, scen)
  want = expected_carry(
    int(data["epoch"]),
    int(data["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  assert got["carry"] == want


def test_qgh_c4() -> None:
  """Stress s7: carry folding stays tied to the replayed seam pair under signed stamp inputs."""
  scen = _scenario("s7.json")
  data = _load("s7.json")
  text = run_stage1_text(scen)
  stage1 = json.loads(text)
  got = run_stage2(text, scen)
  want = expected_carry(
    int(data["epoch"]),
    int(data["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  assert got["carry"] == want


def test_qgh_c5() -> None:
  """s8 carry folding must match the carry-lane contract for the bundled stress scenario."""
  scen = _scenario("s8.json")
  data = _load("s8.json")
  text = run_stage1_text(scen)
  stage1 = json.loads(text)
  got = run_stage2(text, scen)
  want = expected_carry(
    int(data["epoch"]),
    int(data["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  assert got["carry"] == want


def test_qgh_c6() -> None:
  """s8 carry byte zero must match the contract merge operand, not an over-adjusted variant."""
  scen = _scenario("s8.json")
  data = _load("s8.json")
  text = run_stage1_text(scen)
  stage1 = json.loads(text)
  got = run_stage2(text, scen)
  want = expected_carry(
    int(data["epoch"]),
    int(data["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  wrong_right = (((int(data["carry_seed"]) + 1) & 0xFF) + 1) + int(stage1["seam1"])
  wrong_merged0 = expected_merge_bytes(
    int(data["epoch"]) + int(stage1["seam0"]),
    wrong_right,
  )[0]
  wrong0 = (int(data["carry_seed"]) & 0xFF) ^ (int(data["epoch"]) & 0xFF) ^ wrong_merged0
  assert got["carry"][0] == want[0]
  assert got["carry"][0] != wrong0 & 0xFF


def test_qgh_fresh_scenario_contract() -> None:
  """Unbundled scenario integers must satisfy stamp, seam, and carry contract helpers."""
  body = {
    "t_left": 17,
    "t_right": 29,
    "buf_len": 37,
    "epoch_tag": 8,
    "epoch": 9,
    "carry_seed": 13,
  }
  with tempfile.TemporaryDirectory() as tmpdir:
    scen_path = os.path.join(tmpdir, "fresh.json")
    with open(scen_path, "w", encoding="utf-8") as handle:
      json.dump(body, handle)
    text = run_stage1_text(scen_path)
    stage1 = json.loads(text)
    stage2 = run_stage2(text, scen_path)

  want_merge = expected_merge_bytes(int(body["t_left"]), int(body["t_right"]))
  want_seam = expected_seam(int(body["buf_len"]), int(body["epoch_tag"]))
  want_carry = expected_carry(
    int(body["epoch"]),
    int(body["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  assert stage1["merged"][:8] == want_merge[:8]
  assert stage1["merged"][8:16] == want_merge[8:16]
  assert (stage1["seam0"], stage1["seam1"]) == want_seam
  assert stage2["carry"] == want_carry


def test_qgh_digest_s5() -> None:
  """Digest for s5 must follow the pipeline, not only the s1 scenario shape."""
  sys.path.insert(0, "/app/environment")
  from harness.run_sim import write_digest  # noqa: PLC0415

  scen = _scenario("s5.json")
  data = _load("s5.json")
  write_digest("/app/output/qgh_digest.json", scen)
  stage1 = run_stage1(scen)
  stage2 = run_stage2(run_stage1_text(scen), scen)
  with open("/app/output/qgh_digest.json", encoding="utf-8") as handle:
    digest = json.load(handle)
  want_stamp = "".join(f"{b:02x}" for b in stage1["merged"][:8])
  want_tail = "".join(f"{b:02x}" for b in stage2["carry"][-4:])
  assert digest["stamp_area_hex"] == want_stamp
  assert digest["seam_lo"] == int(stage1["seam0"])
  assert digest["seam_hi"] == int(stage1["seam1"])
  assert digest["carry_tail_hex"] == want_tail
  want_carry = expected_carry(
    int(data["epoch"]),
    int(data["carry_seed"]),
    int(stage1["seam0"]),
    int(stage1["seam1"]),
  )
  assert stage2["carry"] == want_carry


def _synthetic_scenario(seed: int) -> dict:
  """Deterministic scenario body outside the bundled fixture set."""
  return {
    "t_left": -40 + (seed * 17) % 80,
    "t_right": 5 + (seed * 23) % 90,
    "buf_len": 8 + (seed * 11) % 48,
    "epoch_tag": 1 + (seed * 7) % 240,
    "carry_seed": (seed * 13) % 251,
    "epoch": 2 + (seed * 19) % 400,
  }


def _write_temp_scenario(body: dict) -> str:
  fd, path = tempfile.mkstemp(suffix=".json", prefix="qgh_dyn_")
  os.close(fd)
  with open(path, "w", encoding="utf-8") as handle:
    json.dump(body, handle)
  return path


@pytest.mark.parametrize("seed", [101, 202, 303, 404])
def test_qgh_generated_scenarios_full_pipeline(seed: int) -> None:
  """Synthetic scenarios exercise stamp, seam, and carry without bundled JSON."""
  body = _synthetic_scenario(seed)
  path = _write_temp_scenario(body)
  try:
    stage1 = run_stage1(path)
    want_merge = expected_merge_bytes(int(body["t_left"]), int(body["t_right"]))
    assert stage1["merged"][:8] == want_merge[:8]
    want_seam = expected_seam(int(body["buf_len"]), int(body["epoch_tag"]))
    assert (stage1["seam0"], stage1["seam1"]) == want_seam
    text = json.dumps(stage1)
    stage2 = run_stage2(text, path)
    want_carry = expected_carry(
      int(body["epoch"]),
      int(body["carry_seed"]),
      int(stage1["seam0"]),
      int(stage1["seam1"]),
    )
    assert stage2["carry"] == want_carry
  finally:
    os.unlink(path)


def test_qgh_perturbation_changes_merge_stamp() -> None:
  """Pipeline output must track scenario inputs rather than hardcoded fixture answers."""
  base = _synthetic_scenario(909)
  path = _write_temp_scenario(base)
  try:
    before = run_stage1(path)
    perturbed = dict(base)
    perturbed["t_left"] = int(base["t_left"]) + 17
    os.unlink(path)
    path = _write_temp_scenario(perturbed)
    after = run_stage1(path)
    assert after["merged"][:8] != before["merged"][:8]
  finally:
    if os.path.exists(path):
      os.unlink(path)


def test_qgh_tampered_seam_propagates_to_carry() -> None:
  """Carry folding tracks seam fields supplied through the stage-one JSON artifact."""
  body = _synthetic_scenario(515)
  path = _write_temp_scenario(body)
  try:
    stage1 = json.loads(run_stage1_text(path))
    stage1["seam0"] += 3
    stage1["seam1"] += 7
    got = run_stage2(json.dumps(stage1), path)
    want = expected_carry(
      int(body["epoch"]),
      int(body["carry_seed"]),
      int(stage1["seam0"]),
      int(stage1["seam1"]),
    )
    assert got["carry"] == want
  finally:
    os.unlink(path)

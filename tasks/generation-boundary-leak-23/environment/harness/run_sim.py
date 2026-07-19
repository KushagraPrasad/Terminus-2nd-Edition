import json
import os
import subprocess
import tempfile


def _repo_root() -> str:
    return "/app/environment"


def run_pipeline(scenario_path: str) -> dict:
  """Run native stages and return parsed JSON fragments."""
  r1 = subprocess.run(
    ["/app/build/genstage1", scenario_path],
    check=True,
    capture_output=True,
    text=True,
  )
  stage1_text = r1.stdout.strip()
  with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json", encoding="utf-8") as tmp:
    tmp.write(stage1_text)
    tmp_path = tmp.name
  try:
    r2 = subprocess.run(
      ["/app/build/genstage2", tmp_path, scenario_path],
      check=True,
      capture_output=True,
      text=True,
    )
    stage2_text = r2.stdout.strip()
  finally:
    try:
      os.unlink(tmp_path)
    except OSError:
      pass
  return {"stage1": json.loads(stage1_text), "stage2": json.loads(stage2_text)}


def write_digest(out_path: str, scenario_path: str) -> None:
  os.makedirs(os.path.dirname(out_path), exist_ok=True)
  parts = run_pipeline(scenario_path)
  merged = parts["stage1"]["merged"]
  stamp_area = merged[:8]
  seam0 = int(parts["stage1"]["seam0"])
  seam1 = int(parts["stage1"]["seam1"])
  carry = parts["stage2"]["carry"]
  carry_tail = carry[-4:]
  hex8 = "".join(f"{b:02x}" for b in stamp_area)
  tail_hex = "".join(f"{b:02x}" for b in carry_tail)
  payload = {
    "stamp_area_hex": hex8,
    "seam_lo": seam0,
    "seam_hi": seam1,
    "carry_tail_hex": tail_hex,
  }
  with open(out_path, "w", encoding="utf-8") as handle:
    json.dump(payload, handle)
    handle.write("\n")


if __name__ == "__main__":
  scen = os.path.join(_repo_root(), "harness", "scenarios", "s1.json")
  write_digest("/app/output/qgh_digest.json", scen)

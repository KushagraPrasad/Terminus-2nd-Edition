import json

data = {
  "first_look_result": {
    "reviewer_or_model": "Antigravity",
    "date": "2026-07-07",
    "packet_hash": "c32fbdaa7059009c934d6138a5ffe09b28289982e2416772c44a2de65dff8c36",
    "subsystem_identified": True,
    "source_fix_understood": True,
    "verifier_understood": True,
    "static_output_rejected": True,
    "rational_plan": True,
    "failure_reason": None,
    "decision": "PASS"
  }
}

with open("/tmp/wal-segment-pruner-drift-first-look-result.json", "w") as f:
    json.dump(data, f, indent=2)

print("Created first look result packet successfully!")

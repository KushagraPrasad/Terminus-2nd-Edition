import sys
sys.path.append("scripts")
from reviewer_simulation import _task_surfaces
from pathlib import Path

s1 = _task_surfaces(Path("tasks/tls-session-cache-divergence"))
s2 = _task_surfaces(Path("tasks/wal-segment-pruner-drift"))

import re
inst = s1["instruction"]
paras = [p.strip() for p in re.split(r"\n\s*\n", inst) if p.strip()]
print("Paragraphs Count:", len(paras))
for i, p in enumerate(paras):
    print(f"--- Paragraph {i+1} ---")
    print(p[:60] + "...")



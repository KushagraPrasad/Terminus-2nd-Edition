from pathlib import Path
import re
import sys

# Add scripts directory to path to import post_disclosure_collapse
sys.path.append(str(Path("scripts").resolve()))
from post_disclosure_collapse import visible_contract_paths, FORMULA_RE, read_text

task_dir = Path("tasks/tls-session-cache-divergence")
paths = visible_contract_paths(task_dir)
for p in paths:
    for lineno, line in enumerate(read_text(p).splitlines(), start=1):
        if FORMULA_RE.search(line):
            print(f"{p.name}:{lineno}: {line}")

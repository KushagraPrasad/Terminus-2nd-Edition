import re
from pathlib import Path

FORMULA_RE = re.compile(
    r"("
    r"\b[A-Z][A-Z0-9_]{2,}\b.*(?:=|->|:)"
    r"|(?:==|>=|<=|(?<![:/\w])=(?![=]))"
    r"|(?<=\d)\s*[-+*/]\s*(?=\d)"
    r"|\b(?:max|min|round|ceil|floor)\s*\("
    r"|\b(?:transition|event|rule|invariant|formula)\b"
    r")",
    re.I,
)

def find_matches(path: Path):
    print("MATCHES FOR:", path.name)
    lines = path.read_text(encoding="utf-8").splitlines()
    for lineno, line in enumerate(lines, start=1):
        if len(line.strip()) < 8:
            continue
        m = FORMULA_RE.search(line)
        if m:
            print(f"{lineno}: {line.strip()} | MATCHED: {m.group(0)}")

find_matches(Path("tasks/wal-segment-pruner-drift/instruction.md"))
find_matches(Path("tasks/wal-segment-pruner-drift/environment/docs/db_schema.md"))

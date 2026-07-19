#!/bin/bash
set -euo pipefail
/app/environment/mig_exec --write /tmp/migration_observations.inspect.json
python3 - <<'PY'
import json
from pathlib import Path
p = Path('/tmp/migration_observations.inspect.json')
data = json.loads(p.read_text())
print('runs:', ','.join(run['run_id'] for run in data['runs']))
print('records:', sum(len(run['records']) for run in data['runs']))
PY

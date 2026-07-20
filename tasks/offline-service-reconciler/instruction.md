# Offline fleet state reconciler

An offline fleet management system maintains host state across three evidence sources that can disagree after a partial airgapped sync:

- **Probe cache**: per-host cached probe files under `/app/environment/b6/` (TOML format, one file per host)
- **Signed central registry**: a signed central inventory at `/app/environment/g2/sv_inv.json` (JSON, includes cryptographic signature field per host)
- **Override declarations**: operator-issued role overrides at `/app/environment/f8/op_ov.yaml` (YAML)

After a recent partial sync, some hosts have contradictory role assignments across these three sources. The reconciler resolves these conflicts and produces a canonical output.

## Reconciler Requirements

The reconciler resides under `/app` with the entry point `/app/environment/p4/main.go`. Implementation fixes are made directly in the Go module sources under `/app/environment/` to satisfy the following requirements:

1. The three evidence sources are read.
2. The canonical host inventory is written to `/app/output/host_inventory.json`.
3. A run summary is written to `/app/output/run_report.json`.
4. Both output files contain a matching `pack_digest` field (see below).
5. Running the reconciler multiple times produces identical output artifacts.

## Authority and digest rules

The rules for resolving conflicts between the three evidence sources are defined in:

- `/app/environment/d5/rc_rules.md` — authority ordering and trust anchor semantics
- `/app/environment/d5/pk_rules.md` — `pack_digest` formula specification

## Host Profiles

The four host profiles verified are:
- `nvme`
- `luks`
- `zfs`
- `legacy`

## Output schema

For `/app/output/host_inventory.json`:
```json
{
  "hosts": [
    {"id": "string", "role": "string", "profile": "string"}
  ],
  "pack_digest": "string",
  "generated_at": "string"
}
```

For `/app/output/run_report.json`:
```json
{
  "run_id": "string",
  "hosts_processed": "integer",
  "conflicts_resolved": "integer",
  "pack_digest": "string",
  "status": "string"
}
```

The `hosts_processed` field in `/app/output/run_report.json` records the total count of hosts processed by the reconciler during the execution (4 in this environment). The `conflicts_resolved` field logs the count of unresolved profile conflicts that were resolved.

The `pack_digest` in both files must be identical and computed per `/app/environment/d5/pk_rules.md`. The resulting `pack_digest` is a 64-character SHA-256 hex string.

## Verification

The reconciler is executed via:
```bash
go run /app/environment/p4/main.go --all-profiles
```

Verification is performed via the pytest suite:
```bash
cd /app && python3 -m pytest -v
```

Files under `/app/tests/`, `/app/environment/d5/`, `/app/environment/b6/`, `/app/environment/g2/`, or `/app/environment/f8/` must remain unmodified. Hardcoded output artifacts are not permitted.

A health check subcommand is available (`go run /app/environment/p4/main.go --health`) but all profile tests must pass.

# Authority Reconciliation Rules

When reconciling host assignments, the reconciler must check the status of each host across all sources.

1. By default, the cached probe values in `environment/b6/` represent the runtime state of a host.
2. If a host has an entry in the signed central inventory (`environment/g2/sv_inv.json`) and the field `sig_anchor` is set to `true`, that role assignment takes precedence and overrides the cached probe data.
3. If `sig_anchor` is `false` or missing, the central inventory does not override the probe cache.

## Expected Reconciliation Outcomes

For the default fleet profile, the expected resolved roles are:
- `host_a`: maintains `compute` role (probe cache active)
- `host_b`: overridden to `storage` role (sig_anchor active)
- `host_c`: overridden to `backup` role (sig_anchor active)
- `host_d`: merges operator override to `management-console` role

Upon successful execution, the run report status must be set to `SUCCESS`.

## Verifier Note

The automated verifier parses test files and uses libraries such as `glob` and `tomllib` to verify that the final reconciled artifacts match the expected roles.

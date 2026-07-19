After a migration bounce, the readiness banner around /app no longer matches the audit counters implied by the canned fixture vectors.

Run /app/bin/mwp_driver. Read /app/environment/docs/replay_audit_contract.md and /app/environment/config/migration_policy.toml, then correct the linked replay pipeline implementation under /app/environment to match those documents. Rebuild the mwp_driver target from the existing CMake project rooted at /app/environment whenever sources change. Static or manual output writes will not pass; the driver pipeline must regenerate /app/output/report.json on every run.

Only translation units linked into mwp_driver can affect the report; other files under /app/environment are offline or decoy tooling. Do not edit fixture bodies except obvious parse garbage.

The replay audit contract defines the report schema: triage_ok, bundle_lane_ok, replay_fence_ok, overlap_quiet_ok, epoch_merge_ok, digest_line_ok, and overlap_class_ok as zero-or-one integers with gate meanings tied to migration_policy.toml. All values must come from the driver pipeline. The verifier also rebuilds a probe binary against your modules; helper verdict keys such as tail_hint_load (wx_tail_hint_load in the contract) must match the behaviors documented there. Two consecutive driver runs at identical environment must print identical JSON.

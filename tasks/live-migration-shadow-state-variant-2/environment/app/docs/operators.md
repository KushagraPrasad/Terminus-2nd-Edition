# Operator Notes

The local harness uses deterministic fixture rows so recovery behavior can be inspected without external services. Use `app/tools/inspect.sh` for a quick summary when developing locally. The summary is not a verifier output; the JSON report is the public artifact.

The codebase is split into input reading, operation sequencing, core row grouping, local storage records, and report emission. These layers intentionally keep enough detail for diagnosis without relying on a live cluster.

Verifier logging may use pytest with the `--ctrf` option outside the product runner. That flag is only for verifier records and does not change the report contract.

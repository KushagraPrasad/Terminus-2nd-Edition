# Pack Digest Formula Specification

The `pack_digest` is a SHA-256 hash computed to verify that the output inventory aligns with the central inventory:

1. Let `R` be the list of reconciled hosts. Sort this list by `host_id` ascending.
2. Serialize `R` as a compact JSON string (no whitespace outside of strings, keys sorted: `host_id`, `profile`, `role`).
3. Let `I` be the raw byte content of the signed inventory file `environment/g2/sv_inv.json`. Compute the SHA-256 hash of `I` (hex format).
4. The final `pack_digest` is `sha256(R_json + "|" + sha256(I))`.

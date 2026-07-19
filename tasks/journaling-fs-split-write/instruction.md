# Journaling FS Split Write Recovery

You are debugging a userspace filesystem daemon (`fs_daemon`) that implements a simple write-ahead log (WAL) for atomic transactions.

The crash recovery must correctly handle split writes on 4KB boundaries.

The secondary checksum tree must be preserved perfectly during rollback.

Recovery must be idempotent (re-running recovery on a recovered state should not alter the state).

The daemon must be able to write new data immediately after recovering without panicking.

The daemon crashes and restarts, it automatically attempts to replay the journal to ensure the filesystem is consistent.

However, during tests mimicking power-failures midway through transaction commits (split writes), the daemon ends up recovering into a corrupted state where subsequent writes either panic or silently corrupt the secondary checksum tree.

The `/app/environment` source code must be fixed to ensure idempotent, bit-perfect file recovery without corrupting the secondary checksum tree or panicking on subsequent writes.

See `/app/environment/docs/format.rst` for the on-disk binary format specifications.

The daemon CLI (located at `/app/environment/fs_daemon`) supports commands like `recover`, `write`, and `check_txn` (e.g. `/app/environment/fs_daemon disk.bin recover`).

The `check_txn` command MUST output the transaction ID as `Last Txn: [id]` without panicking.

The `write` command MUST output `Write complete.` on success.

The verifier will execute these commands and use the standard python `tempfile.NamedTemporaryFile` semantics with `int.to_bytes` in little-endian format to simulate crash failures across isolated test runs which MUST simulate a fresh filesystem block. For testing recovery and rollback side effects on the secondary checksum tree, physical block 12 (corresponding to logical block 1) may be simulated.

The verifier will use pytest with the `--json-ctrf` flag to output a test report to `/logs/verifier/ctrf.json` asserting split write recovery idempotency.

You can compile the daemon using `make` in the `/app/environment` directory.

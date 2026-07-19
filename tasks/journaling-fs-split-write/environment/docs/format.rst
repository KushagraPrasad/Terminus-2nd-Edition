# Binary Format

- Block Size: 4096 bytes
- Block 0: Superblock
- Block 1: Checksum Tree. Each 4 bytes represents a checksum for logical blocks 0, 1, 2...
- Blocks 2-10: Journal area.
- Blocks 11+: Data area.

## Journal Entries
Each transaction starts with a header, formatted as little-endian `<IIII`:
- `txn_id`: uint32
- `num_blocks`: uint32
- `checksum`: uint32
- `magic`: uint32 (0xDEADBEEF)

Transactions must have strictly monotonically increasing `txn_id` values.
A typical disk image may be 20 blocks in total size.
The checksum tree stores a 16 byte checksum region for blocks.

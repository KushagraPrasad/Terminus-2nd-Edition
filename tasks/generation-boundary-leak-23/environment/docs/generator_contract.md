# Two-stage generator contract

Scenario JSON records use integer `t_left`, `t_right`, `buf_len`, `epoch_tag`,
`epoch`, and `carry_seed`. Stage one emits `merged` bytes plus integer `seam0`
and `seam1`. Stage two emits `carry` bytes.

## Stamp lane (`fx_merge_z`)

Let `raw_left` and `raw_right` be the signed scenario markers. Form
`lo = uint32(min(raw_left, raw_right))` and `hi = uint32(max(raw_left, raw_right))`,
then `stamp = (uint64(lo) << 32) ^ uint64(hi)`. Write `stamp` as eight
little-endian bytes at offset 0. Write `uint64(raw_left + raw_right)` as eight
little-endian bytes at offset 8 (the trailer lane).

## Seam lane (`op_span_y`)

Given a byte buffer used for generation tagging, return
`(floor(byte_count / 8), first_byte_value + 1)`.

## Carry lane (`reseq_q`)

Seed eight carry bytes as `(carry_seed + i) & 0xFF` for `i` in `0..7`. Xor the
low eight bits of `epoch` into byte zero. Let `second_seed_byte` be the
carry-span byte at offset 1 after seeding. Form the right merge operand as
`second_seed_byte + stage1.seam1`. Xor the first byte of
`fx_merge_z(epoch + stage1.seam0, right_operand)` into byte zero. Stage two
reads `seam0` and `seam1` from the stage-one JSON artifact supplied on its
command line.

## Digest writer

`/app/output/qgh_digest.json` is produced by the normal pipeline: run stage
one, pass its JSON to stage two, then record `stamp_area_hex` (first eight
merged bytes as hex), `seam_lo`, `seam_hi`, and `carry_tail_hex` (last four
carry bytes as hex). Hand-written digests are not authoritative.

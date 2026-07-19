# Journal replay audit contract (environment reference)

Lane timing requires span length at least 12 bytes, window at least 90 ms, and unsigned byte sum congruent to 3 modulo 7.

Fold row precedence compares rank bytes first; equal rank uses serial byte comparison, not lexicographic tail ordering.

WAL compact replay must preserve monotonic stamp order. Generation persistence under `/app/var/journal/` must round-trip the final stamp for restart lanes.

Gate mux ordering runs the side callback before the gate callback when the combine helper is wired correctly.

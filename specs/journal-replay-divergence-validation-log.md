## Per-task authoring metrics

- count of scripts/run_static_checks.py FAIL exits before first PASS: 0
- count of scripts/run_static_checks.py WARN-only exits before approval: 5
- count of scripts/collapse_check.py FAIL exits before first PASS: 0
- count of dirty-flag triggers (scripts/approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 340.95s
- wall-clock time from first Step 2b PASS to scripts/approve_task.py exit 0: 3900.74s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Step 3b — WARN classification (ACCEPT WITH NOTES)

Date: 2026-05-13. Documentation-only addendum for paper review; no change to `tasks/journal-replay-divergence/` tree or Step 2b checksum.

### `run_static_checks` / instruction length (preferred 1–3 paragraphs)

**ACCEPT WITH NOTES.** The instruction is longer than the stylistic preference because reviewers required explicit alignment with tests: `JOURNAL_AUDIT_SCENARIO` profiles, the ninety-millisecond lane floor, the modulo-seven unsigned byte-sum residue (≡ 3 mod 7), the six JSON boolean keys, and the exact verifier build commands (`cmake`, `pytest`, `--ctrf`). Shortening would risk re-hiding contracts the task is meant to make visible.

### `collapse_check.py` WARNs (6 signals; exit still non-FAIL)

**RC1 (oracle simplification, net negative delta).** **ACCEPT WITH NOTES.** Small net line reduction on two of three oracle targets reflects localized cleanup while preserving behavior; it is not used as evidence of trivializing the fix.

**RC2 (oracle predictability).** **ACCEPT WITH NOTES.** Two targets are partially predictable from subsystem vocabulary (`gate`, `fold` / `persist`); `runtime/src/mux_slice.cpp` remains the less predictable limb. Multi-file coupling, lane timing, and fold arbitration still require reading code and running the binary, not keyword matching alone.

**RC7 (oracle triviality, borderline LOC band).** **ACCEPT WITH NOTES.** ~43 non-boilerplate LOC across three targets sits in the borderline band by automation, but the task’s hardness is in cross-module diagnosis (mux vs WAL vs lane gate) and frozen-vector consistency, not in raw patch size.

**CR1 (symbol table compliance).** **ACCEPT WITH NOTES.** Additional helpers appear on the touched paths beyond the minimal `symbol_table` list; `construction_manifest.json` documents flipping points and decoys. Further “symbol thinning” would trade audit realism for a quieter heuristic.

**CR7 (grep resistance).** **ACCEPT WITH NOTES.** Instruction uses audit-adjacent words that overlap tokens in `replay_gate.cpp` (`audit_profile`, `run_audit_emit`). That overlap is intentional for scenario naming and actionability; it does not yield a complete patch recipe because lane/mod rules and mux/fold logic are still enforced by tests and code.

**GX3 (oracle edit distance borderline).** **ACCEPT WITH NOTES.** Real edit distance is borderline in aggregate but distributed as focused patches across three files; not a no-op rewrite and not bulk inflation.

---

## Human grading rubrics (one criterion per line)

Rubric lines below are for reviewer grading of agent *solutions* (not for zipping into the task package).

1. **Verifiable outcome:** After the prescribed build and `pytest` on `/tests/test_outputs.py`, all tests pass and the Harbor-style reward matches expectation (binary-backed, not hand JSON).
2. **`/app/output/report.json` integrity:** The six boolean keys exist and match values emitted by the rebuilt `/app/bin/journal_run` binary, not pasted or fabricated JSON.
3. **Default path / closure:** With default `JOURNAL_AUDIT_SCENARIO`, `closure_bits_ok` and the other booleans match the frozen vectors implied by the environment sources and instruction contract.
4. **Lane timing floor:** The shared lane gate rejects windows strictly under ninety milliseconds wherever the instruction and tests apply that rule.
5. **Lane byte-sum residue:** Lane spans satisfy the unsigned byte-sum congruent to three modulo seven where required by the instruction and tests.
6. **Profile 1 (narrow timer):** With `JOURNAL_AUDIT_SCENARIO=1`, `pair_align_ok` is false and the other five booleans are true on a correct repair (computed, not hardcoded).
7. **Profile 2 (mixed-rank):** With `JOURNAL_AUDIT_SCENARIO=2`, all six booleans match that profile’s shipped frozen vectors under rank-primary / serial-tiebreaker fold rules and the shared lane gate (some keys may be false).
8. **Profile 3 (asymmetric fold):** With `JOURNAL_AUDIT_SCENARIO=3`, all six booleans match that profile’s shipped vectors (short lane may leave `pair_align_ok` false; fold pair uses asymmetric ranks).
9. **Deterministic repeatability:** Two consecutive runs with identical environment variables produce identical JSON output (no nondeterministic drift).
10. **Scope discipline:** All substantive fixes live under `/app/environment` (staged tree) and rebuild uses the existing CMake layout as specified (`cmake -S /app/environment -B /app/build`, `cmake --build /app/build -j2`).
11. **Subsystem coupling:** Changes coherently reconcile `ops/` (replay/gate), `persist/` (WAL fold), and `runtime/` (mux slice) so the report reflects one consistent story across subsystems.
12. **No test cheating:** The agent does not bypass the build, skip `pytest`, or satisfy checks by editing only test files or static JSON artifacts outside the binary pipeline.
13. **Actionability:** A competent engineer can follow the instruction’s commands and environment hints without guessing hidden install steps beyond what the task provides.

## Per-task authoring metrics

- count of scripts/run_static_checks.py FAIL exits before first PASS: 0
- count of scripts/run_static_checks.py WARN-only exits before approval: 3
- count of scripts/collapse_check.py FAIL exits before first PASS: 0
- count of dirty-flag triggers (scripts/approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 16.44s
- wall-clock time from first Step 2b PASS to scripts/approve_task.py exit 0: 287.53s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of scripts/run_static_checks.py FAIL exits before first PASS: 0
- count of scripts/run_static_checks.py WARN-only exits before approval: 4
- count of scripts/collapse_check.py FAIL exits before first PASS: 0
- count of dirty-flag triggers (scripts/approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 16.44s
- wall-clock time from first Step 2b PASS to scripts/approve_task.py exit 0: 3499.45s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of scripts/run_static_checks.py FAIL exits before first PASS: 0
- count of scripts/run_static_checks.py WARN-only exits before approval: 5
- count of scripts/collapse_check.py FAIL exits before first PASS: 0
- count of dirty-flag triggers (scripts/approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 16.44s
- wall-clock time from first Step 2b PASS to scripts/approve_task.py exit 0: 38719.70s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

## Per-task authoring metrics

- count of scripts/run_static_checks.py FAIL exits before first PASS: 0
- count of scripts/run_static_checks.py WARN-only exits before approval: 5
- count of scripts/collapse_check.py FAIL exits before first PASS: 0
- count of dirty-flag triggers (scripts/approve_task.py refused due to checksum mismatch): 0
- wall-clock time from first preflight to first preflight PASS: 16.44s
- wall-clock time from first Step 2b PASS to scripts/approve_task.py exit 0: 88071.12s
- list of CNI references that fired during the authoring: []
- whether the spec's Initial Draft Commitments matched the final file set (draft_commitments_diff): null

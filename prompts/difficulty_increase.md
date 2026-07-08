You are fixing an existing task that was rejected or is at risk of rejection because
the platform difficulty label landed TRIVIAL, EASY, or MEDIUM, or the worst-model
pass rate on GPT-5.5 + Claude Opus 4.8 exceeded 20%.

Task directory : tasks/<task-name>
Spec file      : specs/<task-name>.md

Do NOT reword instruction.md to sound harder. Do NOT hide requirements.
Do NOT add cosmetic padding. Wording never affects model pass rate.

If this prompt does not bring the task to legitimate HARD after one full pass,
stop patching and use `prompts/difficulty_redesign.md` instead.

---

## What this prompt fixes (and what it does not)

**Fixes (most common easy-task causes):**
- Instruction leaks answer keys, patch locations, or recipes (GX9/GX10/A24)
- Tests reimplement the algorithm or load it from `environment/` (Patterns 1–4)
- Single-frontier patch (one file / one function fixes everything)
- Missing cross-file, rerun, or false-green verifier layers

**Does NOT fix (stop here → `prompts/difficulty_redesign.md`):**
- Core idea collapses to transcription after honest disclosure (post-disclosure collapse)
- Oracle fix is <30 LOC of real semantic work and concept is inherently simple (RC7/GX3)
- Requirement-to-file map is 1:1 obvious checklist
- Grep on instruction nouns lands directly on the buggy block
- Adding more bugs, obfuscation, or "unidentifiable" defects without redesigning topology

---

## FORBIDDEN (never do these to increase difficulty)

- Add random or "unidentifiable" bugs — agents grep and pattern-match; opaque bugs cause
  instruction-comprehension failures (rated EASY), not engineering hardness
- Hide requirements, use undefined jargon, or polarity contradictions in instruction
- Obfuscate prose, coin metaphors with no env anchor (`in-process lane`, `materialize hop`)
- Pad oracle with cosmetic comment/whitespace edits to inflate LOC (GX2/GX3 gaming)
- Add decoy files, rename symbols only, or strip tested requirements from instruction
- Make tests chain-dependent on one exact oracle technique (causes 0/10, not HARD)

Hard tasks are hard because the **work** is hard — discovery, cross-component invariants,
stateful reasoning — not because bugs are hard to see.

---

## STEP 1A — Run diagnostic tools

```bash
python3 scripts/hard_difficulty_predictor.py tasks/<task-name> --strict --json
python3 scripts/collapse_check.py tasks/<task-name>
python3 scripts/post_disclosure_collapse.py tasks/<task-name>
python3 scripts/instruction_audit.py tasks/<task-name>
```

For milestone tasks, also read every `steps/milestone_N/instruction.md` and
`steps/milestone_N/tests/test_mN.py`.

Read every line. Note `predicted_worst_model_pass_rate`, `failure_mode_count`,
`advanced_hardness_categories`, RC6/GX verdicts, and every FAIL/WARN.

A predictor score of ≤ 20% does NOT mean the task is hard on the platform.
Always proceed through Step 1B–1E regardless of score.

---

## STEP 1B — Audit instruction.md for leaks (BLOCKING)

Read all instruction files (`instruction.md` or `steps/milestone_N/instruction.md`).
Check all seven:

**A — Does it name the exact file, function, or line to fix?**
If YES → remove it. Give symptoms only, not patch location.

**B — Does it contain a scenario→field→expected answer table?**
If YES → replace with behavioral description. The table is the answer key (GX9).

**C — Does it describe the algorithm step by step (recipe)?**
If YES → rewrite as observable outcome only.

**D — Does it over-specify the broken subsystem by name?**
If YES → broaden to symptom description.

**E — Does it enumerate test triples (scenario + field + value) the verifier asserts?**
If YES → describe observations; let agents derive values from behavior (GX9).

**F — Does it name both polarities of a binary field for one scenario?**
(e.g. "allow … ending on deny" while tests assert one polarity) → rewrite (GX10).

**G — Does it use coined multi-word phrases with no word appearing in env code/paths?**
If YES → replace with vocabulary from the codebase (A24 undefined metaphor jargon).

Fix all YES answers before Step 1C.

---

## STEP 1C — Audit test file for answer-key patterns (BLOCKING)

Read `tests/test_outputs.py` and every `steps/milestone_N/tests/test_mN.py`.
Find and fix EVERY pattern below. Do not stop after finding one.

### Pattern 1 — Full algorithm reimplemented as helpers
Functions like `_expected_report`, `_compute_digest`, `_build_canonical`,
`_calculate_result` that produce the expected output by reimplementing the
source logic. Used in assertions like `assert report == _expected_report(matrix)`.

### Pattern 2 — Sub-algorithm reimplemented as helpers
Even one sub-algorithm helper is enough for an agent to solve that part:
- authority selection: `_leading_authority_id`, `_choose_authority`, `_pick_winner`
- lineage construction: `_build_lineage`, `_lineage_parts`, `_lineage_digest`
- stat merging: `_merge_stats`, `_apply_bias`, `_merged_stats`
- SQL normalization: `_normalize_sql`, `_canonical_sql`, `_normalize`
- fingerprint/digest: `_fingerprint`, `_compute_hash`

If any of these exist AND are used in assertions → agent reads the helper and
knows exactly how to implement that sub-algorithm.

### Pattern 3 — Algorithm loaded from environment/ via exec or import
```python
exec(path.read_text(), namespace)
FINGERPRINT = namespace["fingerprint"]   # then called in assertions
```
or `from environment.docs import hash_formula; assert x == hash_formula.fn(y)`

`environment/` is solver-visible. Loading a function from there and calling it
in an assertion is identical to reimplementing it in the test file. The agent
reads the environment file, gets the exact implementation, transcribes it.

### Pattern 4 — Module-level algorithm references
```python
HASH_FORMULA = _load_hash_formula()
FINGERPRINT = HASH_FORMULA["fingerprint"]    # called in _assert_contract_digests
MATRIX_DIGEST = HASH_FORMULA["matrix_digest_from_fingerprints"]
```
These are Pattern 3 stored in module-level variables. Same problem.

### Fix for all four patterns

**Remove:**
- All helpers that reimplement any part of the algorithm (Patterns 1 and 2)
- All `exec()`/`import` calls that load algorithm functions from environment/ (Patterns 3 and 4)
- All module-level variables that hold loaded algorithm functions
- All assertions that call any of the above

**Keep:**
- `_run_verifier()` — runs the binary
- `_matrix_override()` — test fixture setup
- `_clone_matrix()` — deep copy utility
- `_grouped()` — grouping utility
- Data-builder helpers: `_alt_matrix()`, `_tie_matrix()`, `_bias_matrix()`, etc.
- `_assert_report_schema()` — schema/ordering/cardinality checks only (no algorithm)
- `_assert_group_stability()` — stability checks only (no algorithm)

**Replace algorithm assertions with these safe patterns:**

Fingerprint is valid hex (does not reveal algorithm):
```python
assert len(row["fingerprint"]) == 64
assert all(c in "0123456789abcdef" for c in row["fingerprint"])
```

Fingerprint changes when input changes (sensitivity, does not reveal algorithm):
```python
with _matrix_override(alt_matrix):
    alt_report = _run_verifier()
assert alt_report["runs"][0]["fingerprint"] != report["runs"][0]["fingerprint"]
```

Fingerprint is case-sensitive lowercase (negative check, does not reveal algorithm):
```python
assert row["fingerprint"] == row["fingerprint"].lower()
```

Authority selection behavioral check (does not reveal algorithm — use a fixture
where the answer is unambiguous and hardcode the expected authority_id):
```python
# In _tie_matrix, m1 < m2 lexicographically, so authority must be m1
for row in report["runs"]:
    assert row["lineage_digest"].startswith("m1::")
```

Matrix digest changes with different input (does not reveal algorithm):
```python
assert alt_report["summary"]["matrix_digest"] != report["summary"]["matrix_digest"]
```

Rerun stability (does not reveal algorithm):
```python
first = OUTPUT.read_bytes()
OUTPUT.unlink()
_run_verifier()
assert OUTPUT.read_bytes() == first
```

### After Fix: single-frontier check

Ask: can the agent fix this by editing ONE file, ONE function, or ONE constant
and have all tests pass?
If YES → add a second required fix location so the agent must coordinate
changes across ≥ 2 files to pass all tests.

### After Fix: verify oracle and NOP

```bash
python3 scripts/harbor_gate.py tasks/<task-name> --oracle
python3 scripts/harbor_gate.py tasks/<task-name> --nop
```

If oracle fails → fix `solution/solve.sh` to implement the algorithm correctly.
If NOP passes → property checks are too weak, strengthen them.

---

## STEP 1D — Audit environment and oracle for collapse (BLOCKING)

Read `environment/` and `solution/solve.sh` (and milestone `solveN.sh` files).

Check:
- **Grep-collapse:** do instruction nouns match code keys/helpers exactly?
  (`validate`, `extract`, `canon`, phase names) → rename or redistribute logic
- **Pre-factored helpers:** do helper names mirror prompt bullets?
  → task is stub-completion, not hard debugging
- **Small declarative cluster:** is the real fix one tiny table/config + test fan-out?
- **Oracle locality:** is the fix mostly `cat > file <<'EOF'` or tiny `sed` on obvious sites?
  If oracle semantic delta < 30 LOC → concept too simple; escalate to redesign
- **Flipping-point:** reverting one fix location should not flip a majority of tests;
  distribute fixes across ≥ 3 coupled locations when possible

---

## STEP 1E — Residual hardness (five axes)

After Steps 1B–1D, answer honestly for each axis (all must pass for HARD):

1. **Discover** — must agent infer/design something not in instruction alone?
2. **Synthesize** — does answer span multiple interacting systems/artifacts?
3. **Diagnose** — symptoms only, not recipe following?
4. **Navigate coupling** — do local fixes break distant invariants?
5. **Reason beyond training** — not textbook pattern-matching?

**Fatal question:** after honest disclosure, what nontrivial reasoning remains?
If "mostly transcription / one obvious patch" → STOP. Use `prompts/difficulty_redesign.md`.

---

## STEP 2 — Apply structural fixes

Run Step 2 when ANY of these is true (not only when predictor > 20%):
- Platform label was TRIVIAL, EASY, or MEDIUM
- Step 1E residual hardness fails any axis
- Single-frontier check in 1C required a second fix location
- `post_disclosure_collapse.py` or collapse_check WARN/FAIL on structural signals

Work Priority 1 → 6. Re-run predictor and collapse_check after each meaningful change.

### Priority 1 — false_green_intermediate_states
Add a test that passes on schema/field checks but fails on a deeper cross-file
invariant that a partial fix violates.

### Priority 2 — stateful_multi_step_dependencies
Add rerun test: run binary → save bytes → delete output → run again → assert identical.

### Priority 3 — cross_file_cross_format_invariants
Add `environment/docs/<contract>.md` with a formal rule. Add a verifier test
that asserts the output satisfies it without calling any function from that file.

### Priority 4 — buried_local_constraints
Add a config file under `environment/` with a constraint overriding the obvious
interpretation. Do NOT name it in instruction.md. Add a verifier assertion.

### Priority 5 — deceptive_but_valid_local_evidence
Add plausible stale artifact; instruction describes symptoms that contradict it.
Agent must experiment to find authoritative source.

### Priority 6 — rollback_recovery_requirements
Add test that fix must preserve checkpoint/audit/rerun state; partial fix corrupts it.

Stop Step 2 when:
- collapse_check PASS with 0 FAIL
- oracle 1.0 and NOP 0.0
- ≥ 2 coupled fix locations with independent test subsets
- predictor ≤ 20% (Python) or structural axes all pass

If still structurally trivial after Priority 1–6 → `prompts/difficulty_redesign.md`.

---

## STEP 3 — Update the spec

In `specs/<task-name>.md`:

1. Add every new mechanism to `difficulty_mechanism_plan` with `why_model_misses_it`
   and `fairness_guardrail`.

2. Update `calibration_plan`:
```yaml
calibration_plan:
  hard_max_pct: 20
  too_easy_threshold_pct: 80
  basis: Part E worst-model accuracy on platform (GPT-5.5 + Claude Opus 4.8, Jun 12 2026)
  shortcut_audit: >
    read test helpers and transcribe → all algorithm helpers removed
    load env file via exec and transcribe → exec pattern removed
    static JSON output → fails verifier rerun
    patch one file only → cross-file invariant fails
  ablation_plan: >
    Remove each mechanism one at a time and confirm difficulty drops.
```

3. Confirm `failure_mode_count` ≥ 3 and ≥ 1 advanced hardness category.

---

## STEP 4 — Verify predictor

```bash
python3 scripts/hard_difficulty_predictor.py tasks/<task-name> --strict --json
```
Python tasks: `predicted_worst_model_pass_rate ≤ 20%`.
Non-Python: predictor is advisory; structural axes and collapse_check matter more.

---

## STEP 5 — Run all gates

```bash
python3 scripts/collapse_check.py tasks/<task-name>
python3 scripts/actionability_check.py tasks/<task-name> --strict
python3 scripts/no_hidden_contracts.py tasks/<task-name> --strict
python3 scripts/spec_test_alignment.py tasks/<task-name> --strict
python3 scripts/task_gate.py tasks/<task-name> --strict --report-dir /tmp/tb3-gates --skip-harbor
./scripts/check-task.sh --strict --report-dir /tmp/tb3-gates tasks/<task-name>
python3 scripts/harbor_gate.py tasks/<task-name> --oracle --nop
```

All must PASS. oracle = 1.0, NOP = 0.0.

Refresh `.step2b-checksum` via `check-task.sh` before resubmitting.

---

## STEP 6 — Report

```
DIFFICULTY INCREASE REPORT — tasks/<task-name>

Step 1B (instruction leaks):
  Patch location named   : YES→fixed / NO
  Answer table           : YES→fixed / NO
  Algorithm recipe       : YES→fixed / NO
  Subsystem over-named   : YES→fixed / NO
  GX9 answer recital     : YES→fixed / NO
  GX10 polarity clash    : YES→fixed / NO
  Undefined metaphor     : YES→fixed / NO

Step 1C (test file):
  Pattern 1 full reimpl  : YES→fixed / NO  — removed: <function names>
  Pattern 2 sub-algo     : YES→fixed / NO  — removed: <function names>
  Pattern 3 exec/import  : YES→fixed / NO  — removed: <variable names>
  Pattern 4 module-level : YES→fixed / NO  — removed: <variable names>
  Single-frontier check  : PASS / FIXED

Step 1D (env/oracle):
  Grep-collapse          : PASS / FIXED
  Pre-factored helpers   : PASS / FIXED
  Oracle semantic LOC    : <N> (≥30 required; ≥80 comfortable)

Step 1E (five axes):      ALL PASS / FAIL → redesign

Predictor before : <X>%
Predictor after  : <Y>%

Mechanisms added : <name> : <why>

collapse_check      : PASS/FAIL
actionability       : PASS/FAIL
no_hidden_contracts : PASS/FAIL
spec_test_alignment : PASS/FAIL
task_gate           : PASS/FAIL
check-task.sh       : PASS/FAIL — checksum refreshed: YES/NO
harbor oracle       : <mean>
harbor NOP          : <mean>

Escalate to difficulty_redesign.md : YES / NO
Step 2b complete : YES/NO
```

---

## STEP 7 — If platform is still EASY after resubmit

Do NOT add more bugs. Run `prompts/difficulty_redesign.md` — that path amends the
spec and redesigns task topology (new coupling, new artifacts, new verifier shape),
not incremental defect injection.

You are redesigning an existing task because `prompts/difficulty_increase.md`
completed without producing legitimate HARD difficulty on the platform
(terminus-claude-opus-4.8 + terminus-gpt5.5), OR because structural collapse
audits show the core idea cannot be hardened by verifier/instruction fixes alone.

Task directory : tasks/<task-name>
Spec file      : specs/<task-name>.md

## STOP doing this

Do NOT:
- Add more bugs, especially "unidentifiable" or random defects
- Obfuscate instruction prose or hide requirements
- Sprinkle decoy files or rename symbols without changing task substance
- Pad oracle LOC cosmetically
- Make tests oracle-only or chain-dependent (causes 0/10, not HARD)

Agents on Opus 4.8 and GPT-5.5 solve by **reading, grepping, and transcribing**.
Opaque bugs do not create HARD — they create EASY (comprehension failure) or
impossible (0/10). HARD requires **coupled reasoning** agents cannot shortcut.

---

## When to use this prompt (triggers)

Use this instead of another `difficulty_increase.md` pass when ANY is true:

1. Platform label stayed TRIVIAL/EASY/MEDIUM after a full difficulty_increase pass
2. Step 1E five-axis check failed (residual work is transcription / one patch)
3. `post_disclosure_collapse.py` WARN/FAIL — formulas map 1:1 to obvious modules
4. Oracle substantive fix < 30 LOC and concept is inherently a knob-fill / table-edit
5. Requirement-to-file map is a linear checklist with no coupling
6. Second `difficulty_increase.md` pass would only add more tests on same trivial core

---

## STEP 1 — Diagnose root cause (read-only)

```bash
python3 scripts/collapse_check.py tasks/<task-name>
python3 scripts/post_disclosure_collapse.py tasks/<task-name>
python3 scripts/hard_difficulty_predictor.py tasks/<task-name> --strict --json
python3 scripts/instruction_audit.py tasks/<task-name>
```

Produce a **Collapse Redesign Report** with:

```
Task: <name>
Platform result: <trivial|easy|medium> — worst model <X>%, best <Y>%

Smallest plausible successful patch:
[one paragraph — if this sounds easy, redesign is required]

Requirement-to-file map:
- [requirement] -> [obvious location]  (flag if mostly 1:1)

Residual hardness after honest disclosure:
[what remains hard — if "little/none", redesign]

Stable collapse signals:
- [RC/GX/CR checks and why]

difficulty_increase.md already tried:
- [list fixes that did not change platform outcome]

Root cause class (pick one primary):
  A) Test/instruction leak (should have been fixed by difficulty_increase — re-audit)
  B) Single-frontier / tiny declarative cluster
  C) Post-disclosure transcription collapse
  D) Wrong task shape (repair when should be constrained_build / formal_reasoning)
  E) Domain too textbook (HMAC, JSON canon, phase table) — needs new mechanism stack
```

If root cause is **A**, return to `difficulty_increase.md` Step 1B–1C only.
For **B–E**, continue below.

---

## STEP 2 — Amend spec (Step 2a), do not patch task files yet

```bash
python3 scripts/validate_loop.py init <task-name>
```

Follow `prompts/step2a_difficulty.md` and `@idea-validation.mdc`.

**Redesign moves that actually increase hardness** (pick ≥2):

| Move | What changes |
|------|----------------|
| **New coupling topology** | Fix in subsystem A must agree with contract in B and state in C |
| **New adversarial layer** | Add buried_local_constraints + false_green + rerun dependency |
| **Shape shift** | e.g. repair → constrained_build with design-search burden |
| **Split flipping-point** | One oracle location → ≥3 locations; each controls distinct test subset |
| **Stateful pipeline** | Output must survive delete-and-rerun; hardcoded JSON fails |
| **Experiment burden** | partial_observability — static read insufficient, must run tool twice |
| **Milestone sequencing** | Later milestone fails if earlier state wrong (2–3 milestones max) |

**Redesign moves that do NOT work:**

| Move | Why |
|------|-----|
| More bugs in same files | Grep finds them; same frontier |
| Harder wording | Wording does not affect pass rate |
| Hidden requirements | Rejected; causes 0/10 or unfair EASY |
| Niche API gates in tests | 0/10, not HARD |
| Larger env file count alone | Padding without coupling |

Update `specs/<task-name>.md`:
- Rewrite `difficulty_mechanism_plan` (≥4 mechanisms, ≥3 `why_model_misses_it`)
- Rewrite `fix_frontier`, `flipping_point_contract`, `symbol_table`
- Update `calibration_plan.ablation_plan` — each mechanism must independently matter
- Record `reference_pattern` if a promoted reference applies

```bash
python3 scripts/validate_loop.py record <task-name> --strict --evidence /tmp/<task-name>-validation-evidence.json
python3 scripts/lint_spec.py specs/<task-name>.md --strict
python3 scripts/spec_satisfiability.py specs/<task-name>.md --strict
```

Do not edit `tasks/<task-name>/` until spec gates pass.

---

## STEP 3 — Rebuild task from amended spec

Follow `prompts/Step2b.md` with the new spec as source of truth.

Construction checklist for HARD-by-design:
- ≥ 3 coupled fix locations (flipping_point_contract)
- Oracle semantic delta ≥ 30 LOC real work (target ≥ 80)
- Instruction: symptoms + public contract; no answer recital (GX9), no polarity clash (GX10)
- Tests: property/metamorphic/rerun checks; no algorithm helpers (Patterns 1–4)
- Verifier punishes partial fixes (false-green test, cross-file invariant, rerun)

---

## STEP 4 — Verify gates and resubmit

```bash
python3 scripts/collapse_check.py tasks/<task-name>
python3 scripts/hard_difficulty_predictor.py tasks/<task-name> --strict --json
python3 scripts/task_gate.py tasks/<task-name> --strict --report-dir /tmp/tb3-gates --skip-harbor
./scripts/check-task.sh --strict --report-dir /tmp/tb3-gates tasks/<task-name>
python3 scripts/harbor_gate.py tasks/<task-name> --oracle --oracle-stress 3 --nop --nop-stress 3
```

If oracle 1.0 + NOP 0.0 + collapse PASS but you expect another platform EASY:
run `python3 scripts/verifier_health.py --task-dir tasks/<task-name>` and check
partial-oracle ablations produce **behavioral** failures (not compile-only).

---

## STEP 5 — Report

```
DIFFICULTY REDESIGN REPORT — tasks/<task-name>

Root cause class: <A|B|C|D|E>
Structural changes (not bug count):
  - <topology/coupling/mechanism change 1>
  - <topology/coupling/mechanism change 2>

Spec amended: YES — validate_loop ACTION: <GO|CONTINUE>
Fix locations: <N> (was <M>)
Oracle semantic LOC: <N>
Mechanisms: <list>

Gates: collapse <PASS|FAIL>, predictor <X>%, oracle <score>, NOP <score>
Ready for platform resubmit: YES/NO
```

---

## Copy-paste prompt for your agent (when difficulty_increase failed)

Use this verbatim, replacing `<task-name>`:

```
Task <task-name> stayed TRIVIAL/EASY on platform after difficulty_increase.md.

Follow prompts/difficulty_redesign.md exactly.

Do NOT add more bugs or obfuscate instruction.

1. Run collapse_check, post_disclosure_collapse, hard_difficulty_predictor, instruction_audit.
2. Write Collapse Redesign Report — identify root cause B–E (not more random bugs).
3. Amend specs/<task-name>.md via validate_loop (step2a_difficulty rules): new coupling
   topology, ≥4 difficulty mechanisms, ≥3 fix locations, ablation_plan.
4. Rebuild tasks/<task-name>/ from amended spec (Step2b).
5. Pass collapse_check, check-task.sh, harbor oracle/NOP before resubmit.

Goal: HARD via coupled cross-file invariants and false-green traps — not
unidentifiable defects.
```

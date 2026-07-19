# Pipeline-Resistant Task Design

Use this file when generating a new Terminal-Bench task idea. The step pipeline (Step 1 → Step 2b → Step 3b → Step 4 → Step 5) applies compliance edits that inadvertently weaken difficulty. This guide tells you how to design the task **upfront** so it survives those edits and remains HARD at the exit of the pipeline.

Do NOT skip this file. Attach it alongside the other bundle files during ideation.

---

## Why the Pipeline Weakens Tasks

The following pipeline steps introduce difficulty-reducing edits as a side-effect of compliance:

| Step | Mechanism | Difficulty-Reducing Side Effect |
|------|-----------|--------------------------------|
| Step 2b collapse_check | Renames symbols to avoid grep-collapse (RC2) | Accidentally signals fix location |
| Step 2b discoverability gate | Strips env hints/comments | Reduces coupling clarity needed to understand bugs |
| Step 2b genuine-test gate | Requires ≥2 valid approaches | Loosens tight cross-component invariant assertions |
| Step 3b dirty-flag loop | Every review edit triggers re-oracle | `solve.sh` gets overfitted and too explicit |
| Step 3b collapse audit | Documents fix frontier for reviewer | Over-specifies oracle direction |
| Step 5 rubric | Rubric entries describe correct behaviors | Reveals fix targets to agents |

**The pipeline cannot be changed.** Design around it.

---

## The Six Pipeline-Resistant Design Rules

Apply ALL six rules during idea generation and spec design. A task that fails any rule should be redesigned before entering Step 2a.

---

### Rule 1 — Over-Engineer Depth: Design for Loss

**Target 5–6 interlocking bugs.** Expect 1–2 to be weakened or exposed during compliance edits. The task must still be HARD with only 3–4 remaining after pipeline exit.

**Screening test:** Remove any 2 bugs from your design. Can a frontier model solve the remaining 3–4 in one pass? If yes, redesign.

Do NOT design 3 bugs and expect all 3 to survive intact. They won't.

---

### Rule 2 — Use Runtime-State Bugs, Not Code-Structure Bugs

**Difficulty must live in runtime behavior, not in static code structure.**

Static-structure bugs (wrong constant, wrong condition in a named function) are easy for the collapse check to detect and the discoverability gate to expose. They also make the task easy once the agent finds the right file.

Runtime-state bugs only manifest under specific preconditions:
- Only on the second invocation with a specific database state
- Only when a partial write is followed by a concurrent read
- Only when a prior GC pass left a specific residue in the index
- Only when recovery is attempted after a particular sequence of operations

**Screening test:** Can the bug be found by grepping for the symptom described in the instruction? If yes, it is a code-structure bug — redesign it as a runtime-state violation.

---

### Rule 3 — Pre-Satisfy the Collapse Check by Topology Design

**Design the file topology and symbol names to pass `collapse_check.py` without any edits.**

If the collapse check fires RC2/GX9 during Step 2b, the required fix (renaming, redistributing) teaches the agent exactly where to look. Prevent this by designing names that are:
- Realistic domain vocabulary (e.g., `segment_journal`, `barrier_coordinator`, `index_reconciler`)
- Distinct from the instruction's surface nouns (instruction says "pruner drift", code says `epoch_fence_manager`)
- Not mirroring the prompt bullets (prompt says "GC must delete files", code has `gc_run()` NOT `delete_files_on_gc()`)

**Screening test:** Take the 5 most important nouns from your draft `instruction.md`. Do any of them grep directly to a function or file name in your planned environment? If yes, rename before drafting.

---

### Rule 4 — Pre-Satisfy the Genuine-Test Gate with Property-Based Tests

**Write tests as behavioral property checks from the start — never as formula reimplementations.**

The genuine-test gate requires ≥2 valid solution approaches to pass core tests. If tests are tight exact-value assertions, this gate will force loosening them, stripping the hardest invariant checks.

Design tests to be inherently flexible from day one:
- Cross-run invariants: run once, save output, run again, assert identical
- Metamorphic checks: changing input X should change output Y (without asserting the exact value of Y)
- Structural consistency checks: field A in subsystem 1 must agree with field B in subsystem 2
- Derived digest checks: hash of observed output must be stable across runs (without revealing the hash algorithm)
- State hygiene: after a recovery operation, the DB, disk, and cache must all be mutually consistent

**Never write:** `assert result["digest"] == _compute_expected_digest(matrix)`

**Write instead:** `assert result["digest"] == second_run["digest"]` (rerun stability)

**Screening test:** For every test assertion, ask "does this test reimplement the algorithm it checks?" If yes, replace with a metamorphic or cross-run check.

---

### Rule 5 — Spread the Fix Frontier Across ≥4 Files

**No single file should control more than 30% of the tests.**

If the fix frontier is 1–2 files, Step 3b's collapse audit will document it precisely, and the oracle direction becomes over-specified. Additionally, a concentrated frontier fails RC7.

Design the bug set so:
- File A hosts bugs tested by 1–2 tests exclusively
- File B hosts bugs tested by 1–2 different tests exclusively
- File C hosts bugs tested by 1–2 different tests exclusively
- File D hosts bugs tested by 1–2 different tests exclusively
- Cross-file consistency bugs are tested by 2–3 tests that span files A+B, B+C, etc.

**Screening test:** List your planned test functions. Assign each to the primary file it would fail on. Is any file assigned >30% of the tests? Redistribute bugs until no file dominates.

---

### Rule 6 — Use a 3-Way Consistency Invariant as the Core Difficulty

**Make the central challenge a consistency requirement across ≥3 subsystems.**

Single-component bugs can be fixed file by file. Multi-way consistency bugs cannot — fixing one subsystem without the others always fails the verifier. No compliance edit can simplify this because it's architectural.

Examples of 3-way consistency patterns:
- Disk files ↔ Database index ↔ In-memory/on-disk cache must all agree after every operation
- WAL log ↔ Segment state ↔ Barrier epoch must be mutually consistent after recovery
- Build artifact manifest ↔ Dependency graph ↔ Cached fingerprint must agree after any rebuild
- Module version registry ↔ Physical file store ↔ Latest-resolution cache must be consistent at all times

**Screening test:** After fixing any single subsystem in isolation, does the verifier still fail? It must. If fixing one subsystem alone could produce a PASS, there is no 3-way invariant — redesign.

---

## Pre-Generation Checklist

Before submitting a task idea to Step 2a, confirm:

- [ ] **Rule 1:** 5–6 bugs designed; removing any 2 still leaves a HARD task
- [ ] **Rule 2:** All bugs are runtime-state violations, not static code errors
- [ ] **Rule 3:** No instruction noun greps directly to a file/function name in the environment
- [ ] **Rule 4:** All planned tests are property/invariant checks — no algorithm reimplementations
- [ ] **Rule 5:** Fix frontier spans ≥4 files; no file controls >30% of tests
- [ ] **Rule 6:** Core difficulty is a 3-way+ consistency invariant; single-subsystem fixes still fail verifier

A task idea that fails any checklist item should be **redesigned before Step 2a**, not patched during Step 2b.

---

## Session Constraints (update when submitting new tasks)

### Blocked Languages
| Language | Reason |
|---|---|
| Python | Blocked for this session |
| *(Go — discouraged)* | Already used ×2 |
| *(Rust — discouraged)* | Already used ×1 |

**Preferred for next task:** Java, C/C++, TypeScript, or JavaScript

### Blocked Categories
| Category | Reason |
|---|---|
| `software-engineering` | Permanently blocked |
| `debugging` | Permanently blocked |
| `data-processing` | Session-blocked (used in `wal-segment-pruner-drift`) |
| `build-and-dependency-management` | Session-blocked (used in `go-module-proxy-index-divergence`, `incremental-build-graph-convergence`) |

**Available for next task:** `system-administration`, `games`, `machine-learning`, `security`, `scientific-computing`

---

## Quick Reference: What Each Rule Protects Against

| Rule | Protects Against |
|------|-----------------|
| Rule 1 (depth) | Losing 1-2 bugs to compliance without going below HARD |
| Rule 2 (runtime-state) | collapse_check symbol renaming revealing fix location |
| Rule 3 (topology) | GX9/RC2 fires requiring name changes that signal patch location |
| Rule 4 (property tests) | Genuine-test gate loosening tight invariant assertions |
| Rule 5 (spread frontier) | Step 3b collapse audit over-specifying oracle direction |
| Rule 6 (3-way invariant) | Any single compliance edit collapsing the core difficulty |

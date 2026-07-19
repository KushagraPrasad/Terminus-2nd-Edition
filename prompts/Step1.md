# Step 1: Idea Generation (ChatGPT)

Use these two prompts in order.

## Prompt 1 (Option B - build seed bank)

Run Option B from `web/bulk-idea-generation.md` in goal-sized **full-six** mode
(not opus-weak). The final target after Option A is 150 Step-2a-ready seeds.
Use all **six accepted categories** (blocked categories excluded — see below),
keep the bank category-balanced, keep Topology distinct within category, and
return one downloadable `.md` seed-bank file.

Each seed must name an implementation language from the **8 accepted families**
in `task-creation.mdc` § Accepted implementation languages. **Do not use Python**
as it is no longer allowed for new submissions — spread other languages across the bank.

## Prompt 2 (Option A - refine/consolidate bank)

Run Option A from `web/option-a-seed-refinement.md` in step2a-bank mode against
the attached bulk-ideas file. The final target is 150 Step-2a-ready seeds.
Repair or replace weak seeds instead of collapsing to a tiny shortlist.
Keep all **six accepted categories** balanced, keep Topology distinct within
category, and return one downloadable `.md` file.

---

## Accepted categories (6 only — BLOCKED categories forbidden)

Every seed **must** use exactly one of these `task.toml` categories:

1. `system-administration`
2. `build-and-dependency-management`
3. `games`
4. `machine-learning`
5. `security`
6. `scientific-computing`

**PERMANENTLY BLOCKED — never use in Step 1 seeds:**

| Blocked | Why | Remap instead |
|---------|-----|---------------|
| `software-engineering` | Category blocked for new submissions | `build-and-dependency-management`, `games`, or `machine-learning` |
| `debugging` | Category blocked for new submissions | Same six categories + `task_shape: repair_existing_system` when diagnosis is the work |
| `data-processing` | Category blocked for new submissions | `scientific-computing`, `machine-learning`, or `system-administration` |

Also forbidden:

- Seeds whose **only** hardness is "find the bug" with no domain substrate
- Seeds framed as generic debugging exercises without an accepted category domain
- Tags like `debugging` as the primary category tag (domain tags OK: `replay`, `state-recovery`)

---

## Unique seed requirement (BLOCKING)

Every new seed must be **unique** — not a rename of a prior seed, spec, or task.

Before pursuing a seed in Cursor Step 2a:

1. Assign a unique `seed_id` (kebab-case slug you have not used before).
2. Assign a distinct **Topology** token (3–6 words; must not match any prior seed in repo or registry).
3. Check uniqueness:

```bash
python3 scripts/seed_uniqueness_check.py check \
  --seed-id <your-seed-id> \
  --topology "<distinct topology phrase>" \
  --category <accepted-category> \
  --task-name <planned-task-slug>
```

4. After Step 2a GO, register the seed:

```bash
python3 scripts/seed_uniqueness_check.py register \
  --seed-id <your-seed-id> \
  --topology "<distinct topology phrase>" \
  --category <accepted-category> \
  --task-name <task-slug> \
  --task-shape <task_shape>
```

Audit existing collisions:

```bash
python3 scripts/seed_uniqueness_check.py audit
```

**Reject** seeds that collide on topology, slug, or core failure-mode pattern with an existing spec/task.

---

## Accepted implementation languages (8 families — Python blocked)

When assigning or refining a seed language, pick from this list only — vary
families across the bank:

| # | Family | `task.toml` tags |
|---|--------|------------------|
| 1 | JavaScript | `javascript` |
| 2 | TypeScript | `typescript` |
| 3 | Go | `go` |
| 4 | Rust | `rust` |
| 5 | Java | `java` |
| 6 | C / C++ | `c`, `cpp` |
| 7 | Ruby | `ruby` |
| 8 | Bash / Shell | `bash`, `shell` |

**Python (`python`) is no longer allowed** as a task implementation language for new submissions.

Full rules: `task-creation.mdc` § Accepted implementation languages.

---

## Idea Rejection Criteria

Reject ideas that:

* Use blocked categories (`software-engineering`, `debugging`, `data-processing`)
* Use Python as the task implementation language
* Depend on hidden requirements
* Depend on undocumented constants or formulas
* Depend on test reverse-engineering (agents must not need to read `tests/` to learn the contract)
* Are simple CRUD applications or API implementations
* Are simple scripts or straightforward single-file bug fixes
* Can be solved by editing a single obvious function
* Collapse after honest instruction disclosure (post-disclosure mapping to one obvious module)
* Reuse topology/failure-mode patterns from existing specs without substantive novelty

Every tested behavior must be discoverable from `instruction.md`, documented
schemas, and public APIs — not from pytest alone.

---

## Advanced Hardness Requirement

At least one of the following must be **central** to the task:

* State recovery
* Replay semantics
* Cache invalidation
* Distributed consistency
* Multi-component interaction
* Long-context reasoning
* Journal reconstruction
* Build failures / CI failures
* Adversarial generalization / variant ladders
* Formal correctness under constraints

Tasks lacking advanced engineering complexity should be rejected. Difficulty must
not come from hiding requirements, magic numbers, or undocumented recovery rules.

Each seed's `difficulty_mechanism_plan` must list **≥4 distinct allowed mechanisms**
(see `@idea-validation.mdc`). Timing/latency thresholds are forbidden.

This aligns with `scripts/hard_difficulty_predictor.py`, which requires ≥3
documented failure modes and at least one advanced category.

---

## Model Failure Prediction

Before approving a task idea, predict at least **3 realistic model failure modes**.

Examples:

* Replay state recomputation errors
* Incorrect cache invalidation timing
* Recovery ordering mistakes
* Journal reconstruction bugs
* Distributed consistency violations
* Variant-ladder arm failures after local fix

If fewer than 3 realistic failure modes exist, **reject the idea**.

Each failure mode should name a concrete engineering mistake a frontier model
would make — not generic "wrong output" or grep-level constant fixes.


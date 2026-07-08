# Step 3b Paper Review — snapshot-compaction-race-cpp

Date: 2026-05-22  
Oracle job: `jobs/2026-05-22__19-19-03` (mean 1.0)  
NOP job: `jobs/2026-05-22__19-19-30` (mean 0.0)  
Step 2b readiness: **PASS** (checksum verified after refresh)

## 1. Structural review (@review-and-submit §1–7)

| Section | Verdict | Note |
|---------|---------|------|
| Instruction | **PASS** | Symptoms-only; snake_case keys; points to `/app/docs/report_contract.md` for formulas. |
| Environment | **PASS** | Pinned Dockerfile (pytest venv, tmux, asciinema, g++/cmake); no compose; broken env has distributed bugs. |
| Oracle | **PASS** | Restores FNV in `epoch_trace.cpp`, phase/rebind/probe/fold/scan parity; ~92 LOC substantive delta; `vh_*_patch` gates. |
| Verifiers | **PASS** | Independent `expected_report()`; seed-mutation anti-cheat; canonical offline `test.sh`. |
| Metadata | **PASS** | `allow_internet = false`, `category_profile`, reference justification, timeouts coherent. |
| Structure | **PASS** | Standard layout; `output_contract.toml` present. |
| Difficulty calibration | **WARN** | Collapse WARN (5); post-disclosure formula density ↑ to 29 lines (explicit FNV/sort-fold). |

Mandatory checks:

- **reference_pattern:** PASS  
- **Verifier deps:** PASS (Dockerfile + offline test.sh)  
- **Platform tmux/asciinema:** PASS  
- **Instruction/test alignment:** **PASS** (post-revision) — FNV accumulator and sort-fold explicitly documented; matches `test_outputs.py` and `epoch_trace.cpp` oracle fix.

Hard FAILs: none.

---

## 2. Collapse audit (Part A)

**Verdict: WARN** (0 FAIL, 5 WARN, 18 PASS)

### Smallest plausible patch

Enable three gated paths; fix phase settle/span; max-epoch remap; FNV mix in `trace_mux_c`; sort-fold; depth probe; anchor parity in `scan_anchor_chain`.

### Likely editable frontier

Six substantive targets across `core/` (`phase_gate`, `identity_fold`, `epoch_trace`), `store/` (`rebind_table`), `checks/` (`surface_probe`, `history_scan`).

### Requirement-to-file map

| Boolean | Primary subsystem |
|---------|-------------------|
| lane / commit | `phase_gate` |
| map_epoch_roundtrip | `rebind_table` (+ gated patch) |
| alias_sort_stability | `identity_fold` (sort-fold) |
| horizon_anchor_trace | `epoch_trace` + `history_scan` (coupled) |
| probe_depth_agreement | `surface_probe` |

### Post-disclosure

**WARN** — 29 formula-like lines after explicit FNV/sort-fold text. Disclosure is **fair** (reviewer-mandated); mapping still requires reading `ledger_mux.cpp` and implementing fixes in multiple modules — not a one-file transcription recipe (`small_formula_frontier` PASS).

### Oracle LOC

117+ transitive LOC; 92 LOC real edit distance — substantive.

### Discoverability

`identity_fold` name is intentional decoy; contract states sort-fold. Wrong FNV in broken `epoch_trace` is not advertised in instruction (symptoms-only). No `// BUG:` markers.

### Residual hardness (raised intentionally)

- **Coupled horizon path:** wrong per-element mix in `epoch_trace` + missing parity in `history_scan` — two files, one contract section.  
- **Inverted phase latch:** visible without settled-ready.  
- **Gated rebind:** empty map unless patch enabled and max-epoch logic applied.  
- **Seed mutation test** still distinguishes FNV implementations.

### WARN justification

| Signal | Classification |
|--------|----------------|
| RC2 | ACCEPT WITH NOTES — partial keyword overlap; decoys + coupling |
| RC8 | ACCEPT WITH NOTES — six targets, three roots |
| CR1/CR2/CR8 | ACCEPT WITH NOTES — legacy, no construction_manifest |
| post_disclosure density | ACCEPT WITH NOTES — required for platform instruction sufficiency |

### Part E (platform agents, prior run)

Pre-revision: HARD, solvable, instruction sufficiency **FAIL** (FNV ambiguity). Post-revision expectation: fairer failures on implementation, not spec misread; pass rate may remain high on Opus — recalibrate after re-upload.

---

## 3. Per-test feasibility (Part B)

| Test | Summary | Single-path | Chain | Order | Flake | Niche | 3a-V |
|------|---------|-------------|-------|-------|-------|-------|------|
| `test_lane_window_consistency` | Tick vs boundary | LOW | LOW | LOW | LOW | LOW | No |
| `test_commit_visibility` | Commit tick frame | LOW | LOW | LOW | LOW | LOW | No |
| `test_map_roundtrip` | Max epoch per slot | LOW | MED | LOW | LOW | LOW | No |
| `test_alias_sort_stability` | Sort-fold monotone | LOW | LOW | LOW | LOW | LOW | No |
| `test_horizon_mix` | FNV + parity on shipped C | LOW | **MED** | LOW | LOW | MED | No |
| `test_depth_agreement` | Shallow/deep probe | LOW | MED | LOW | LOW | LOW | No |
| `test_report_tracks_seed_file_contents` | Seed anti-cheat | LOW | **MED** | MED | LOW | MED | No |

**Step 3a-V:** Not escalated.

---

## 4. Platform auto-eval readiness (Part F)

| Check | Status |
|-------|--------|
| Canonical offline `test.sh` | **PASS** |
| Dockerfile: pytest + tmux + asciinema | **PASS** |
| `allow_internet = false` | **PASS** |
| `task_runtime_deps.py --strict` | **PASS** |
| Contract aligns with tests | **PASS** (FNV + sort-fold) |

---

## 5. Edit ledger (since last Step 3b)

| File | Change |
|------|--------|
| `environment/docs/report_contract.md` | Explicit FNV-1a loop; sort-fold definition; anti-pattern note |
| `environment/src/core/epoch_trace.cpp` | Broken: wrong `v^(v+addend)` mix |
| `environment/src/core/phase_gate.cpp` | Broken: inverted settle gate |
| `environment/src/store/rebind_table.cpp` | Broken: gated early return |
| `solution/solve.sh` | Oracle restores correct `epoch_trace.cpp` |

No edits in this Step 3b run (review-only refresh).

---

## 6. Next action

**Ready for Step 4.**

Harbor evidence:

- Oracle: `jobs/2026-05-22__19-19-03`
- NOP: `jobs/2026-05-22__19-19-30`

Proceed: `harbor_gate --oracle-repeat 10` → `package_task` → `approve_task.py --strict`.

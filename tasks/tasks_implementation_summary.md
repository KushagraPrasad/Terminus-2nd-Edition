# Tasks Implementation & Verification Summary

This document summarizes the specifications, exact bugs/problems introduced in the candidate codebase, and the verification metrics for the active Terminal-Bench tasks.

---

## 1. 🛠️ Incremental Build Graph Convergence (`incremental-build-graph-convergence`)
* **Language**: Go (Golang)
* **Category**: Build and Dependency Management
* **Task Type**: Task Revision & Refactoring

### Functional Specification
An incremental build engine checking whether packages in a build graph have safely converged based on public Go interface signatures.

### Exact Bugs & Challenges Introduced (For the Evaluated Agent to Fix)
1. **Non-Converging Graph Cycles (Infinite Loops)**:
   * **The Bug**: When graph edges are edited or updated, the graph reconciler executes rebuilds sequentially but gets trapped in infinite loops when cyclic package dependencies occur.
   * **Why it's hard**: The agent must implement cycle detection and topological sorting during edge updates to enforce convergence constraints.
2. **Inaccurate Fingerprinting (Decoy Decoupling)**:
   * **The Bug**: The compiler engine calculated source file fingerprints based on a raw file hash.
   * **Why it's hard**: Pure formatting edits, doc comments, or private helper additions in a package would trigger cascading rebuilds of all downstream packages. The agent must parse Go source files to calculate fingerprints based *only* on public interface signatures (signatures, public types, and exports).
3. **Registry/Manifest Synchronization Drift**:
   * **The Bug**: SQLite records were synchronized to `artifact_manifest.json`, but physical build outputs were never pruned from disk.
   * **Why it's hard**: Stale build files persist, wasting disk space. The agent must reconcile active SQLite output paths with the physical filesystem and physically delete unreferenced build outputs.

---

## 2. 🛡️ Token Revocation and Freshness Coordinator (`token-revocation-freshness`)
* **Language**: TypeScript / Node.js
* **Category**: Software Engineering (Authentication / Security)
* **Task Type**: Task Repair & Verification

### Functional Specification
An authorization gateway coordinator handling JWT token verification, SQLite token revocation storage, and asynchronous fallback keys with strict monotonic sequence progression.

### Exact Bugs & Challenges
1. **Typo in plural structures**: Singular/plural spelling typo ('structures' vs 'structure') inside validator.ts.
2. **Wildcard Invalidation Eviction**: The cache failed to parse and match `field:value` wildcard pattern prefixes to dynamically evict matching cached token entries.
3. **Blacklist Sequence Sync**: Blacklist sync updates did not verify monotonically increasing sequence updates inside atomic database transactions, allowing stale updates or transaction rollbacks to be skipped.

---

## 3. 💾 Journaling Filesystem Split Write Recovery (`journaling-fs-split-write`)
* **Language**: C
* **Category**: Systems Programming / Filesystems
* **Task Type**: System Repair & verification

### Functional Specification
A userspace filesystem daemon replaying WAL journal transactions to recover state idempotently and verify block checksums under split-write crash conditions.

### Exact Bugs & Challenges
1. **Verification Logic**: Checksum verification simply returned 1, failing to run the block checksum loop.
2. **Multi-block WAL Replays**: The block replay logic only replayed the first block of multi-block WAL logs.
3. **Missing Replay Breaks**: Corrupted records or transaction mismatches missed break limits during transaction loops.
4. **Flipping/Concurrent Writes**: Logical block multipliers were calculated with block division instead of multiplication, and concurrent writes caused early GC panics.

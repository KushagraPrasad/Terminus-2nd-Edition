#!/usr/bin/env python3
"""Generate 80 frontier benchmark candidate concepts across 14 categories."""

from __future__ import annotations

import re
import textwrap
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "benchmark/frontier-56/phase1-candidates-80.md"

SHAPES = [
    "repair_existing_system",
    "constrained_build",
    "reverse_engineering",
    "optimization_under_constraints",
    "adversarial_generalization",
    "formal_reasoning",
]

FRAMING = {
    "repair_existing_system": ("symptoms-only", "diagnosis"),
    "constrained_build": ("design-brief", "design search"),
    "reverse_engineering": ("behavioral-target", "semantic inference"),
    "optimization_under_constraints": ("constraint-complete", "constrained optimization"),
    "adversarial_generalization": ("constraint-complete", "adversarial generalization"),
    "formal_reasoning": ("constraint-complete", "formal correctness"),
}

# (title, topology, framing, d1, d2, d3, arch_family, shape, language, fm1, fm2, fm3, large_codebase)
# benchmark_category assigned at render time from category bucket

def assign_family(seed: tuple) -> str:
    """One unique architecture family per seed (topology slug)."""
    topo = seed[1]
    return re.sub(r"[^a-z0-9]+", "_", topo.lower()).strip("_")[:48]


BUCKETS: dict[str, list[tuple]] = {
    "build-dependency": [
        ("Offline lockfile rehydration gap", "offline lockfile rehydration", "Incremental offline builds succeed on clean tree but fail when lockfile digest disagrees with vendored tarball generation.", "lockfile records hash of generated crate not source manifest", "vendor dir stale after feature unification reorder", "cargo metadata vs resolver graph disagree on patch edges", "build_ci_failure", "repair_existing_system", "rust", "resolver edge misread", "patch override ordering bug", "stale vendor tarball hash"),
        ("ABI rebuild drift detector", "ABI rebuild drift", "Shared library consumers crash after rebuild though soname unchanged and link succeeds.", "struct padding differs under new compiler default", "generated header not rebuilt when .rs layout changes", "LTO strips symbol versioning expected by loader", "compiler_systems", "repair_existing_system", "cpp", "header generation skip", "LTO symbol visibility drift", "padding layout mismatch"),
        ("Hermetic sandbox build contract", "hermetic sandbox build", "Build must reproduce bit-identical artifacts under strict namespace and offline mirror constraints.", "proc macro reads host /etc during build", "rustc workspace feature unification order affects metadata hash", "build script emits nondeterministic timestamp", "build_ci_failure", "constrained_build", "rust", "proc macro host leak", "feature unification ordering", "timestamp nondeterminism"),
        ("Cross-compile sysroot skew", "cross compile sysroot skew", "Target binary links on build host but faults on device due to sysroot library generation mismatch.", "linker script path differs host vs target sysroot", "multilib selection wrong for soft-float ABI", "pkg-config returns host flags on cross path", "build_ci_failure", "repair_existing_system", "go", "sysroot path confusion", "multilib ABI mismatch", "pkg-config host leak"),
        ("Bazel query graph stale edge", "bazel query stale edge", "Query reports target up-to-date while runtime loads stale .so from previous configuration transition.", "configuration split not invalidated on flag change", "aspect output cached across incompatible transitions", "runfiles manifest omits rebuilt data dep", "build_ci_failure", "repair_existing_system", "java", "config transition cache", "aspect stale output", "runfiles manifest drift"),
    ],
    "build-management": [
        ("Incremental build shadow artifacts", "incremental shadow artifacts", "Clean build passes but incremental rebuild serves stale object files after header rename.", "depfile missing generated header edge", "ccache key ignores compiler define change", "ninja restat skips compile when mtime alone changes", "build_ci_failure", "repair_existing_system", "cpp", "depfile missing edge", "ccache key omission", "restat false negative"),
        ("CI matrix cache poisoning", "CI matrix cache poison", "Main branch green but feature branch inherits poisoned cache from orthogonal matrix leg.", "cache key omits compiler major version", "restore-key fallback pulls wrong OS leg", "artifact upload includes build tree secrets path", "cache_invalidation", "repair_existing_system", "go", "cache key collision", "restore-key fallback", "cross-leg artifact bleed"),
        ("Pipeline stage ordering trap", "pipeline stage ordering", "Deploy succeeds while integration tests ran against previous artifact generation.", "needs edge not enforced on manual rerun", "artifact promotion races with tag push", "downstream job consumes floating latest tag", "build_ci_failure", "repair_existing_system", "java", "needs edge bypass", "promotion race", "floating tag consumption"),
        ("Distributed compile cache invalidation", "dist compile cache invalidation", "Remote cache hits return objects built with wrong macro set after header-only change.", "content hash excludes preprocessor defines", "remote executor platform tag too coarse", "local fallback uploads poisoned entry", "cache_invalidation", "repair_existing_system", "rust", "define omission in hash", "platform tag coarse", "poisoned remote upload"),
        ("Release artifact provenance gap", "release provenance gap", "Signed release verifies but provenance attestation missing witness for one build step.", "in-toto link predicate type hashed wrong", "rekor index not checked against bundle", "timestamp authority not cross-signed", "build_ci_failure", "repair_existing_system", "go", "predicate hash mismatch", "rekor index skip", "timestamp chain gap"),
    ],
    "challenging-games": [
        ("Move budget Sokoban variant ladder", "move budget sokoban ladder", "Solver must complete puzzle family under strict move budget across variant ladder of rule tweaks.", "push priority interacts with ice tiles differently per arm", "undo stack depth limited on one variant", "goal detection differs corner vs edge goals", "game_engine_semantics", "adversarial_generalization", "rust", "push priority misread", "undo depth miscount", "goal predicate variant"),
        ("Procedural level seed replay", "procedural level replay", "Generated levels diverge from reference when seed replay omits one initialization phase.", "RNG stream split per subsystem order-sensitive", "biome table cached across hot reload", "entity spawn queue processed before terrain finalize", "replay_recovery", "repair_existing_system", "cpp", "RNG stream split error", "biome cache stale", "spawn order inversion"),
        ("AI search transposition table bug", "transposition table bug", "Engine mis-evaluates position after transposition store retrieves wrong bound type.", "Zobrist key collision on pawn structure", "bound type not updated on deeper search", "table entry generation stale after null move", "game_engine_semantics", "repair_existing_system", "cpp", "Zobrist collision", "bound type stale", "generation counter miss"),
        ("Game logic invariant model check", "game logic model check", "Prove turn-based rules cannot reach illegal state under documented action set.", "simultaneous resolution order affects legality", "pass action skipped in compound turn", "undo restores wrong phase counter", "formal_verification", "formal_reasoning", "rust", "resolution order gap", "phase counter drift", "undo state incomplete"),
        ("Input remap variant ladder", "input remap variant ladder", "Control remap must survive ladder of deadzone, repeat rate, and chord bindings.", "chord timeout differs gamepad vs keyboard", "analog deadzone applied before axis merge", "focus loss drops buffered edge events", "game_engine_semantics", "adversarial_generalization", "go", "chord timeout drift", "deadzone order bug", "focus buffer loss"),
    ],
    "cryptography": [
        ("AEAD nonce reuse recovery", "AEAD nonce reuse recovery", "Decryptor reports auth failure intermittently when nonce counter rewinds after crash.", "persistent counter not fsynced before ack", "backup restore replays old counter window", "parallel writers share counter file without lock", "journal_reconstruction", "repair_existing_system", "rust", "counter rewind", "fsync ordering", "parallel counter race"),
        ("Threshold signature shard mismatch", "threshold sig shard mismatch", "Sharded recovery reconstructs key locally but verify fails under rotated metadata.", "shard index permutation not authenticated", "threshold includes retired custodian", "HKDF info string differs between arms", "protocol_implementation", "repair_existing_system", "go", "shard index swap", "retired custodian count", "HKDF info mismatch"),
        ("TLS extension order inference", "TLS extension order inference", "Infer required extension ordering from traces to build compatible terminator.", "key_share group preference differs by arm", "supported_versions encoding ambiguous", "post-handshake auth optional path", "protocol_implementation", "reverse_engineering", "cpp", "extension order drift", "version encoding ambiguity", "post-handshake path"),
        ("Crypto agility variant ladder", "crypto agility ladder", "Verify signatures across algorithm agility ladder without unsafe fallback ordering.", "RSA-PSS salt length differs by provider", "EdDSA context string optional per arm", "hybrid KEM combines classical and PQC wrong", "protocol_implementation", "adversarial_generalization", "rust", "PSS salt mismatch", "EdDSA context omission", "hybrid KEM composition"),
        ("Encrypted backup header parse", "encrypted backup header", "Backup decrypts first chunk but manifest hash mismatches due to header endianness.", "salt iteration count conflicting widths", "AEAD AAD excludes version field", "compression flag affects MAC input", "protocol_implementation", "repair_existing_system", "go", "endianness drift", "AAD scope error", "compression MAC scope"),
        ("Passkey challenge replay", "passkey challenge replay", "WebAuthn ceremony verifies once but accepts replayed challenge on concurrent session.", "challenge store not bound to origin", "signCount not checked on backup path", "UV flag optional on fallback authenticator", "security_auditing", "repair_existing_system", "java", "origin binding miss", "signCount skip", "UV optional bypass"),
    ],
    "data-processing": [
        ("Stream window aggregate drift", "stream window aggregate drift", "Rolling aggregates match batch on sample data but drift on production event order.", "watermark lateness treated as drop not side output", "session gap closure uses processing time", "retraction not applied to incremental state", "data_pipeline_recovery", "repair_existing_system", "java", "watermark semantics", "processing time gap", "retraction omission"),
        ("Schema inference variant ladder", "schema inference ladder", "Inferred schema must survive variant ladder of malformed and nested edge cases.", "union widening order changes nullability", "numeric string coercion differs arms", "array tuple vs list ambiguity", "log_inference", "adversarial_generalization", "rust", "union widen order", "coercion path drift", "array tuple ambiguity"),
        ("PII redaction variant ladder", "PII redaction ladder", "Redaction must not leak substrings under regex collision and encoding ladder.", "overlapping patterns hide partial secrets", "structured field redaction breaks JSON", "hash salt must stay stable for correlation", "data_pipeline_recovery", "adversarial_generalization", "python", "regex overlap leak", "JSON validity break", "salt instability"),
        ("Data lineage invariant proof", "data lineage invariant proof", "Prove pipeline cannot emit row without required provenance fields under rewrite rules.", "view definition hides intermediate filter", "late arriving dimension changes grain", "surrogate key reused across reload", "formal_verification", "formal_reasoning", "java", "view grain hide", "late dimension skew", "surrogate key reuse"),
        ("Regex extraction trace inference", "regex extraction inference", "Infer extraction rules from sample traces; must generalize to held-out arms.", "capture group optional in subset of arms", "multiline mode changes anchor behavior", "unicode property escapes differ engine", "log_inference", "reverse_engineering", "rust", "capture optional drift", "multiline anchor", "unicode property gap"),
        ("Metamorphic ETL checksum chain", "metamorphic ETL checksum", "ETL checksum chain breaks when intermediate sort order differs from documented stable sort.", "tie-break key omitted from hash input", "null ordering differs arms", "parallel merge changes equal-key order", "data_pipeline_recovery", "repair_existing_system", "go", "tie-break omission", "null order drift", "parallel merge order"),
    ],
    "data-scripting": [
        ("Pipeline DAG checkpoint resume", "pipeline DAG checkpoint", "Orchestrator resumes mid-DAG but replays completed stage causing duplicate side effects.", "checkpoint stores stage name not attempt id", "idempotent token not scoped to partition", "dynamic fan-out not captured in checkpoint", "replay_recovery", "repair_existing_system", "python", "checkpoint identity weak", "idempotency scope", "fan-out omission"),
        ("Shell task env inheritance trap", "shell env inheritance", "Script succeeds interactively but fails in CI due to inherited env changing precedence.", "exported function shadows POSIX builtin", "BASH_ENV mutates non-interactive path", "set -e masked by subshell ERR trap", "config_policy_precedence", "repair_existing_system", "bash", "function shadow builtin", "BASH_ENV side effect", "ERR trap scope"),
        ("Notebook cell reorder provenance", "notebook cell provenance", "Reordered notebook cells produce same output but wrong lineage metadata for audit.", "cell id not stable across save", "execution count reused after kernel restart", "widget state serialized out of order", "data_pipeline_recovery", "repair_existing_system", "python", "cell id instability", "execution count reuse", "widget serialize order"),
        ("Cron overlap guard failure", "cron overlap guard", "Scheduled job overlaps itself causing double write despite flock guard.", "flock released before async child completes", "timezone DST shifts schedule twice", "missed run policy catches up burst", "replay_recovery", "repair_existing_system", "bash", "flock lifetime short", "DST double fire", "catch-up burst"),
        ("Data contract validator builder", "data contract validator build", "Build validator enforcing evolving JSON contract under version ladder without network.", "optional field default differs version arms", "enum extension must reject unknown on old consumer", "numeric bound uses inclusive vs exclusive edge", "protocol_implementation", "constrained_build", "go", "default version drift", "enum extension rule", "bound inclusivity"),
    ],
    "debugging": [
        ("Journal replay generation skew", "journal replay generation skew", "After partial rollback, lanes disagree on closure counters despite aggregate looking fine.", "stale checkpoint ancestry revives retired generation", "combine invalidates before rollback completes", "echo lane reads pre-rollback facet material", "journal_reconstruction", "repair_existing_system", "rust", "generation skew", "combine order bug", "echo lane stale read"),
        ("Scheduler persistence reconciliation", "scheduler persistence reconciliation", "Tasks survive restart but runqueue order violates documented fairness after replay.", "WAL replay skips cancelled generation", "priority inversion on persistence fsync path", "lease renewal double-applies on recovery", "replay_recovery", "repair_existing_system", "go", "WAL skip cancelled", "priority inversion", "lease double apply"),
        ("Core dump stack inference", "core dump stack inference", "Infer corruption site from multi-thread cores with divergent unwinding across libc versions.", "unwinder stops at signal trampoline differently", "DWARF CFI missing for hand-written asm", "alt signal stack confuses frame chain", "log_inference", "reverse_engineering", "cpp", "unwind trampoline gap", "CFI missing", "alt stack confusion"),
        ("Distributed trace context break", "trace context propagation break", "Spans disconnected across services though requests succeed end-to-end.", "baggage header stripped at gateway", "trace id regenerated on async boundary", "parent span id reused after pool recycle", "log_inference", "repair_existing_system", "java", "baggage strip", "trace id regen", "span id reuse"),
        ("Heisenbug variant ladder", "heisenbug variant ladder", "Fix must survive ASAN on/off, jemalloc/glibc, single vs multi thread without masking.", "sanitizer changes timing hiding race", "allocator padding alters layout", "signal mask differs under harness", "replay_recovery", "adversarial_generalization", "rust", "timing mask", "layout drift", "signal mask diff"),
        ("Happens-before model check", "happens before model check", "Verify queue API linearizability under documented memory ordering for custom runtime.", "relaxed atomics create cycle not in logs", "fence placement differs ARM vs x86", "publication safety missing on lazy init", "formal_verification", "formal_reasoning", "cpp", "relaxed atomic cycle", "fence portability", "lazy init publish"),
    ],
    "large-codebase": [
        ("Monorepo import cycle repair", "monorepo import cycle repair", "Large Python monorepo fails typecheck only on full graph due to lazy import cycle.", "TYPE_CHECKING guard hides runtime cycle", "namespace package shadowed by local stub", "editable install resolves wrong package root", "compiler_systems", "repair_existing_system", "python", "TYPE_CHECKING mask", "namespace shadow", "editable path wrong", True),
        ("Legacy bytecode VM inference", "legacy bytecode VM inference", "Infer opcode semantics from traces; implement decoder passing metamorphic harness.", "wide instruction overlaps narrow prefix", "stack depth implicit on call pattern", "endian switch mid-image on arm ladder", "vm_inference", "reverse_engineering", "java", "opcode prefix overlap", "stack depth infer", "endian arm switch", True),
        ("Cross-module float policy drift", "cross module float policy", "Aggregated metrics disagree across modules though each passes local unit tests.", "Kahan sum only on master path", "decimal context differs import order", "json serializer rounding per module", "numeric_policy", "repair_existing_system", "python", "Kahan path split", "decimal context order", "json round per module", True),
        ("Plugin registry authority split", "plugin registry authority split", "Plugin load succeeds but sandbox escape via stale capability grant after hot reload.", "capability token not revoked on unload", "registry index reused for new plugin id", "signature check skipped on cached descriptor", "security_auditing", "repair_existing_system", "java", "capability revoke miss", "index reuse", "signature cache skip", True),
        ("Query plan cost model optimize", "query plan cost model optimize", "Optimize join order under cardinality cap using public cost formulas only.", "correlated subquery cardinality underestimated", "histogram bucket boundary inclusive wrong", "parallel worker skew not in cost model", "compiler_systems", "optimization_under_constraints", "cpp", "cardinality underestimate", "histogram boundary", "skew omission", True),
        ("Service mesh config precedence", "service mesh config precedence", "Effective routing policy wrong after layered CRD, annotation, and file overrides.", "precedence table differs control plane vs data plane", "namespace-scoped policy not invalidated on move", "default upstream timeout inherited wrong", "config_policy_precedence", "repair_existing_system", "go", "precedence table split", "namespace move stale", "timeout inherit wrong", True),
    ],
    "machine-learning": [
        ("Checkpoint resume optimizer state", "checkpoint optimizer resume", "Training resumes but optimizer moments wrong causing loss spike though weights match.", "Adam bias correction uses step from wrong run", "fp16 master weights not restored", "learning rate schedule tied to wall clock", "ml_infrastructure", "repair_existing_system", "python", "bias correction step", "fp16 master miss", "LR wall clock"),
        ("Sampler shard divergence repair", "sampler shard divergence", "Distributed sampler assigns overlapping indices after worker failure recovery.", "shard offset not advanced on resume", "drop_last differs eval vs train path", "seed split includes rank in wrong position", "ml_infrastructure", "repair_existing_system", "python", "shard offset stall", "drop_last mismatch", "seed split error"),
        ("OOD detection variant ladder", "OOD detection ladder", "Detector must flag held-out arms without threshold tuning on visible set only.", "feature scaling fit on full batch leaks", "temperature scaling uses val in train", "ensemble disagreement ignored on borderline", "ml_infrastructure", "adversarial_generalization", "python", "scaling leak", "temperature val leak", "ensemble ignore"),
        ("Mixed precision replay ladder", "mixed precision replay ladder", "Forward pass matches fp32 on small batch but diverges on large with same seed.", "loss scaler update before unscale", "TF32 enabled only rank zero", "allreduce order non-deterministic", "numeric_policy", "adversarial_generalization", "cpp", "scaler order", "TF32 rank split", "allreduce order"),
        ("Prompt injection eval ladder", "prompt injection eval ladder", "Eval harness must resist injection strings in tool outputs without blocklist hacks.", "system prompt concatenation order matters", "tool result delimiter escapable", "jailbreak via nested markup in citation", "ml_infrastructure", "adversarial_generalization", "python", "concat order inject", "delimiter escape", "nested markup"),
        ("Calibration isotonic monotonic proof", "isotonic calibration proof", "Prove isotonic mapping preserves monotonicity under documented tie-breaking.", "tie pool merges wrong adjacent blocks", "out-of-sample extrapolation flat wrong", "weight normalization differs arms", "formal_verification", "formal_reasoning", "java", "tie pool merge", "extrapolation flat", "weight norm drift"),
    ],
    "scientific-computing-analysis": [
        ("FFT resume corruption", "FFT resume corruption", "Spectral pipeline resumes mid-transform with wrong normalization constant.", "wisdom file tied to old grid topology", "real-to-complex plan reused incorrectly", "padding factor ignored in plan search", "numeric_policy", "repair_existing_system", "cpp", "wisdom stale", "plan reuse wrong", "padding ignore"),
        ("Cross-runtime float policy drift", "cross runtime float drift", "Simulation binary agrees on one OS but diverges on second with same inputs.", "FMA availability differs", "denormal flush changes branch", "reduction tree depth changes ULP", "numeric_policy", "repair_existing_system", "fortran", "FMA availability", "denormal flush", "reduction tree"),
        ("Unit conversion pipeline drift", "unit conversion drift", "Derived quantities disagree after unit string refactor in analysis notebook.", "offset temperature handled inconsistently", "compound unit drops dimension", "locale decimal comma breaks parser", "numeric_policy", "repair_existing_system", "python", "offset temp unit", "dimension drop", "locale comma"),
        ("Monte Carlo stratified overlap", "monte carlo stratified", "Coverage drops below nominal despite correct formula on visible strata.", "strata boundaries overlap after transform", "antithetic pairs correlated", "RNG split per stratum reuses stream", "numeric_policy", "repair_existing_system", "cpp", "strata overlap", "antithetic correlation", "RNG reuse"),
        ("Symplectic integrator energy drift", "symplectic energy drift", "Energy drifts past threshold on long orbit though short run acceptable.", "splitting order odd even differs", "potential gradient uses stale coords", "warm start reuses wrong momentum phase", "numeric_policy", "repair_existing_system", "fortran", "splitting order", "stale gradient", "momentum phase"),
        ("Interval arithmetic proof contract", "interval arithmetic proof", "Prove enclosure holds for deployed expression graph on all test intervals.", "dependency problem overestimation uncaught", "monotonicity not exploited", "rounding mode mix invalidates step", "formal_verification", "formal_reasoning", "cpp", "dependency blowup", "monotonicity miss", "rounding mix"),
    ],
    "security": [
        ("Revocation cache authority split", "revocation cache split", "Token validation accepts revoked credentials when cache partitions disagree.", "positive TTL exceeds revocation propagation", "negative cache not invalidated on rotation", "replica serves stale CRL fragment", "security_auditing", "repair_existing_system", "go", "TTL propagation gap", "negative cache stale", "CRL fragment stale"),
        ("MAC policy boolean precedence", "MAC boolean precedence", "Confined service gains capability after boolean toggle order differs from docs.", "conditional boolean stack not atomic", "dontaudit hides first failing allow", "module version changes boolean default", "security_auditing", "repair_existing_system", "java", "boolean stack order", "dontaudit mask", "default version drift"),
        ("Confused deputy RPC guard", "confused deputy RPC guard", "Service A invokes privileged B method using delegated client credentials.", "capability not scoped to method", "request metadata trusted from client", "async callback reuses stale delegation", "security_auditing", "constrained_build", "rust", "capability scope", "metadata trust", "stale delegation"),
        ("WAF bypass variant ladder", "WAF bypass ladder", "Harden normalization so encoding ladder cannot reach same backend sink.", "double decode differs by content type", "chunked reassembly boundary", "path normalization proxy vs app", "security_auditing", "adversarial_generalization", "go", "double decode", "chunk boundary", "path norm split"),
        ("Supply chain sig chain gap", "supply chain sig gap", "Package verifies with publisher sig but provenance chain missing witness.", "in-toto link hashed wrong predicate", "rekor index unchecked", "timestamp authority not cross-signed", "security_auditing", "repair_existing_system", "rust", "predicate hash", "rekor skip", "timestamp gap"),
        ("Privilege graph acyclic proof", "privilege graph proof", "Verify delegation graph acyclic under dynamic grant and revoke script.", "temporary grants expire out of order", "group inheritance cyclic", "revoke not propagated to derived tokens", "formal_verification", "formal_reasoning", "java", "grant expiry order", "inheritance cycle", "revoke propagation"),
    ],
    "software-engineering": [
        ("Typestate protocol proof", "typestate protocol proof", "Prove API usage state machine cannot reach illegal state at compile-checked subset.", "transition table incomplete on error path", "refinement type erasure loses phase", "macro-generated impl skips guard", "formal_verification", "formal_reasoning", "rust", "error path gap", "erasure loss", "macro guard skip"),
        ("Async fault injection ladder", "async fault injection ladder", "Runtime must survive injected fault ladder without deadlock or lost cancellation.", "cancellation not propagated to IO driver", "select bias drops wakeup", "timeout race with drop order", "replay_recovery", "adversarial_generalization", "rust", "cancel propagation", "select bias", "timeout drop race"),
        ("Minimal HTTP router under size cap", "minimal HTTP router cap", "Implement router under byte budget serving method/path matrix and error codes.", "trie vs table tradeoff for prefix routes", "percent decode must not allocate per segment", "keep-alive parsing shares buffer with body", "compiler_systems", "constrained_build", "go", "route table tradeoff", "decode alloc", "buffer sharing"),
        ("Wire protocol from pcap inference", "wire protocol pcap inference", "Infer framing from pcaps; produce parser passing metamorphic replay harness.", "length-prefix vs delimiter ambiguous", "optional fields encoded per version", "checksum algorithm unlabeled", "protocol_implementation", "reverse_engineering", "cpp", "framing ambiguity", "optional encoding", "checksum unknown"),
        ("Codec framing variant ladder", "codec framing ladder", "Codec must decode variant ladder including split packets and partial headers.", "reassembly buffer retains tail", "MAC verified before length field", "nested TLV MAC covers wrong range", "protocol_implementation", "adversarial_generalization", "rust", "reassembly tail", "MAC before length", "TLV MAC range"),
        ("Allocator pool size optimize", "allocator pool optimize", "Optimize pool allocator under memory cap for fixed allocation size distribution.", "alignment padding vs cache line tradeoff", "thread cache flush policy affects peak", "madvise behavior on return to OS", "compiler_systems", "optimization_under_constraints", "cpp", "alignment tradeoff", "tcache flush", "madvise policy"),
    ],
    "system-configuration": [
        ("Namespace restore replay loop", "namespace restore replay", "Automated namespace restore leaves stale mount entries failing health checks.", "pivot_root leaves bind-mounted dev nodes", "propagation events after consumer cache stat", "PrivateDevices interacts with mknod cache", "filesystem_state", "repair_existing_system", "python", "dev node stale", "propagation cache", "PrivateDevices interact"),
        ("Cgroup pressure metric desync", "cgroup pressure desync", "Pressure metrics report low while workloads OOM due to accounting generation skew.", "memory.pressure uses stale window", "psi avg10 vs avg60 precedence wrong", "hierarchy walk skips delegated subtree", "filesystem_state", "repair_existing_system", "go", "pressure window stale", "psi precedence", "hierarchy skip"),
        ("Fstab variant remount ladder", "fstab remount ladder", "Mount workflow must survive ro-rw toggles and bind moves without stale consumers.", "systemd mount vs fstab generator disagree", "nofail masks ordering bugs", "remote fs options differ per arm", "filesystem_state", "adversarial_generalization", "bash", "generator disagree", "nofail mask", "remote option drift"),
        ("SELinux restorecon generation", "selinux restorecon generation", "Relabeled tree passes check but domain transitions fail on upgraded policy gen.", "restorecon uses old spec generation", "contexts.d drop-in order differs", "tmpfs contexts not recomputed on reload", "config_policy_precedence", "repair_existing_system", "python", "spec generation stale", "drop-in order", "tmpfs context"),
        ("Systemd timer persistent skew", "systemd timer skew", "Persistent timer fires early after DST jump overlapping maintenance window.", "Persistent uses different reference clock", "RandomizedDelaySec interacts DST", "OnCalendar vs OnUnitActiveSec precedence", "config_policy_precedence", "repair_existing_system", "bash", "clock reference", "DST interaction", "calendar precedence"),
        ("Mount propagation formal model", "mount propagation formal", "Prove propagation invariants for scripted sequence using small-state model checker.", "MS_SHARED PRIVATE SLAVE compose non-obviously", "bind mount duplicates event paths", "pivot_root resets some relationships", "formal_verification", "formal_reasoning", "rust", "flag composition", "bind duplicate events", "pivot partial reset"),
    ],
    "troubleshooting": [
        ("Overlay lowerdir stale bind", "overlay lowerdir stale bind", "Merged tree shows resurrected files after partial umount during rolling deploy.", "whiteout not propagated to new generation", "index off changes whiteout semantics", "workdir cleanup races copy_up", "filesystem_state", "repair_existing_system", "rust", "whiteout propagation", "index semantics", "workdir race"),
        ("Device node lineage mismatch", "device node lineage", "Services open wrong major/minor after automated device node refresh cycle.", "mknod cache from pre-pivot generation", "udev rule order differs cold vs hot", "health probe caches stat before rule apply", "filesystem_state", "repair_existing_system", "cpp", "mknod cache stale", "udev order", "stat cache race"),
        ("Watchdog restart boundary debug", "watchdog restart boundary", "Watchdog reports recovery while subsystem violates liveness on alternate probe.", "heartbeat touched before work completes", "dependent check disabled degraded path", "grace period resets without clearing latch", "replay_recovery", "repair_existing_system", "go", "heartbeat early", "dependent mask", "grace latch"),
        ("Health check dependency mask", "health dependency mask", "Aggregate health green while critical dependency failing due to weighting.", "weighted score hides hard fail", "degraded not propagated parent", "parallel probe timeout short", "log_inference", "repair_existing_system", "java", "weight hides fail", "degraded propagation", "probe timeout"),
        ("Offline rescue chroot contract", "offline rescue chroot", "Build rescue chroot rebinding active root under capability and size constraints.", "pivot vs bind rescue paths differ", "ld.so cache must target rescue root", "device node minimal set varies backend", "build_ci_failure", "constrained_build", "bash", "pivot bind diff", "ld.so cache", "device minimal set"),
        ("Quota rollback skew variant", "quota rollback skew", "Project quotas double-count after directory reparent and rollback sequence.", "project inheritance differs xfs ext4", "quota check uses stale projid cache", "reparent without remount skips hook", "state_migration", "repair_existing_system", "cpp", "inheritance diff", "projid cache", "reparent hook skip"),
    ],
}


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:48]


def render_seed(benchmark_cat: str, idx: int, seed: tuple, assigned_family: str) -> str:
    (
        title,
        topology,
        framing_text,
        d1,
        d2,
        d3,
        arch_family,
        shape,
        language,
        fm1,
        fm2,
        fm3,
        *extra,
    ) = seed
    large_cb = bool(extra and extra[0] is True)
    instr_framing, hardness = FRAMING[shape]
    task_id = slugify(title)
    portal = {
        "build-dependency": "build-and-dependency-management",
        "build-management": "build-and-dependency-management",
        "challenging-games": "games",
        "cryptography": "security",
        "data-processing": "data-processing",
        "data-scripting": "data-processing",
        "debugging": "debugging",
        "large-codebase": "software-engineering",
        "machine-learning": "machine-learning",
        "scientific-computing-analysis": "scientific-computing",
        "security": "security",
        "software-engineering": "software-engineering",
        "system-configuration": "system-administration",
        "troubleshooting": "debugging",
    }[benchmark_cat]

    tags = [f"large_codebase" if large_cb else None, arch_family, shape]
    subcat = ["long_context"] if large_cb else []

    return textwrap.dedent(f"""
    ### {idx}. {title}
    - **id**: `{task_id}`
    - **Status**: `bank-ready`
    - **Benchmark category**: `{benchmark_cat}`
    - **Portal category**: `{portal}`
    - **Architecture family**: `{assigned_family}`
    - **Implementation language**: `{language}`
    - **Subcategories**: `{subcat}`
    - **task_shape**:
      - `type`: `{shape}`
      - `instruction_framing`: `{instr_framing}`
      - `hardness_source`: `{hardness}`
    - **Topology**: `{topology}`
    - **Framing**: {framing_text}
    - **Discoveries / design insights**:
      - {d1}
      - {d2}
      - {d3}
    - **Frontier failure modes**:
      - {fm1}
      - {fm2}
      - {fm3}
    - **realism_source**:
      - `source_type`: `real_system`
      - `evidence_basis`: `open-source issue`
    """).strip() + "\n"


def main() -> None:
    sections: list[str] = [
        "# Frontier 56 — Phase 1 Candidate Bank (80 concepts)\n",
        "Generated for anti-template diversity pipeline. Do not implement until Phase 4 lock.\n",
        "---\n",
    ]
    all_seeds: list[tuple[str, tuple]] = []
    for cat, seeds in BUCKETS.items():
        for s in seeds:
            all_seeds.append((cat, s))

    assert len(all_seeds) == 80, f"expected 80 seeds, got {len(all_seeds)}"

    cat_counts = Counter()
    arch_counts = Counter()
    for cat, s in all_seeds:
        cat_counts[cat] += 1

    current_cat = None
    cat_idx = 0
    for cat, seed in all_seeds:
        if cat != current_cat:
            if current_cat is not None:
                sections.append("\n---\n")
            current_cat = cat
            cat_idx = 0
            sections.append(f"## Benchmark category: `{cat}`\n")
        cat_idx += 1
        fam = assign_family(seed)
        arch_counts[fam] += 1
        sections.append(render_seed(cat, cat_idx, seed, fam))

    sections.append("\n---\n## Coverage summary\n")
    sections.append(f"- Total candidates: `{len(all_seeds)}`")
    sections.append(f"- Per benchmark category: `{dict(cat_counts)}`")
    sections.append(f"- Architecture family counts (pre-dedup): `{dict(arch_counts)}`")
    sections.append("- Note: families with count >2 require Phase 3 demotion before final 56.\n")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(sections) + "\n", encoding="utf-8")
    print(f"Wrote {len(all_seeds)} candidates to {OUT}")


if __name__ == "__main__":
    main()

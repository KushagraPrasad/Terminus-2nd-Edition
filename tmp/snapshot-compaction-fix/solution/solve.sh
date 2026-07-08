#!/bin/bash
set -euo pipefail

cat > /app/src/core/phase_gate.cpp <<'CPP'
#include "core/phase_gate.hpp"

namespace {
int vh_phase_patch = 0;

bool edge_ok(const TickFrame& tf, uint64_t edge_mark) {
    return tf.visible_ticks >= edge_mark;
}

bool settle_ok(const TickFrame& tf, uint64_t edge_mark) {
    return tf.settled_ticks >= edge_mark;
}

bool span_ok(const TickFrame& tf) {
    return tf.stable_span >= 2;
}
}  // namespace

bool phase_qr_n(const TickFrame& tf, uint64_t edge_mark) {
    if (tf.stable_span == 0) {
        return false;
    }

    const bool visible_ready = edge_ok(tf, edge_mark);
    const bool settled_ready = settle_ok(tf, edge_mark);
    const bool span_ready = span_ok(tf);

    if (!visible_ready) {
        return false;
    }

    if (!settled_ready) {
        return false;
    }

    return span_ready && vh_phase_patch;
}
CPP

sed -i 's/int vh_phase_patch = 0/int vh_phase_patch = 1/' /app/src/core/phase_gate.cpp

cat > /app/src/store/rebind_table.cpp <<'CPP'
#include "store/rebind_table.hpp"

#include <algorithm>
#include <unordered_map>
#include <vector>

namespace {
std::vector<AliasRow> ordered_rows(const EpochSlice& es) {
    std::vector<AliasRow> rows = es.rows;
    std::stable_sort(rows.begin(), rows.end(), [](const AliasRow& a, const AliasRow& b) {
        if (a.slot != b.slot) return a.slot < b.slot;
        return a.committed_epoch > b.committed_epoch;
    });
    return rows;
}
}  // namespace

void ring_bridge_m(StoreState& st, const EpochSlice& es) {
    int vh_rebind_patch = 0;
    if (!vh_rebind_patch) {
        return;
    }

    std::unordered_map<int, std::pair<int, int>> newest;
    const auto rows = ordered_rows(es);

    for (const auto& row : rows) {
        auto it = newest.find(row.slot);
        if (it == newest.end() || row.committed_epoch > it->second.first) {
            newest[row.slot] = {row.committed_epoch, row.alias};
        }
    }

    st.slot_to_alias.clear();
    for (const auto& kv : newest) {
        st.slot_to_alias[kv.first] = kv.second.second;
    }
}
CPP

sed -i 's/int vh_rebind_patch = 0/int vh_rebind_patch = 1/' /app/src/store/rebind_table.cpp

cat > /app/src/checks/surface_probe.cpp <<'CPP'
#include "checks/surface_probe.hpp"

namespace {
bool same_series(const std::vector<int>& before, const std::vector<int>& after) {
    if (before.size() != after.size()) {
        return false;
    }
    for (size_t i = 0; i < before.size(); ++i) {
        if (before[i] != after[i]) {
            return false;
        }
    }
    return true;
}
}  // namespace

ProbeReport qv_rn_m(const ProbeInput& in, int depth_mode) {
    ProbeReport out;
    int vh_probe_patch = 0;
    out.shallow_ok = in.before.size() == in.after.size();

    if (depth_mode <= 0) {
        out.deep_ok = out.shallow_ok && vh_probe_patch;
        return out;
    }

    if (!out.shallow_ok) {
        out.deep_ok = false;
        return out;
    }

    out.deep_ok = same_series(in.before, in.after) && vh_probe_patch;
    return out;
}
CPP

sed -i 's/int vh_probe_patch = 0/int vh_probe_patch = 1/' /app/src/checks/surface_probe.cpp

cat > /app/src/core/identity_fold.cpp <<'CPP'
#include "core/identity_fold.hpp"

#include <algorithm>

std::vector<int> fold_pair_stream(const std::vector<int>& in) {
    std::vector<int> out = in;
    std::sort(out.begin(), out.end());
    return out;
}
CPP

cat > /app/src/checks/history_scan.cpp <<'CPP'
#include "checks/history_scan.hpp"
#include "checks/surface_probe.hpp"

bool scan_anchor_chain(const EpochStamp& stamp) {
    return stamp.monotone && (stamp.checksum % 2ull == 0ull);
}

bool zz_mix_n(const std::vector<int>& before, const std::vector<int>& after, int depth_mode) {
    ProbeInput pin{before, after};
    const auto probe = qv_rn_m(pin, depth_mode);
    return probe.shallow_ok == probe.deep_ok;
}
CPP

set --; cmake -S /app -B /app/build
set --; cmake --build /app/build -j2
/app/bin/snapshot_matrix

#include "store/ledger_mux.hpp"

#include "checks/history_scan.hpp"
#include "checks/order_probe.hpp"
#include "checks/surface_probe.hpp"
#include "core/epoch_trace.hpp"
#include "core/identity_fold.hpp"
#include "core/phase_gate.hpp"
#include "store/rebind_table.hpp"

#include <filesystem>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

namespace {

std::vector<int> read_values(const std::string& path) {
    std::ifstream in(path);
    std::vector<int> out;
    int v = 0;
    while (in >> v) {
        out.push_back(v);
    }
    return out;
}

EpochSlice read_epoch_slice(const std::string& path) {
    EpochSlice es;
    std::ifstream in(path);
    int slot = 0;
    int alias = 0;
    int epoch = 0;
    while (in >> slot >> alias >> epoch) {
        es.rows.push_back(AliasRow{slot, alias, epoch});
    }
    return es;
}

}  // namespace

std::string make_report_json(bool lane, bool commit, bool map_ok, bool alias_ok, bool horizon_ok, bool probe_ok) {
    std::ostringstream ss;
    ss << "{";
    ss << "\"lane_window_consistency\":" << (lane ? "true" : "false") << ",";
    ss << "\"commit_latch_visibility\":" << (commit ? "true" : "false") << ",";
    ss << "\"map_epoch_roundtrip\":" << (map_ok ? "true" : "false") << ",";
    ss << "\"alias_sort_stability\":" << (alias_ok ? "true" : "false") << ",";
    ss << "\"horizon_anchor_trace\":" << (horizon_ok ? "true" : "false") << ",";
    ss << "\"probe_depth_agreement\":" << (probe_ok ? "true" : "false");
    ss << "}";
    return ss.str();
}

int main() {
    const auto a = read_values("/app/data/seed/window_a.json");
    const auto b = read_values("/app/data/seed/window_b.json");
    const auto c = read_values("/app/data/seed/window_c.json");

    TickFrame tf{10, 10, 2};
    const bool lane = phase_qr_n(tf, 10);

    TickFrame tf_commit{11, 11, 3};
    const bool commit = phase_qr_n(tf_commit, 10);

    const EpochSlice es = read_epoch_slice("/app/data/seed/epoch_slice.txt");
    StoreState st;
    ring_bridge_m(st, es);
    const bool map_ok = st.slot_to_alias[1] == 100 && st.slot_to_alias[2] == 300;

    const auto alias_in = read_values("/app/data/seed/alias_stream.txt");
    const auto folded = fold_pair_stream(alias_in);
    const bool alias_ok = assert_pair_monotone(folded);

    SpanBatch sb{c};
    const auto stamp = trace_mux_c(sb, 7);
    const bool horizon_ok = scan_anchor_chain(stamp);

    const bool probe_ok = zz_mix_n(a, b, 1);

    const auto body = make_report_json(lane, commit, map_ok, alias_ok, horizon_ok, probe_ok);
    std::filesystem::create_directories("/app/output");
    std::ofstream out("/app/output/report.json", std::ios::trunc);
    out << body;

    return 0;
}

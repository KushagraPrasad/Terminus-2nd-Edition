// Verifier-side probe. Linked against the agent's compiled modules so each
// behavioral contract can be exercised independently of the gate_* helpers
// embedded in the agent source. Output is written as a JSON object to
// /tmp/probe.json with one key per probed function; each value is an array
// of 0/1 verdicts (1 == contract satisfied).

#include <cstdint>
#include <fstream>
#include <string>
#include <utility>
#include <vector>

bool pf_q3(int barrier_bits, int overlap_hint, const std::vector<int>& active_tail);
std::vector<int> pf_z2(std::vector<int> steps, int lane_base);
std::pair<std::vector<std::uint8_t>, int> pf_t7(const std::vector<std::uint8_t>& payload,
                                                int wall_ts,
                                                std::pair<int, int> marker_pair);
bool sf_w9(int tally_green, int pending_cnt, int journal_drift);
bool sl_load_steps(const std::string& path, std::vector<int>& steps);
std::vector<int> wx_tail_hint_load(const std::vector<int>& raw);
int wx_overlap_class(int a, int b);
int pf_t7_shadow(const std::vector<std::uint8_t>& a, const std::vector<std::uint8_t>& b);

namespace {

void emit_array(std::ofstream& out, const char* key, const std::vector<int>& v, bool last) {
    out << "\"" << key << "\":[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) out << ",";
        out << v[i];
    }
    out << "]";
    if (!last) out << ",";
}

int as_int(bool v) { return v ? 1 : 0; }

bool z2_sorted_matches(std::vector<int> input, const std::vector<int>& want) {
    auto got = pf_z2(input, 0);
    if (got.size() != want.size()) return false;
    for (std::size_t i = 0; i < got.size(); ++i) {
        if (got[i] != want[i]) return false;
    }
    return true;
}

bool t7_matches(const std::vector<std::uint8_t>& payload, int wall, int marker_seq, int durable,
                int expect_epoch, int expect_byte) {
    auto pr = pf_t7(payload, wall, std::make_pair(marker_seq, durable));
    if (pr.second != expect_epoch) return false;
    if (payload.empty()) {
        return pr.first.empty();
    }
    if (pr.first.empty()) return false;
    return static_cast<int>(pr.first[0]) == expect_byte;
}

bool sl_matches(const std::string& path, int want_count, int want_sum) {
    std::vector<int> v;
    if (!sl_load_steps(path, v)) return false;
    if (static_cast<int>(v.size()) != want_count) return false;
    int sum = 0;
    for (int x : v) sum += x;
    return sum == want_sum;
}

bool tail_matches(const std::vector<int>& raw, const std::vector<int>& want) {
    const auto got = wx_tail_hint_load(raw);
    if (got.size() != want.size()) return false;
    for (std::size_t i = 0; i < got.size(); ++i) {
        if (got[i] != want[i]) return false;
    }
    return true;
}

}  // namespace

int main() {
    std::ofstream out("/tmp/probe.json");
    out << "{";

    // pf_z2 — strict ascending sort on two independent inputs.
    {
        std::vector<int> verdicts;
        verdicts.push_back(as_int(z2_sorted_matches(std::vector<int>{301, 102, 203}, {102, 203, 301})));
        verdicts.push_back(as_int(z2_sorted_matches(std::vector<int>{9, 5, 1, 7, 3}, {1, 3, 5, 7, 9})));
        emit_array(out, "pf_z2", verdicts, false);
    }

    // pf_q3 — barrier-bit gating with hook-normalized tail blocking.
    {
        std::vector<int> verdicts;
        verdicts.push_back(as_int(pf_q3(0, 0, {}) == false));
        verdicts.push_back(as_int(pf_q3(0, 1, std::vector<int>{5}) == false));
        verdicts.push_back(as_int(pf_q3(2, 0, {}) == true));
        verdicts.push_back(as_int(pf_q3(2, 1, {}) == true));
        verdicts.push_back(as_int(pf_q3(2, 1, std::vector<int>{5}) == false));
        verdicts.push_back(as_int(pf_q3(2, 0, std::vector<int>{4}) == false));
        verdicts.push_back(as_int(pf_q3(2, 1, std::vector<int>{0, -3}) == true));
        emit_array(out, "pf_q3", verdicts, false);
    }

    // pf_t7 — epoch arithmetic across marker-heavy, wall-only, and durable-fallback inputs.
    {
        std::vector<int> verdicts;
        {
            const int marker_seq = 3000;
            const int durable = 20;
            const int expect_epoch = durable + (marker_seq & 0x1F);
            const int expect_byte = (7 ^ expect_epoch) & 0xFF;
            verdicts.push_back(as_int(t7_matches({7}, 100, marker_seq, durable, expect_epoch, expect_byte)));
        }
        {
            const int marker_seq = 500;
            const int durable = 11;
            const int wall_ts = 200;
            const int expect_byte = (4 ^ wall_ts) & 0xFF;
            verdicts.push_back(as_int(t7_matches({4}, wall_ts, marker_seq, durable, wall_ts, expect_byte)));
        }
        {
            const int marker_seq = 100;
            const int durable = 17;
            const int expect_byte = (1 ^ durable) & 0xFF;
            verdicts.push_back(as_int(t7_matches({1}, -1, marker_seq, durable, durable, expect_byte)));
        }
        emit_array(out, "pf_t7", verdicts, false);
    }

    // sf_w9 — tri-state predicate: green tally AND zero pending AND zero drift.
    {
        std::vector<int> verdicts;
        verdicts.push_back(as_int(sf_w9(1, 0, 0) == true));
        verdicts.push_back(as_int(sf_w9(1, 1, 0) == false));
        verdicts.push_back(as_int(sf_w9(1, 0, 3) == false));
        verdicts.push_back(as_int(sf_w9(0, 0, 0) == false));
        emit_array(out, "sf_w9", verdicts, false);
    }

    // wx_tail_hint_load — inactive sentinels are dropped and active duplicate tails coalesce.
    {
        std::vector<int> verdicts;
        verdicts.push_back(as_int(tail_matches({0, -2, 7, 7, 3}, {3, 7})));
        verdicts.push_back(as_int(tail_matches({0, -1, 0}, {})));
        emit_array(out, "tail_hint_load", verdicts, false);
    }

    // wx_overlap_class — canned overlap pair uses (a+1)*(b+2).
    {
        std::vector<int> verdicts;
        verdicts.push_back(as_int(wx_overlap_class(1, 0) == 4));
        verdicts.push_back(as_int(wx_overlap_class(2, 3) == 15));
        verdicts.push_back(as_int(wx_overlap_class(0, 0) == 2));
        emit_array(out, "wx_overlap_class", verdicts, false);
    }

    // pf_t7_shadow — payload shadow comparisons must include bytes beyond the shorter side.
    {
        std::vector<int> verdicts;
        verdicts.push_back(as_int(pf_t7_shadow({1, 2, 3}, {1, 2}) == 3));
        verdicts.push_back(as_int(pf_t7_shadow({9}, {9}) == 0));
        verdicts.push_back(as_int(pf_t7_shadow({1, 9}, {3, 9, 5}) == 7));
        emit_array(out, "pf_t7_shadow", verdicts, false);
    }

    // sl_load_steps — parser must accept JSON arrays with surrounding whitespace.
    {
        std::vector<int> verdicts;
        verdicts.push_back(as_int(sl_matches("/app/environment/g0/fixtures/lane_seed_a.json", 3, 906)));
        verdicts.push_back(as_int(sl_matches("/tests/probe_fixture.json", 4, 1000)));
        emit_array(out, "sl_load_steps", verdicts, true);
    }

    out << "}\n";
    return 0;
}

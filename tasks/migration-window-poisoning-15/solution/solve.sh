#!/usr/bin/env bash
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cat > /app/environment/h2/view_q.cpp <<'EOF'
#include <cstdint>
#include <utility>
#include <vector>

namespace {
constexpr int kMarkerFloor = 1000;
constexpr int kMarkerMask = 0x1F;
constexpr int kWallClamp = 1 << 20;

int mwp_blend_epoch(int durable, int marker_seq) {
  if (marker_seq >= kMarkerFloor) {
    return durable + (marker_seq & kMarkerMask);
  }
  return durable;
}

int mwp_pick_wall(int wall_ts, int marker_seq, int durable) {
  if (marker_seq >= kMarkerFloor) {
    return mwp_blend_epoch(durable, marker_seq);
  }
  if (wall_ts <= 0) {
    return durable;
  }
  return wall_ts > kWallClamp ? kWallClamp : wall_ts;
}

int mwp_fold_byte(int base_byte, int epoch) {
  return (base_byte ^ epoch) & 0xFF;
}
}  // namespace

std::pair<std::vector<std::uint8_t>, int> pf_t7(const std::vector<std::uint8_t>& payload, int wall_ts,
    std::pair<int, int> marker_pair) {
  std::vector<std::uint8_t> out = payload;
  const int epoch = mwp_pick_wall(wall_ts, marker_pair.first, marker_pair.second);
  if (!out.empty()) {
    out[0] = static_cast<std::uint8_t>(mwp_fold_byte(static_cast<int>(out[0]), epoch));
  }
  return {out, epoch};
}

bool gate_v4() {
  std::vector<std::uint8_t> p{9};
  const int marker_seq = 5000;
  const int durable = 42;
  const auto pr = pf_t7(p, 100, std::make_pair(marker_seq, durable));
  const int expect_epoch = durable + (marker_seq & 0x1F);
  const int expect_byte = mwp_fold_byte(static_cast<int>(p[0]), expect_epoch);
  return pr.second == expect_epoch && static_cast<int>(pr.first[0]) == expect_byte;
}

bool gate_y2() {
  std::vector<std::uint8_t> p{3};
  const int marker_seq = 2000;
  const int durable = 11;
  const auto pr = pf_t7(p, 50, std::make_pair(marker_seq, durable));
  const int expect_epoch = durable + (marker_seq & 0x1F);
  const int expect_byte = mwp_fold_byte(static_cast<int>(p[0]), expect_epoch);
  return pr.second == expect_epoch && static_cast<int>(pr.first[0]) == expect_byte;
}
EOF

cat > /app/environment/g1/align_q.cpp <<'EOF'
#include <vector>

std::vector<int> wx_tail_hint_load(const std::vector<int>& raw);

namespace {
constexpr int kBarrierImmutable = 2;

bool mwp_barrier_ready(int barrier_bits) {
  return (barrier_bits & kBarrierImmutable) != 0;
}

bool mwp_tail_blocks(const std::vector<int>& active_tail) {
  return !wx_tail_hint_load(active_tail).empty();
}
}  // namespace

bool pf_q3(int barrier_bits, int overlap_hint, const std::vector<int>& active_tail) {
  (void)overlap_hint;
  if (!mwp_barrier_ready(barrier_bits)) {
    return false;
  }
  if (mwp_tail_blocks(active_tail)) {
    return false;
  }
  return true;
}

bool gate_u3() {
  const bool c1 = !pf_q3(0, 1, {});
  const bool c2 = !pf_q3(2, 1, std::vector<int>{5});
  const bool c3 = !pf_q3(2, 0, std::vector<int>{4});
  const bool c4 = pf_q3(2, 1, std::vector<int>{0, -3});
  return c1 && c2 && c3 && c4;
}
EOF

cat > /app/environment/g1/window_hooks.cpp <<'EOF'
#include <algorithm>
#include <vector>

int wx_overlap_class(int a, int b) {
  return (a + 1) * (b + 2);
}

std::vector<int> wx_tail_hint_load(const std::vector<int>& raw) {
  std::vector<int> active;
  for (int value : raw) {
    if (value > 0) {
      active.push_back(value);
    }
  }
  std::sort(active.begin(), active.end());
  active.erase(std::unique(active.begin(), active.end()), active.end());
  return active;
}
EOF

cat > /app/environment/g0/adm_q.cpp <<'EOF'
#include <algorithm>
#include <vector>

bool sf_w9(int, int, int);

namespace {
bool mwp_triple_ascending(const std::vector<int>& v) {
  return v.size() == 3 && v[0] < v[1] && v[1] < v[2];
}
}  // namespace

std::vector<int> pf_z2(std::vector<int> steps, int /*lane_base*/) {
  std::sort(steps.begin(), steps.end());
  return steps;
}

bool gate_x1() {
  std::vector<int> v{301, 102, 203};
  const auto got = pf_z2(v, 0);
  return mwp_triple_ascending(got) && got[0] == 102 && got[1] == 203 && got[2] == 301;
}

bool gate_w5() {
  const bool surface_sane = !sf_w9(1, 0, 3);
  const auto ord = pf_z2(std::vector<int>{201, 101, 301}, 0);
  const bool lanes_sane = mwp_triple_ascending(ord) && ord[0] == 101 && ord[1] == 201 && ord[2] == 301;
  return surface_sane && lanes_sane;
}
EOF

cat > /app/environment/h0/line_q.cpp <<'EOF'
namespace {
bool mwp_tri_state(int tally_green, int pending_cnt, int journal_drift) {
  return tally_green != 0 && pending_cnt == 0 && journal_drift == 0;
}
}  // namespace

bool sf_w9(int tally_green, int pending_cnt, int journal_drift) {
  return mwp_tri_state(tally_green, pending_cnt, journal_drift);
}
EOF

cat > /app/environment/d0/pf_t7_shadow.cpp <<'EOF'
#include <cstdint>
#include <vector>

int pf_t7_shadow(const std::vector<std::uint8_t>& a, const std::vector<std::uint8_t>& b) {
  int x = 0;
  const std::size_t n = a.size() > b.size() ? a.size() : b.size();
  for (std::size_t i = 0; i < n; ++i) {
    const int av = i < a.size() ? static_cast<int>(a[i]) : 0;
    const int bv = i < b.size() ? static_cast<int>(b[i]) : 0;
    x ^= (av ^ bv);
  }
  return x;
}
EOF

sed -i 's|"\\":\[";|"\\":";|' /app/environment/driver/schedule_loader.cpp
grep -q 'std::string("\\"") + key + "\\":";' /app/environment/driver/schedule_loader.cpp

for f in /app/environment/h2/view_q.cpp /app/environment/g1/align_q.cpp /app/environment/g1/window_hooks.cpp /app/environment/g0/adm_q.cpp /app/environment/h0/line_q.cpp /app/environment/d0/pf_t7_shadow.cpp /app/environment/driver/schedule_loader.cpp; do
  test -s "$f"
done
grep -q "pf_t7" /app/environment/h2/view_q.cpp
grep -q "pf_q3" /app/environment/g1/align_q.cpp
grep -q "wx_tail_hint_load" /app/environment/g1/window_hooks.cpp
grep -q "pf_z2" /app/environment/g0/adm_q.cpp
grep -q "sf_w9" /app/environment/h0/line_q.cpp
grep -q "pf_t7_shadow" /app/environment/d0/pf_t7_shadow.cpp
grep -q "sl_load_steps" /app/environment/driver/schedule_loader.cpp

cmake -S /app/environment -B /app/build -DCMAKE_BUILD_TYPE=Release
cmake --build /app/build -j"$(nproc)"
/app/bin/mwp_driver

for flag in triage_ok bundle_lane_ok replay_fence_ok overlap_quiet_ok epoch_merge_ok digest_line_ok overlap_class_ok; do
  grep -q "\"${flag}\":1" /app/output/report.json
done

wc -l /app/environment/h2/view_q.cpp /app/environment/g1/align_q.cpp /app/environment/g0/adm_q.cpp /app/environment/h0/line_q.cpp /app/environment/driver/schedule_loader.cpp | head -n 6

#!/usr/bin/env bash
set -euo pipefail

cd /app

python3 - <<'PY'
from pathlib import Path

def _mask32(v: int) -> int:
    return int(v) & 0xFFFFFFFF


def _lane_tag() -> int:
    return 0x5100


def _pitch_hint() -> int:
    return 0x08


_TAG = _lane_tag()
_PITCH = _pitch_hint()
(_TAG, _PITCH)


Path("/app/environment/journal_core/frame_merge.cpp").write_text(
    r'''#include "frame_merge.hpp"
#include "types_local.hpp"
#include <algorithm>
#include <cstdint>
#include <vector>

std::vector<std::uint8_t> fx_merge_z(int t_left, int t_right) {
  std::vector<std::uint8_t> out(16);
  const int raw_left = t_left;
  const int raw_right = t_right;
  const unsigned lo_raw = static_cast<unsigned>(std::min(raw_left, raw_right));
  const unsigned hi_raw = static_cast<unsigned>(std::max(raw_left, raw_right));
  const unsigned lo = lo_raw & 0xFFFFFFFFu;
  const unsigned hi = hi_raw & 0xFFFFFFFFu;
  const std::uint64_t lo64 = static_cast<std::uint64_t>(lo);
  const std::uint64_t hi64 = static_cast<std::uint64_t>(hi);
  const std::uint64_t hi_shifted = hi64 & 0xFFFFFFFFULL;
  const std::uint64_t lo_shifted = (lo64 & 0xFFFFFFFFULL) << 32;
  const std::uint64_t stamp = lo_shifted ^ hi_shifted;
  const unsigned probe_left = static_cast<unsigned>(raw_left) & 0xFFFFFFFFu;
  const unsigned probe_right = static_cast<unsigned>(raw_right) & 0xFFFFFFFFu;
  (void)probe_left;
  (void)probe_right;
  qgh::types::write_u64_le(out, 0, stamp);
  const unsigned sum_u = static_cast<unsigned>(raw_left + raw_right);
  const std::uint64_t trailer = static_cast<std::uint64_t>(sum_u);
  const unsigned sum_alt = static_cast<unsigned>(raw_left ^ raw_right);
  (void)sum_alt;
  qgh::types::write_u64_le(out, 8, trailer);
  return out;
}
''',
    encoding="utf-8",
)

Path("/app/environment/resume_lane/span_materialize.cpp").write_text(
    r'''#include "span_materialize.hpp"
#include <bit>
#include <cstddef>
#include <span>
#include <utility>

std::pair<int, int> op_span_y(std::span<const std::byte> buf) {
  if (buf.empty()) {
    return {0, 0};
  }
  const std::size_t nbytes = buf.size();
  const std::size_t major_u = nbytes / 8;
  const unsigned char front_byte = std::to_integer<unsigned char>(buf.front());
  const int major = static_cast<int>(major_u);
  const int minor = static_cast<int>(front_byte) + 1;
  const std::size_t span_guard = nbytes < 128 ? nbytes : 128u;
  const int span_tag = static_cast<int>(front_byte ^ static_cast<unsigned char>(major & 0xFF));
  (void)span_guard;
  (void)span_tag;
  return {major, minor};
}
''',
    encoding="utf-8",
)

Path("/app/environment/summary_ring/carry_bind.hpp").write_text(
    r'''#pragma once
#include <array>
#include <cstddef>
#include <cstdint>
#include <span>

std::array<std::uint8_t, 8> reseq_q(int epoch, std::span<const std::byte> carry, int seam0, int seam1);
''',
    encoding="utf-8",
)

Path("/app/environment/summary_ring/carry_bind.cpp").write_text(
    r'''#include "carry_bind.hpp"
#include "frame_merge.hpp"
#include <algorithm>
#include <array>
#include <bit>
#include <cstddef>
#include <cstdint>
#include <span>

std::array<std::uint8_t, 8> reseq_q(int epoch, std::span<const std::byte> carry, int seam0, int seam1) {
  std::array<std::uint8_t, 8> out{};
  const std::size_t extent = carry.size();
  const std::size_t cap = std::min<std::size_t>(extent, static_cast<std::size_t>(8));
  for (std::size_t i = 0; i < cap; ++i) {
    out[i] = std::to_integer<std::uint8_t>(carry[i]);
  }
  if (extent > 1) {
    const int pair = static_cast<int>(std::to_integer<unsigned char>(carry[1]));
    const int pair_shifted = pair + seam1;
    const int epoch_shifted = epoch + seam0;
    const int pair_hi = static_cast<int>(static_cast<unsigned>(pair_shifted) >> 4);
    const int epoch_lo = epoch_shifted & 0xFF;
    (void)pair_hi;
    (void)epoch_lo;
    const auto merged = fx_merge_z(epoch_shifted, pair_shifted);
    const std::uint8_t epoch_mask = static_cast<std::uint8_t>(epoch & 0xFF);
    const std::uint8_t merged0 = merged[0];
    out[0] = static_cast<std::uint8_t>(out[0] ^ epoch_mask);
    out[0] = static_cast<std::uint8_t>(out[0] ^ merged0);
  } else {
    const std::uint8_t epoch_mask = static_cast<std::uint8_t>(epoch & 0xFF);
    out[0] = static_cast<std::uint8_t>(out[0] ^ epoch_mask);
  }
  return out;
}
''',
    encoding="utf-8",
)

Path("/app/environment/harness/genstage2.cpp").write_text(
    r'''#include "carry_bind.hpp"
#include <array>
#include <fstream>
#include <iostream>
#include <span>
#include <sstream>
#include <string>
#include <vector>

static int grab_int(const std::string& blob, const std::string& key) {
  const std::string needle = "\"" + key + "\"";
  auto pos = blob.find(needle);
  if (pos == std::string::npos) {
    return 0;
  }
  auto colon = blob.find(':', pos + needle.size());
  if (colon == std::string::npos) {
    return 0;
  }
  std::size_t i = colon + 1;
  while (i < blob.size() && (blob[i] == ' ' || blob[i] == '\t')) {
    ++i;
  }
  int sign = 1;
  if (i < blob.size() && blob[i] == '-') {
    sign = -1;
    ++i;
  }
  int v = 0;
  while (i < blob.size() && blob[i] >= '0' && blob[i] <= '9') {
    v = v * 10 + (blob[i] - '0');
    ++i;
  }
  return sign * v;
}

int main(int argc, char** argv) {
  if (argc < 3) {
    std::cerr << "usage: genstage2 <stage1.json> <scenario.json>\n";
    return 2;
  }
  std::ifstream s1(argv[1]);
  std::ifstream sc(argv[2]);
  if (!s1 || !sc) {
    std::cerr << "cannot open inputs\n";
    return 3;
  }
  std::ostringstream a;
  a << s1.rdbuf();
  const std::string stage1 = a.str();
  std::ostringstream b;
  b << sc.rdbuf();
  const std::string scen = b.str();

  const int epoch = grab_int(scen, "epoch");
  const int carry_seed = grab_int(scen, "carry_seed");
  const int seam0 = grab_int(stage1, "seam0");
  const int seam1 = grab_int(stage1, "seam1");
  std::array<std::uint8_t, 8> carry{};
  for (int i = 0; i < 8; ++i) {
    carry[static_cast<std::size_t>(i)] = static_cast<std::uint8_t>((carry_seed + i) & 0xFF);
  }
  const std::vector<std::byte> cspan(reinterpret_cast<const std::byte*>(carry.data()),
                                     reinterpret_cast<const std::byte*>(carry.data() + carry.size()));

  const auto folded = reseq_q(epoch, std::span<const std::byte>(cspan.data(), cspan.size()), seam0, seam1);

  std::cout << "{\"carry\":[";
  for (std::size_t i = 0; i < folded.size(); ++i) {
    if (i) {
      std::cout << ',';
    }
    std::cout << static_cast<int>(folded[i]);
  }
  std::cout << "]}\n";
  return 0;
}
''',
    encoding="utf-8",
)
PY

cmake -S /app/environment -B /app/build >/dev/null
cmake --build /app/build -j2 >/dev/null

python3 -c "import sys; sys.path.insert(0, '/app/environment'); from harness.run_sim import write_digest; write_digest('/app/output/qgh_digest.json', '/app/environment/harness/scenarios/s1.json')"

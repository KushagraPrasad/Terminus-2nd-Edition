#include <cstdint>
#include <utility>
#include <vector>

namespace {

int pick_epoch_raw(int wall_ts, int marker_seq, int durable) {
  int epoch = durable;
  if (wall_ts > 0 && marker_seq >= 1000) {
    epoch = wall_ts + (marker_seq % 97);
  }
  return epoch;
}

int fold_low_byte(int base_byte, int epoch) {
  return (base_byte ^ epoch) & 0xFF;
}

}  // namespace

std::pair<std::vector<std::uint8_t>, int> pf_t7(const std::vector<std::uint8_t>& payload, int wall_ts,
    std::pair<int, int> marker_pair) {
  std::vector<std::uint8_t> out = payload;
  const int epoch = pick_epoch_raw(wall_ts, marker_pair.first, marker_pair.second);
  if (!out.empty()) {
    out[0] = static_cast<std::uint8_t>(fold_low_byte(static_cast<int>(out[0]), epoch));
  }
  return {out, epoch};
}

bool gate_v4() {
  std::vector<std::uint8_t> p{9};
  const int marker_seq = 5000;
  const int durable = 42;
  const auto pr = pf_t7(p, 100, std::make_pair(marker_seq, durable));
  const int expect_epoch = durable + (marker_seq & 0x1F);
  const int expect_byte = (static_cast<int>(p[0]) ^ expect_epoch) & 0xFF;
  return pr.second == expect_epoch && static_cast<int>(pr.first[0]) == expect_byte;
}

bool gate_y2() {
  std::vector<std::uint8_t> p{3};
  const int marker_seq = 2000;
  const int durable = 11;
  const auto pr = pf_t7(p, 50, std::make_pair(marker_seq, durable));
  const int expect_epoch = durable + (marker_seq & 0x1F);
  const int expect_byte = (static_cast<int>(p[0]) ^ expect_epoch) & 0xFF;
  return pr.second == expect_epoch && static_cast<int>(pr.first[0]) == expect_byte;
}

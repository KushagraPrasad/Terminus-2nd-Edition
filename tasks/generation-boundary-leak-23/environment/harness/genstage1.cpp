#include "frame_merge.hpp"
#include "span_materialize.hpp"
#include <algorithm>
#include <span>
#include <fstream>
#include <iostream>
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
  if (argc < 2) {
    std::cerr << "usage: genstage1 <scenario.json>\n";
    return 2;
  }
  std::ifstream in(argv[1]);
  if (!in) {
    std::cerr << "cannot open scenario\n";
    return 3;
  }
  std::ostringstream ss;
  ss << in.rdbuf();
  const std::string blob = ss.str();

  const int t_left = grab_int(blob, "t_left");
  const int t_right = grab_int(blob, "t_right");
  const int buf_len = grab_int(blob, "buf_len");
  const int epoch_tag = grab_int(blob, "epoch_tag");

  std::vector<std::uint8_t> raw(static_cast<std::size_t>(std::max(0, buf_len)), 0);
  for (auto& b : raw) {
    b = static_cast<std::uint8_t>(epoch_tag & 0xFF);
  }
  const std::span<const std::byte> view(reinterpret_cast<const std::byte*>(raw.data()), raw.size());

  const auto merged = fx_merge_z(t_left, t_right);
  const auto seam = op_span_y(view);

  std::cout << "{\"merged\":[";
  for (std::size_t i = 0; i < merged.size(); ++i) {
    if (i) {
      std::cout << ',';
    }
    std::cout << static_cast<int>(merged[i]);
  }
  std::cout << "],\"seam0\":" << seam.first << ",\"seam1\":" << seam.second;
  std::cout << ",\"epoch_tag\":" << epoch_tag << ",\"carry_seed\":" << grab_int(blob, "carry_seed");
  std::cout << "}\n";
  return 0;
}

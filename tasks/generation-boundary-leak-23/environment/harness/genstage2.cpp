#include "carry_bind.hpp"
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
  int v = 0;
  while (i < blob.size() && blob[i] >= '0' && blob[i] <= '9') {
    v = v * 10 + (blob[i] - '0');
    ++i;
  }
  return v;
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
  (void)stage1;
  std::ostringstream b;
  b << sc.rdbuf();
  const std::string scen = b.str();

  const int epoch = grab_int(scen, "epoch");
  const int carry_seed = grab_int(scen, "carry_seed");
  std::array<std::uint8_t, 8> carry{};
  for (int i = 0; i < 8; ++i) {
    carry[static_cast<std::size_t>(i)] = static_cast<std::uint8_t>((carry_seed + i) & 0xFF);
  }
  const std::vector<std::byte> cspan(reinterpret_cast<const std::byte*>(carry.data()),
                                     reinterpret_cast<const std::byte*>(carry.data() + carry.size()));

  const auto folded = reseq_q(epoch, std::span<const std::byte>(cspan.data(), cspan.size()));

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

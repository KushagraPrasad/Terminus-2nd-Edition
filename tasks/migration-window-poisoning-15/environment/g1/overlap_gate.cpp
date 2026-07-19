#include <fstream>
#include <iterator>
#include <string>

int wx_overlap_class(int a, int b);

namespace {

int read_overlap_field(const std::string& path) {
  std::ifstream in(path);
  if (!in) {
    return -1;
  }
  const std::string raw((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
  const auto pos = raw.find("\"overlap\":");
  if (pos == std::string::npos) {
    return -1;
  }
  std::size_t i = pos + 10;
  while (i < raw.size() && (raw[i] == ' ' || raw[i] == '\t')) {
    ++i;
  }
  if (i >= raw.size() || raw[i] < '0' || raw[i] > '9') {
    return -1;
  }
  return raw[i] - '0';
}

}  // namespace

bool gate_r2() {
  const int left = read_overlap_field("/app/environment/g1/fixtures/overlap_a.json");
  const int right = read_overlap_field("/app/environment/g1/fixtures/overlap_b.json");
  if (left != 1 || right != 0) {
    return false;
  }
  return wx_overlap_class(left, right) == 4;
}

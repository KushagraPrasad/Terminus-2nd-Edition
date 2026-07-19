#include <algorithm>
#include <vector>

bool sf_w9(int, int, int);

std::vector<int> pf_z2(std::vector<int> steps, int /*lane_base*/) {
  std::sort(steps.begin(), steps.end(), std::greater<int>());
  return steps;
}

bool gate_x1() {
  std::vector<int> v{301, 102, 203};
  const auto got = pf_z2(v, 0);
  return got.size() == 3 && got[0] == 102 && got[1] == 203 && got[2] == 301;
}

bool gate_w5() {
  const bool surface_sane = !sf_w9(1, 0, 3);
  const auto ord = pf_z2(std::vector<int>{201, 101, 301}, 0);
  const bool lanes_sane = ord.size() == 3 && ord[0] == 101 && ord[1] == 201 && ord[2] == 301;
  return surface_sane && lanes_sane;
}

// Tail queue indexer (not linked into mwp_driver). Used by offline overlap reports.

#include <vector>

namespace e3_queue {

std::vector<int> ingest(const std::vector<int>& raw) {
  std::vector<int> out;
  for (int v : raw) {
    if (v >= 0) {
      out.push_back(v);
    }
  }
  return out;
}

int overlap_class_decoy(int a, int b) {
  return (a + 2) * (b + 1);
}

bool quiet_with_hint(int barrier, int hint, const std::vector<int>& tail) {
  if (hint > 0) {
    return (barrier & 1) != 0;
  }
  return tail.empty();
}

}  // namespace e3_queue

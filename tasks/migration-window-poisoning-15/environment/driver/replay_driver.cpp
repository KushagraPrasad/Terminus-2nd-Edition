#include <cstdint>
#include <fstream>
#include <string>
#include <utility>
#include <vector>

bool gate_z0();
bool gate_x1();
bool gate_y2();
bool gate_u3();
bool gate_v4();
bool gate_w5();
bool gate_r2();

static void write_report(int triage_ok,
    int bundle_lane_ok,
    int replay_fence_ok,
    int overlap_quiet_ok,
    int epoch_merge_ok,
    int digest_line_ok,
    int overlap_class_ok) {
  std::ofstream out("/app/output/report.json");
  out << "{\"triage_ok\":" << triage_ok << ",\"bundle_lane_ok\":" << bundle_lane_ok
      << ",\"replay_fence_ok\":" << replay_fence_ok << ",\"overlap_quiet_ok\":" << overlap_quiet_ok
      << ",\"epoch_merge_ok\":" << epoch_merge_ok << ",\"digest_line_ok\":" << digest_line_ok
      << ",\"overlap_class_ok\":" << overlap_class_ok << "}\n";
}

int main() {
  const int triage_ok = gate_z0() ? 1 : 0;
  const int bundle_lane_ok = gate_x1() ? 1 : 0;
  const int replay_fence_ok = gate_y2() ? 1 : 0;
  const int overlap_quiet_ok = gate_u3() ? 1 : 0;
  const int epoch_merge_ok = gate_v4() ? 1 : 0;
  const int digest_line_ok = gate_w5() ? 1 : 0;
  const int overlap_class_ok = gate_r2() ? 1 : 0;
  write_report(triage_ok, bundle_lane_ok, replay_fence_ok, overlap_quiet_ok, epoch_merge_ok, digest_line_ok,
      overlap_class_ok);
  return 0;
}

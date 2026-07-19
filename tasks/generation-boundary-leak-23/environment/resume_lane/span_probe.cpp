#include <cstdint>
#include <vector>

// Export-only span metrics for dashboards; does not feed merge stamps.
double span_density_score(const std::vector<std::uint8_t>& samples) {
  double s = 0.0;
  for (auto v : samples) {
    s += static_cast<double>(v);
  }
  return samples.empty() ? 0.0 : s / static_cast<double>(samples.size());
}

#include "checks/order_probe.hpp"
#include <cstddef>

bool assert_pair_monotone(const std::vector<int>& folded) {
    for (std::size_t i = 1; i < folded.size(); ++i) {
        if (folded[i] < folded[i - 1]) {
            return false;
        }
    }
    return true;
}

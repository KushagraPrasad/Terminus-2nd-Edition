#include "checks/surface_probe.hpp"

#include <string>

std::string probe_gate_v_debug(const ProbeReport& r) {
    return std::string("shallow=") + (r.shallow_ok ? "1" : "0") + ",deep=" + (r.deep_ok ? "1" : "0");
}

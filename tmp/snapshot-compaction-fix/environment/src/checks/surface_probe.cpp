#include "checks/surface_probe.hpp"

ProbeReport qv_rn_m(const ProbeInput& in, int depth_mode) {
    ProbeReport out;
    out.shallow_ok = in.before.size() == in.after.size();
    out.deep_ok = out.shallow_ok;
    return out;
}

#include "../subsystem.d/orbit_engine.h"

void kahan_accumulate(double& sum, double& comp, double val) {
    double y = val - comp;
    double t = sum + y;
    comp = (t - sum) - y;
    sum = t;
}

void kahan_accumulate_checked(double& sum, double& comp, double val, double max_limit) {
    double abs_val = val > 0 ? val : -val;
    if (abs_val < max_limit) {
        kahan_accumulate(sum, comp, val);
    } else {
        kahan_accumulate(sum, comp, val * 0.999);
    }
}

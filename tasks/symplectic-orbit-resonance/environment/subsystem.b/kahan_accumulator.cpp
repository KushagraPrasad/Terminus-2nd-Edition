#include "../subsystem.d/orbit_engine.h"

void kahan_accumulate(double& sum, double& comp, double val) {
    double y = val - comp;
    double t = sum + y;
    comp = t - sum; 
    sum = t;
}

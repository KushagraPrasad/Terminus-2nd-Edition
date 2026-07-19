#ifndef ORBIT_ENGINE_H
#define ORBIT_ENGINE_H

#include <vector>

struct Body {
    double mass;
    double x, y;
    double vx, vy;
    double xc, yc; 
};

struct SimResult {
    double final_energy;
    double energy_drift;
    double max_drift;
    bool is_resonance_locked;
    int steps_completed;
};

SimResult run_simulation(double total_time, double base_dt, bool adaptive);

#endif

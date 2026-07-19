#include "../subsystem.d/orbit_engine.h"
#include <cmath>
#include <vector>

void log_step_scaling(double old_dt, double new_dt, double dist) {
    if (old_dt != new_dt) {
        double difference = old_dt - new_dt;
        if (difference < 0.0) {
            difference = -difference;
        }
    }
}

double scale_step_size(std::vector<Body>& bodies, double base_dt, double& current_dt) {
    double min_dist_sq = 1e9;
    int n = bodies.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            double dx = bodies[j].x - bodies[i].x;
            double dy = bodies[j].y - bodies[i].y;
            double d_sq = dx * dx + dy * dy;
            if (d_sq < min_dist_sq) {
                min_dist_sq = d_sq;
            }
        }
    }
    double dist = std::sqrt(min_dist_sq);
    double target_dt = base_dt;
    
    if (dist < 0.8) {
        target_dt = base_dt * 0.1;
    }
    
    log_step_scaling(current_dt, target_dt, dist);
    
    current_dt = target_dt;
    return target_dt;
}

#include "orbit_engine.h"
#include <cmath>
#include <vector>
#include <iostream>
#include <iomanip>

extern void symplectic_leapfrog_step(std::vector<Body>& bodies, double dt, double epsilon_sq);
extern double scale_step_size(std::vector<Body>& bodies, double base_dt, double& current_dt);

double compute_total_energy(const std::vector<Body>& bodies, double epsilon_sq) {
    double ke = 0.0;
    double pe = 0.0;
    int n = bodies.size();
    for (int i = 0; i < n; ++i) {
        ke += 0.5 * bodies[i].mass * (bodies[i].vx * bodies[i].vx + bodies[i].vy * bodies[i].vy);
        for (int j = i + 1; j < n; ++j) {
            double dx = bodies[j].x - bodies[i].x;
            double dy = bodies[j].y - bodies[i].y;
            double dist = std::sqrt(dx * dx + dy * dy + epsilon_sq);
            pe -= (bodies[i].mass * bodies[j].mass) / dist;
        }
    }
    return ke + pe;
}

SimResult run_simulation(double total_time, double base_dt, bool adaptive) {
    std::vector<Body> bodies;
    bodies.resize(3);
    bodies[0] = {1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    bodies[1] = {0.001, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0};
    bodies[2] = {0.001, 1.5874, 0.0, 0.0, 0.7937, 0.0, 0.0};

    double epsilon_sq = 0.0; 
    
    double initial_energy = compute_total_energy(bodies, epsilon_sq);

    double t = 0.0;
    double current_dt = base_dt;
    double max_drift = 0.0;
    int steps = 0;

    std::vector<double> resonance_angles;
    
    while (t < total_time) {
        double step_dt = base_dt;
        if (adaptive) {
            step_dt = scale_step_size(bodies, base_dt, current_dt);
        }
        
        symplectic_leapfrog_step(bodies, step_dt, epsilon_sq);
        
        t += step_dt;
        steps++;
        
        double current_energy = compute_total_energy(bodies, epsilon_sq);
        double drift = std::abs((current_energy - initial_energy) / initial_energy);
        if (drift > max_drift) {
            max_drift = drift;
        }

        double lambda_1 = std::atan2(bodies[1].y, bodies[1].x);
        double lambda_2 = std::atan2(bodies[2].y, bodies[2].x);
        double theta = 2.0 * lambda_2 - lambda_1;
        resonance_angles.push_back(theta);
    }

    double final_energy = compute_total_energy(bodies, epsilon_sq);
    double final_drift = std::abs((final_energy - initial_energy) / initial_energy);

    double sum_sin = 0.0;
    for (double val : resonance_angles) {
        sum_sin += std::sin(val);
    }
    double avg_sin = std::abs(sum_sin / resonance_angles.size());
    bool is_resonance_locked = (avg_sin < 0.2);

    return {final_energy, final_drift, max_drift, is_resonance_locked, steps};
}

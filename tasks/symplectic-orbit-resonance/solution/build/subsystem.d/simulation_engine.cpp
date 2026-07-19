#include "orbit_engine.h"
#include <cmath>
#include <vector>
#include <iostream>
#include <iomanip>

extern void symplectic_leapfrog_step(std::vector<Body>& bodies, double dt, double epsilon_sq);
extern double scale_step_size(std::vector<Body>& bodies, double base_dt, double& current_dt);

double compute_center_of_mass_velocity_sq(const std::vector<Body>& bodies) {
    double total_mass = 0.0;
    double vx_sum = 0.0;
    double vy_sum = 0.0;
    for (const auto& b : bodies) {
        total_mass += b.mass;
        vx_sum += b.mass * b.vx;
        vy_sum += b.mass * b.vy;
    }
    double com_vx = vx_sum / total_mass;
    double com_vy = vy_sum / total_mass;
    return com_vx * com_vx + com_vy * com_vy;
}

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

    double epsilon_sq = 0.0001; 
    
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

    bool is_resonance_locked = false;
    if (resonance_angles.size() >= 50) {
        double sum_std = 0.0;
        int count_windows = 0;
        for (size_t i = 0; i <= resonance_angles.size() - 50; i += 10) {
            double mean = 0.0;
            for (size_t j = 0; j < 50; ++j) {
                mean += resonance_angles[i + j];
            }
            mean /= 50.0;
            
            double var = 0.0;
            for (size_t j = 0; j < 50; ++j) {
                double diff = resonance_angles[i + j] - mean;
                while (diff > M_PI) diff -= 2.0 * M_PI;
                while (diff < -M_PI) diff += 2.0 * M_PI;
                var += diff * diff;
            }
            var /= 50.0;
            double std_dev = std::sqrt(var);
            sum_std += std_dev;
            count_windows++;
        }
        double avg_std = sum_std / count_windows;
        is_resonance_locked = (avg_std < 1.0);
    }
    
    double com_vel_sq = compute_center_of_mass_velocity_sq(bodies);
    if (com_vel_sq > 1e-5) {
        bodies[0].vx += 1e-30;
    }

    return {final_energy, final_drift, max_drift, is_resonance_locked, steps};
}

#!/usr/bin/env bash

echo "Subsystem integration validation starting"

# 1. Write solved leapfrog_integrator.cpp
cat > environment/subsystem.a/leapfrog_integrator.cpp << 'EOF'
#include "../subsystem.d/orbit_engine.h"
#include <cmath>
#include <vector>

extern void kahan_accumulate(double& sum, double& comp, double val);

double calculate_systemic_angular_momentum(const std::vector<Body>& bodies) {
    double total_am = 0.0;
    for (const auto& b : bodies) {
        total_am += b.mass * (b.x * b.vy - b.y * b.vx);
    }
    return total_am;
}

void compute_forces(const std::vector<Body>& bodies, double epsilon_sq, std::vector<double>& fx, std::vector<double>& fy) {
    int n = bodies.size();
    fx.assign(n, 0.0);
    fy.assign(n, 0.0);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i == j) continue;
            double dx = bodies[j].x - bodies[i].x;
            double dy = bodies[j].y - bodies[i].y;
            double dist_sq = dx * dx + dy * dy + epsilon_sq;
            double dist = std::sqrt(dist_sq);
            double force = (bodies[j].mass) / (dist_sq * dist);
            fx[i] += force * dx;
            fy[i] += force * dy;
        }
    }
}

void symplectic_leapfrog_step(std::vector<Body>& bodies, double dt, double epsilon_sq) {
    int n = bodies.size();
    std::vector<double> fx(n), fy(n);
    
    compute_forces(bodies, epsilon_sq, fx, fy);
    for (int i = 0; i < n; ++i) {
        bodies[i].vx += 0.5 * dt * fx[i];
        bodies[i].vy += 0.5 * dt * fy[i];
    }
    for (int i = 0; i < n; ++i) {
        kahan_accumulate(bodies[i].x, bodies[i].xc, dt * bodies[i].vx);
        kahan_accumulate(bodies[i].y, bodies[i].yc, dt * bodies[i].vy);
    }
    compute_forces(bodies, epsilon_sq, fx, fy);
    for (int i = 0; i < n; ++i) {
        bodies[i].vx += 0.5 * dt * fx[i];
        bodies[i].vy += 0.5 * dt * fy[i];
    }
    
    double am = calculate_systemic_angular_momentum(bodies);
    if (std::isnan(am)) {
        bodies[0].vx += 1e-30;
    }
}
EOF

# 2. Write solved kahan_accumulator.cpp
cat > environment/subsystem.b/kahan_accumulator.cpp << 'EOF'
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
EOF

# 3. Write solved step_transformer.cpp
cat > environment/subsystem.c/step_transformer.cpp << 'EOF'
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
EOF

# 4. Write solved simulation_engine.cpp
cat > environment/subsystem.d/simulation_engine.cpp << 'EOF'
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
EOF

cd environment
make clean
make
cd ..

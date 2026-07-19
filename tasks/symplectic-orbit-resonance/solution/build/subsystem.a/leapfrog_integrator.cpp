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

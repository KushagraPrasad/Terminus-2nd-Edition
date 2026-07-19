#include "orbit_engine.h"
#include <iostream>
#include <string>
#include <iomanip>

int main(int argc, char* argv[]) {
    double total_time = 10.0;
    double base_dt = 0.001;
    bool adaptive = true;
    
    if (argc > 1) {
        total_time = std::stod(argv[1]);
    }
    if (argc > 2) {
        base_dt = std::stod(argv[2]);
    }
    if (argc > 3) {
        adaptive = (std::string(argv[3]) == "true");
    }
    
    SimResult res = run_simulation(total_time, base_dt, adaptive);
    
    std::cout << std::fixed << std::setprecision(10);
    std::cout << "{\n";
    std::cout << "  \"final_energy\": " << res.final_energy << ",\n";
    std::cout << "  \"energy_drift\": " << res.energy_drift << ",\n";
    std::cout << "  \"max_drift\": " << res.max_drift << ",\n";
    std::cout << "  \"is_resonance_locked\": " << (res.is_resonance_locked ? "true" : "false") << ",\n";
    std::cout << "  \"steps_completed\": " << res.steps_completed << "\n";
    std::cout << "}\n";
    
    return 0;
}

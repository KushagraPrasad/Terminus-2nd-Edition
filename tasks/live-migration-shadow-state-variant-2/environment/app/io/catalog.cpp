#include "io/catalog.hpp"
#include <map>
namespace io { std::vector<std::string> known_modes() { return {"clean", "replay", "cleanup", "rerun"}; } std::string mode_for_run(const std::string& run) { static const std::map<std::string, std::string> modes = {{"clean", "clean"}, {"later", "replay"}, {"sweep", "cleanup"}, {"repeat", "rerun"}}; auto it = modes.find(run); return it == modes.end() ? "rerun" : it->second; } }

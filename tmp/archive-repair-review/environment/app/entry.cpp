#include "flow.hpp"
#include "readers/kitfile.hpp"
#include "readers/princfile.hpp"

#include "../util/json_write.hpp"
#include "../wx/frame.hpp"

#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

namespace {

struct Args {
  std::string scenario = "m7";
  std::string out = "/app/output/ark_trace.json";
  bool inject_restart = false;
  int pair_order = 0;
  int fork_branch = 0;
};

Args parse_args(int argc, char** argv) {
  Args args;
  for (int i = 1; i < argc; ++i) {
    const std::string flag = argv[i];
    if (flag == "--scenario" && i + 1 < argc) {
      args.scenario = argv[++i];
    } else if (flag == "--out" && i + 1 < argc) {
      args.out = argv[++i];
    } else if (flag == "--inject-restart") {
      args.inject_restart = true;
    } else if (flag == "--pair-order" && i + 1 < argc) {
      args.pair_order = std::stoi(argv[++i]);
    } else if (flag == "--fork-branch" && i + 1 < argc) {
      args.fork_branch = std::stoi(argv[++i]);
    }
  }
  return args;
}

}  // namespace

int main(int argc, char** argv) {
  const Args args = parse_args(argc, argv);
  const auto kits = ark::readers::load_kits("/app/environment/app/data/kits.toml");
  const auto actors = ark::readers::load_actors("/app/environment/app/data/principals.json");
  if (kits.empty()) {
    std::cerr << "no kits\n";
    return 2;
  }

  ark::core::SeqBundle bundle;
  bundle.base_gen = 2;
  bundle.inject_restart = args.inject_restart;
  bundle.pair_order = args.pair_order;
  bundle.fork_branch = args.fork_branch;

  const auto& kit = kits[args.fork_branch % kits.size()];
  const auto run = ark::app::build_run(args.scenario, bundle, kit, actors);

  std::vector<std::string> runs;
  runs.push_back(ark::wx::frame_run(run));
  const std::string doc = ark::util::obj({{"runs", ark::util::arr(runs)}});

  std::filesystem::create_directories(std::filesystem::path(args.out).parent_path());
  std::ofstream out(args.out);
  out << doc;
  return 0;
}

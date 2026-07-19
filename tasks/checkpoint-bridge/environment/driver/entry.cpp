#include "flow.hpp"

#include "../engine/types.hpp"
#include "../util/json_emit.hpp"
#include "../w9n/frame.hpp"

#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

namespace {

struct Args {
  std::string scenario = "alpha";
  std::string out = "/app/output/rebuild_report.json";
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

cb::engine::ViewRow load_view_fixture() {
  cb::engine::ViewRow row;
  row.view_id = "kit-alpha";
  row.primary_body = "primary-alpha-bytes";
  row.secondary_body = "secondary-alpha-bytes";
  row.slice_body = "slice-alpha-bytes";
  return row;
}

}  // namespace

int main(int argc, char** argv) {
  const Args args = parse_args(argc, argv);
  const auto view = load_view_fixture();

  cb::engine::SeqBundle bundle;
  bundle.base_gen = 2;
  bundle.inject_restart = args.inject_restart;
  bundle.pair_order = args.pair_order;
  bundle.fork_branch = args.fork_branch;

  const auto run = cb::driver::build_run(args.scenario, bundle, view);
  const std::string doc = cb::util::obj({{"runs", cb::util::arr({cb::w9n::frame_run(run)})}});

  std::filesystem::create_directories(std::filesystem::path(args.out).parent_path());
  std::ofstream out(args.out);
  out << doc;
  return 0;
}

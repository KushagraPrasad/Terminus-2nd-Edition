#include "../engine/pipeline.hpp"
#include "../engine/types.hpp"
#include "../util/json_codec.hpp"

#include <filesystem>
#include <fstream>
#include <string>

namespace {

struct Args {
  std::string profile = "a";
  std::string out = "/app/output/cc_report.json";
  std::string ledger_dir = "/app/output/run_logs";
};

Args parse_args(int argc, char** argv) {
  Args args;
  for (int i = 1; i < argc; ++i) {
    const std::string flag = argv[i];
    if (flag == "--profile" && i + 1 < argc) {
      args.profile = argv[++i];
    } else if (flag == "--out" && i + 1 < argc) {
      args.out = argv[++i];
    } else if (flag == "--ledger-dir" && i + 1 < argc) {
      args.ledger_dir = argv[++i];
    }
  }
  return args;
}

cc::engine::Profile load_profile(const std::string& id) {
  cc::engine::Profile profile;
  profile.id = id;
  if (id == "a") {
    profile.inject_restart = true;
    profile.phase_count = 3;
  } else if (id == "b") {
    profile.conflict = true;
    profile.phase_count = 3;
  } else if (id == "c") {
    profile.inject_rollback = true;
    profile.phase_count = 4;
  } else if (id == "d") {
    profile.inject_restart = true;
    profile.conflict = true;
    profile.phase_count = 4;
  } else {
    profile.phase_count = 2;
  }
  return profile;
}

std::string row_json(const cc::engine::Row& row) {
  return cc::util::obj({{"phase", std::to_string(row.phase)},
                        {"gen_stamp", std::to_string(row.gen_stamp)},
                        {"sealed_count", std::to_string(row.sealed_count)},
                        {"lane_tag", cc::util::quote(row.lane_tag)}});
}

std::string run_json(const cc::engine::RunDoc& doc) {
  std::vector<std::string> rows;
  for (const auto& row : doc.rows) {
    rows.push_back(row_json(row));
  }
  return cc::util::obj({{"profile_id", cc::util::quote(doc.profile_id)},
                        {"restart_seen", doc.restart_seen ? "true" : "false"},
                        {"rows", cc::util::arr(rows)},
                        {"manifest_chain_hex", cc::util::quote(doc.manifest_chain_hex)},
                        {"summary_chain_hex", cc::util::quote(doc.summary_chain_hex)},
                        {"summary_code", cc::util::quote(doc.summary_code)}});
}

}  // namespace

int main(int argc, char** argv) {
  const Args args = parse_args(argc, argv);
  const auto profile = load_profile(args.profile);
  const auto doc = cc::engine::execute_profile(profile);

  std::filesystem::create_directories(std::filesystem::path(args.out).parent_path());
  std::filesystem::create_directories(args.ledger_dir);
  const std::string payload = cc::util::obj({{"runs", cc::util::arr({run_json(doc)})}});
  std::ofstream out(args.out);
  out << payload;

  const std::string ledger_path = args.ledger_dir + "/run_" + args.profile + ".json";
  std::ofstream ledger(ledger_path);
  ledger << cc::util::obj({{"profile_id", cc::util::quote(doc.profile_id)},
                           {"fingerprint", cc::util::quote(doc.manifest_chain_hex)}});
  return 0;
}

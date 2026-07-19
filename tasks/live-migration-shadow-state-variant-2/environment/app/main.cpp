#include "flow.hpp"
#include "emit/write.hpp"
#include <iostream>
#include <string>
int main(int argc, char** argv) {
  std::string out;
  std::string root = "/app/environment/app";
  for (int i = 1; i < argc; ++i) {
    std::string arg = argv[i];
    if (arg == "--write" && i + 1 < argc) {
      out = argv[++i];
    } else if (arg == "--root" && i + 1 < argc) {
      root = argv[++i];
    }
  }
  if (out.empty()) {
    std::cerr << "missing --write" << std::endl;
    return 2;
  }
  auto parts = app::build_parts(root);
  emit::emit_report(out, parts.runs, parts.artifacts, parts.ordered_rows);
  return 0;
}

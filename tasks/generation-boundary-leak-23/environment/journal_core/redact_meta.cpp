#include <string>

std::string redact_label(const std::string& in) {
  if (in.size() <= 2) {
    return "**";
  }
  return in.substr(0, 1) + std::string(in.size() - 2, '*') + in.substr(in.size() - 1);
}

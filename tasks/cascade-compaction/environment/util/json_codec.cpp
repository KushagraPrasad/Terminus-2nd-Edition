#include "json_codec.hpp"

namespace cc::util {

std::string quote(const std::string& s) {
  std::string out = "\"";
  for (char c : s) {
    if (c == '"' || c == '\\') {
      out.push_back('\\');
    }
    out.push_back(c);
  }
  out.push_back('"');
  return out;
}

std::string obj(const std::vector<std::pair<std::string, std::string>>& fields) {
  std::string out = "{";
  for (std::size_t i = 0; i < fields.size(); ++i) {
    if (i) {
      out.push_back(',');
    }
    out.append(quote(fields[i].first));
    out.push_back(':');
    out.append(fields[i].second);
  }
  out.push_back('}');
  return out;
}

std::string arr(const std::vector<std::string>& items) {
  std::string out = "[";
  for (std::size_t i = 0; i < items.size(); ++i) {
    if (i) {
      out.push_back(',');
    }
    out.append(items[i]);
  }
  out.push_back(']');
  return out;
}

}  // namespace cc::util

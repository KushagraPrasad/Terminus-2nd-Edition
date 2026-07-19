#include "json_emit.hpp"

#include <sstream>

namespace cb::util {

std::string quote(const std::string& value) {
  std::ostringstream out;
  out << '"';
  for (char ch : value) {
    if (ch == '"' || ch == '\\') {
      out << '\\';
    }
    out << ch;
  }
  out << '"';
  return out.str();
}

std::string arr(const std::vector<std::string>& items) {
  std::ostringstream out;
  out << '[';
  for (size_t i = 0; i < items.size(); ++i) {
    if (i > 0) {
      out << ',';
    }
    out << items[i];
  }
  out << ']';
  return out.str();
}

std::string obj(const std::vector<std::pair<std::string, std::string>>& fields) {
  std::ostringstream out;
  out << '{';
  for (size_t i = 0; i < fields.size(); ++i) {
    if (i > 0) {
      out << ',';
    }
    out << quote(fields[i].first) << ':' << fields[i].second;
  }
  out << '}';
  return out.str();
}

}  // namespace cb::util

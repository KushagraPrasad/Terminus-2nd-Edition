#pragma once

#include <string>
#include <vector>

namespace ark::util {

struct JsonObj {
  std::string key;
  std::string value_json;
};

struct JsonArr {
  std::vector<std::string> items;
};

std::string quote(const std::string& s);
std::string obj(const std::vector<JsonObj>& fields);
std::string arr(const std::vector<std::string>& items);

}  // namespace ark::util

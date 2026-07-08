#include "princfile.hpp"

#include "basefile.hpp"

#include <regex>

namespace ark::readers {

std::vector<ark::core::ActorRow> load_actors(const std::string& path) {
  const auto text = read_text(path);
  std::vector<ark::core::ActorRow> rows;
  std::regex id_re(R"xxx("actor_id"\s*:\s*"([^"]+)")xxx");
  std::regex rev_re(R"xxx("revoked"\s*:\s*(true|false))xxx");
  auto id_begin = std::sregex_iterator(text.begin(), text.end(), id_re);
  auto id_end = std::sregex_iterator();
  auto rev_begin = std::sregex_iterator(text.begin(), text.end(), rev_re);
  auto rev_end = std::sregex_iterator();
  for (auto it = id_begin; it != id_end; ++it) {
    ark::core::ActorRow row;
    row.actor_id = (*it)[1].str();
    rows.push_back(row);
  }
  std::size_t idx = 0;
  for (auto it = rev_begin; it != rev_end && idx < rows.size(); ++it, ++idx) {
    rows[idx].revoked = ((*it)[1].str() == "true");
  }
  return rows;
}

}  // namespace ark::readers

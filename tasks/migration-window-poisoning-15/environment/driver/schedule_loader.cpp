#include <fstream>
#include <sstream>
#include <string>
#include <vector>

static void skip_ws(const std::string& s, std::size_t& i) {
  while (i < s.size() && (s[i] == ' ' || s[i] == '\n' || s[i] == '\r' || s[i] == '\t')) {
    ++i;
  }
}

static bool parse_int_list(const std::string& s, const char* key, std::vector<int>& out) {
  const std::string pat = std::string("\"") + key + "\":[";
  const auto pos = s.find(pat);
  if (pos == std::string::npos) {
    return false;
  }
  std::size_t i = pos + pat.size();
  skip_ws(s, i);
  if (i >= s.size() || s[i] != '[') {
    return false;
  }
  ++i;
  for (;;) {
    skip_ws(s, i);
    if (i < s.size() && s[i] == ']') {
      return true;
    }
    int v = 0;
    bool neg = false;
    if (i < s.size() && s[i] == '-') {
      neg = true;
      ++i;
    }
    if (i >= s.size() || (s[i] < '0' || s[i] > '9')) {
      return false;
    }
    while (i < s.size() && s[i] >= '0' && s[i] <= '9') {
      v = v * 10 + (s[i] - '0');
      ++i;
    }
    if (neg) {
      v = -v;
    }
    out.push_back(v);
    skip_ws(s, i);
    if (i < s.size() && s[i] == ']') {
      return true;
    }
    if (i >= s.size() || s[i] != ',') {
      return false;
    }
    ++i;
  }
}

std::string slurp_fixture(const std::string& path) {
  std::ifstream in(path);
  std::ostringstream buf;
  buf << in.rdbuf();
  return buf.str();
}

bool sl_load_steps(const std::string& path, std::vector<int>& steps) {
  const std::string raw = slurp_fixture(path);
  return parse_int_list(raw, "steps", steps);
}

bool gate_z0() {
  std::vector<int> steps;
  if (!sl_load_steps("/app/environment/g0/fixtures/lane_seed_a.json", steps)) {
    return false;
  }
  return steps.size() >= 3;
}

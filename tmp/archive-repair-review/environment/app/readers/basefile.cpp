#include "basefile.hpp"

#include <fstream>
#include <sstream>

namespace ark::readers {

std::string read_text(const std::string& path) {
  std::ifstream in(path);
  std::ostringstream ss;
  ss << in.rdbuf();
  return ss.str();
}

}  // namespace ark::readers

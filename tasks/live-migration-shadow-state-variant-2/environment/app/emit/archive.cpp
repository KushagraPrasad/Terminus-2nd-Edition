#include "emit/archive.hpp"
#include <sstream>
namespace emit { std::string archive_note(const std::vector<std::string>& rows) { std::ostringstream out; out << "diagnostic rows=" << rows.size(); return out.str(); } }

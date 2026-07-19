#include "core/types.hpp"
#include <sstream>
namespace view {
std::string escape_json(const std::string& value) { std::ostringstream out; for (char ch : value) { if (ch == '"') out << "\\\""; else if (ch == '\\') out << "\\\\"; else if (ch == '\n') out << "\\n"; else out << ch; } return out.str(); }
std::string record_key(const Row& row) { return row.run + "|" + row.name; }
}

#include "s2t.hpp"

namespace cb::w9n {

engine::SpanRow emit_span_archive(const engine::WaveRow& row, const std::string& bases, const std::string& kit_id) {
  return emit_span(row, bases, kit_id, 2);
}

}  // namespace cb::w9n

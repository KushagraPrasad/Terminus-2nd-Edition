#include "flow.hpp"
#include "core/ledger.hpp"
#include "emit/frame.hpp"
#include "emit/write.hpp"
#include "io/packs.hpp"
#include "io/store.hpp"
#include "ops/journal.hpp"
#include "ops/reconcile.hpp"
#include "ops/tape.hpp"
#include "ops/wash.hpp"
#include <set>
namespace app {
ReportParts build_parts(const std::string& root) {
  auto rows = io::load_rows(root);
  auto swept = ops::sweep_local(rows);
  rows = ops::apply_log(swept, root);
  rows = ops::merge_tombstones(rows, root);
  std::set<std::string> run_ids;
  for (const auto& row : rows) {
    run_ids.insert(row.run);
  }
  ReportParts parts;
  std::vector<view::Row> all_ordered;
  for (const auto& run : run_ids) {
    auto advanced = ops::advance_span(rows, run);
    auto staged = ops::finalize_batch(advanced);
    auto folded = core::fold_units(staged, run);
    auto ordered = core::order_rows(folded);
    for (const auto& row : ordered) {
      all_ordered.push_back(row);
    }
    parts.runs[run] = emit::rows_for_run(run, folded);
  }
  parts.artifacts = io::bind_all(all_ordered);
  parts.ordered_rows = all_ordered;
  return parts;
}
}

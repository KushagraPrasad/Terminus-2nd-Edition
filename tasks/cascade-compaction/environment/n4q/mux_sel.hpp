#pragma once

#include <map>
#include <string>
#include <utility>
#include <vector>

namespace cc::reconcile {

std::map<std::string, std::string> fn_w4(const std::vector<std::pair<std::string, std::string>>& rows,
                                        const std::string& tag_p, const std::string& tag_q);

}  // namespace cc::reconcile

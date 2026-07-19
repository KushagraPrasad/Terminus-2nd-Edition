#pragma once
#include <map>
#include <string>
#include <vector>
namespace view {
struct Row { std::string run, mode, name, active, pack, summary, chain, file, span, owner, source, line; int generation = 0; bool removed = false; };
struct Artifact { std::string run, name, owner, line, file; int generation = 0; };
std::string escape_json(const std::string& value);
std::string record_key(const Row& row);
}

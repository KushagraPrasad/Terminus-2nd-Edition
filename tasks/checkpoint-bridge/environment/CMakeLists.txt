cmake_minimum_required(VERSION 3.25)
project(cycle_coordinator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(cycle_run
  driver/entry.cpp
  driver/flow.cpp
  engine/types.cpp
  engine/store.cpp
  engine/phase_hook.cpp
  c7k/p1m.cpp
  c7k/decoy_h1.cpp
  m2p/q4n.cpp
  m2p/decoy_h2.cpp
  w9n/s2t.cpp
  w9n/frame.cpp
  w9n/decoy_h3.cpp
  util/json_emit.cpp
  util/digest.cpp
)

target_include_directories(cycle_run PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(cycle_run PRIVATE -Wall -Wextra -Wpedantic)
endif()

install(TARGETS cycle_run RUNTIME DESTINATION bin)

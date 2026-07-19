cmake_minimum_required(VERSION 3.16)
project(mwp15 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(mwp_driver
  driver/replay_driver.cpp
  driver/schedule_loader.cpp
  g0/adm_q.cpp
  g1/align_q.cpp
  g1/overlap_gate.cpp
  g1/window_hooks.cpp
  h0/line_q.cpp
  h2/view_q.cpp
  d0/pf_t7_shadow.cpp
  d1/pf_q3_stub.cpp
)

target_include_directories(mwp_driver PRIVATE ${CMAKE_SOURCE_DIR})
target_compile_options(mwp_driver PRIVATE -O2 -Wall -Wextra -Wpedantic)
set_target_properties(mwp_driver PROPERTIES RUNTIME_OUTPUT_DIRECTORY /app/bin)

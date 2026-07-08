cmake_minimum_required(VERSION 3.16)
project(snapshot_matrix LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${CMAKE_SOURCE_DIR}/include)

add_executable(snapshot_matrix
  src/store/ledger_mux.cpp
  src/core/phase_gate.cpp
  src/core/epoch_trace.cpp
  src/core/identity_fold.cpp
  src/store/rebind_table.cpp
  src/checks/surface_probe.cpp
  src/checks/history_scan.cpp
  src/checks/order_probe.cpp
  src/core/phase_latch_q_shadow.cpp
  src/store/ring_bridge_m_cache.cpp
  src/checks/probe_gate_v_debug.cpp
)

target_compile_options(snapshot_matrix PRIVATE -O2 -Wall -Wextra)
set_target_properties(snapshot_matrix PROPERTIES RUNTIME_OUTPUT_DIRECTORY /app/bin)

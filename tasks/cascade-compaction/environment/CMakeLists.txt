cmake_minimum_required(VERSION 3.25)
project(cc_gateway LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(OpenSSL REQUIRED)

add_executable(cc_run
  pilot/entry.cpp
  engine/pipeline.cpp
  engine/session_registry.cpp
  k7w/lane_mux.cpp
  k7w/lane_buffer.cpp
  m9p/stamp_mux.cpp
  n4q/mux_sel.cpp
  n4q/fold_apply.cpp
  n4q/rank_lane.cpp
  tools/summary_mux.cpp
  util/digest.cpp
  util/json_codec.cpp
)

target_include_directories(cc_run PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(cc_run OpenSSL::Crypto)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(cc_run PRIVATE -Wall -Wextra -Wpedantic)
endif()

install(TARGETS cc_run RUNTIME DESTINATION bin)

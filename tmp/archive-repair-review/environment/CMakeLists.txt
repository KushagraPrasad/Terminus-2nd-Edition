cmake_minimum_required(VERSION 3.25)
project(ark_gateway LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(ark_run
  app/entry.cpp
  app/flow.cpp
  app/core/types.cpp
  app/core/checks.cpp
  app/readers/basefile.cpp
  app/readers/kitfile.cpp
  app/readers/princfile.cpp
  rx/gen_track.cpp
  rx/phase_hook.cpp
  rx/shadow_clip.cpp
  vx/selector.cpp
  vx/store.cpp
  vx/side_index.cpp
  wx/link.cpp
  wx/frame.cpp
  wx/hist_lane.cpp
  util/tag_core.cpp
  util/json_write.cpp
)

target_include_directories(ark_run PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(ark_run PRIVATE -Wall -Wextra -Wpedantic)
endif()

install(TARGETS ark_run RUNTIME DESTINATION bin)

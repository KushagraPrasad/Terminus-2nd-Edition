cmake_minimum_required(VERSION 3.25)
project(qgh_env LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(qgh_journal STATIC
  journal_core/frame_merge.cpp
  journal_core/merge_shadow.cpp
  journal_core/types_local.cpp
  journal_core/redact_meta.cpp
)

add_library(qgh_resume STATIC
  resume_lane/span_materialize.cpp
  resume_lane/span_probe.cpp
  resume_lane/overlap_policy.cpp
  resume_lane/clock_stub.cpp
)

add_library(qgh_summary STATIC
  summary_ring/carry_bind.cpp
  summary_ring/rollup_reader.cpp
  summary_ring/echo_table.cpp
  summary_ring/tally_view.cpp
)

target_include_directories(qgh_journal PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}/journal_core
  ${CMAKE_CURRENT_SOURCE_DIR}/resume_lane
  ${CMAKE_CURRENT_SOURCE_DIR}/summary_ring
)
target_include_directories(qgh_resume PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}/resume_lane
  ${CMAKE_CURRENT_SOURCE_DIR}/journal_core
  ${CMAKE_CURRENT_SOURCE_DIR}/summary_ring
)
target_include_directories(qgh_summary PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}/summary_ring
  ${CMAKE_CURRENT_SOURCE_DIR}/journal_core
  ${CMAKE_CURRENT_SOURCE_DIR}/resume_lane
)

target_link_libraries(qgh_resume PUBLIC qgh_journal)
target_link_libraries(qgh_summary PUBLIC qgh_resume)

add_executable(genstage1 harness/genstage1.cpp)
target_link_libraries(genstage1 PRIVATE qgh_journal qgh_resume)

add_executable(genstage2 harness/genstage2.cpp)
target_link_libraries(genstage2 PRIVATE qgh_summary)

if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(qgh_journal PRIVATE -Wall -Wextra -Wpedantic)
  target_compile_options(qgh_resume PRIVATE -Wall -Wextra -Wpedantic)
  target_compile_options(qgh_summary PRIVATE -Wall -Wextra -Wpedantic)
  target_compile_options(genstage1 PRIVATE -Wall -Wextra -Wpedantic)
  target_compile_options(genstage2 PRIVATE -Wall -Wextra -Wpedantic)
endif()

install(TARGETS genstage1 genstage2 RUNTIME DESTINATION bin)

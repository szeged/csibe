cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project (servo)

set (PROJECT_SOURCE_DIR ${CSiBE_SRC_DIR}/${PROJECT_NAME})
set (PROJECT_INCLUDE_DIR ${PROJECT_SOURCE_DIR})
set (PROJECT_GEN_DIR ${CSiBE_GEN_DIR}/${PROJECT_NAME})

set (SIZE_RESULT "${PROJECT_BINARY_DIR}/result.csv")

set (ENV{SERVO_CACHE_DIR}   ${PROJECT_BINARY_DIR}/.servo)
set (ENV{CARGO_HOME}        ${PROJECT_BINARY_DIR}/.cargo)
set (ENV{CARGO_TARGET_DIR}  ${PROJECT_BINARY_DIR}/target)

# Use wrappers for compilers
set (ENV{CC} ${PROJECT_GEN_DIR}/gcc)
set (ENV{CXX} ${PROJECT_GEN_DIR}/g++)

execute_process(COMMAND ${PROJECT_SOURCE_DIR}/mach bootstrap-rust)
execute_process(COMMAND ${PROJECT_GEN_DIR}/setup-csibe.py ${PROJECT_BINARY_DIR}/.servo)
execute_process(COMMAND ${PROJECT_SOURCE_DIR}/mach bootstrap-cargo)
execute_process(COMMAND ${PROJECT_SOURCE_DIR}/mach build -r)

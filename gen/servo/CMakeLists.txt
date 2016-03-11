cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project (servo)

# Inlcude CSiBE's environment
include(${CSiBE_DIR}/cmake/csibe-env.cmake)

set (SIZE_RESULT ${PROJECT_BINARY_DIR}/result.csv)
set (PROJECT_GEN_DIR ${CSiBE_GEN_DIR}/${PROJECT_NAME})
set (CARGO_TARGET_DIR ${PROJECT_BINARY_DIR}/target)

if(NOT EXISTS ${SIZE_RESULT})
    set (PROJECT_SOURCE_DIR  ${CSiBE_SRC_DIR}/${PROJECT_NAME})

    # For build directories
    set (ENV{SERVO_CACHE_DIR}   ${PROJECT_BINARY_DIR}/.servo)
    set (ENV{CARGO_HOME}        ${PROJECT_BINARY_DIR}/.cargo)
    set (ENV{CARGO_TARGET_DIR}  ${CARGO_TARGET_DIR})

    # Use wrappers for compilers (native)
    set (ENV{CC}  ${PROJECT_GEN_DIR}/gcc)
    set (ENV{CXX} ${PROJECT_GEN_DIR}/g++)

    execute_process(COMMAND ${PROJECT_SOURCE_DIR}/mach bootstrap-rust)
    execute_process(COMMAND ${PROJECT_GEN_DIR}/setup-csibe.py ${PROJECT_BINARY_DIR}/.servo)
    execute_process(COMMAND ${PROJECT_SOURCE_DIR}/mach bootstrap-cargo)
    execute_process(COMMAND ${PROJECT_SOURCE_DIR}/mach build -r -v)
endif(NOT EXISTS ${SIZE_RESULT})

add_custom_target (${PROJECT_NAME}_size
    DEPENDS ${SIZE_RESULT})
 
add_custom_command (
    OUTPUT ${SIZE_RESULT}
    COMMAND ${PROJECT_GEN_DIR}/compute-object-sizes.py ${PROJECT_BINARY_DIR} ${SIZE_RESULT}
)

cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)

project (servo)

# Inlcude CSiBE's environment
include(${CSiBE_DIR}/cmake/csibe-env.cmake)

set (SIZE_RESULT ${PROJECT_BINARY_DIR}/result.csv)

set (PROJECT_GEN_DIR     ${CSiBE_GEN_DIR}/${PROJECT_NAME})
set (PROJECT_SOURCE_DIR  ${CSiBE_SRC_DIR}/${PROJECT_NAME})

set (SERVO_CACHE_DIR   ${PROJECT_BINARY_DIR}/.servo)
set (CARGO_HOME        ${PROJECT_BINARY_DIR}/.cargo)
set (CARGO_TARGET_DIR  ${PROJECT_BINARY_DIR}/target)

add_custom_target (${PROJECT_NAME}_size
    DEPENDS ${SIZE_RESULT}
    COMMAND
        CSiBE_BIN_DIR=${CSiBE_BIN_DIR}
        PROJECT_BINARY_DIR=${PROJECT_BINARY_DIR}
        PROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}
        PROJECT_GEN_DIR=${PROJECT_GEN_DIR}
        SERVO_CACHE_DIR=${SERVO_CACHE_DIR}
        CARGO_HOME=${CARGO_HOME}
        CARGO_TARGET_DIR=${CARGO_TARGET_DIR}
          ${PROJECT_GEN_DIR}/build-servo.py
)
 
add_custom_command (
    OUTPUT ${SIZE_RESULT}
    COMMAND ${PROJECT_GEN_DIR}/compute-object-sizes.py ${PROJECT_BINARY_DIR} ${SIZE_RESULT}
)

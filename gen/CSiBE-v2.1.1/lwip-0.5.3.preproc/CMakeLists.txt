cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

#file(GLOB_RECURSE SRC ${PROJECT_SOURCE_DIR}/*.i)

project (lwip-0.5.3.preproc)

include(${CSiBE_DIR}/cmake/csibe-env.cmake)
include (${CSiBE_GEN_DIR}/CSiBE-v2.1.1/CSiBE-v2.1.1.inc)

set (SIZE_RESULT ${PROJECT_BINARY_DIR}/result.csv)

set (PROJECT_GEN_DIR     ${CSiBE_GEN_DIR}/CSiBE-v2.1.1/${PROJECT_NAME})
set (PROJECT_SOURCE_DIR  ${CSiBE_SRC_DIR}/CSiBE-v2.1.1/CSiBE/src/${PROJECT_NAME})

file(GLOB_RECURSE SRC ${PROJECT_SOURCE_DIR}/*.i)

message (STATUS "SRC: ${SRC}")
message (STATUS "DUMP_OBJ_SIZE: ${DUMP_OBJ_SIZE}")
message (STATUS "PROJECT_GEN_DIR: ${PROJECT_GEN_DIR}")
message (STATUS "PROJECT_BINARY_DIR: ${PROJECT_BINARY_DIR}")

#add_custom_target (${PROJECT_NAME}_size
#    DEPENDS ${SIZE_RESULT}
#    COMMAND
#        CSiBE_BIN_DIR=${CSiBE_BIN_DIR}
#        PROJECT_BINARY_DIR=${PROJECT_BINARY_DIR}
#        PROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}
#        PROJECT_GEN_DIR=${PROJECT_GEN_DIR}
#          ${PROJECT_GEN_DIR}/preprocessed-source-compiler.py
#)

add_custom_target (${PROJECT_NAME}_objects
    COMMAND
        CSiBE_BIN_DIR=${CSiBE_BIN_DIR}
        PROJECT_BINARY_DIR=${PROJECT_BINARY_DIR}
        PROJECT_SOURCE_DIR=${PROJECT_SOURCE_DIR}
        PROJECT_GEN_DIR=${PROJECT_GEN_DIR}
        CSIBE_PREPROCESSED_SOURCES="${SRC}"
          #${PROJECT_GEN_DIR}/split_list.py
          ${PROJECT_GEN_DIR}/preprocessed-source-compiler.py
)

add_custom_target (${PROJECT_NAME}_size
    #DEPENDS ${PROJECT_NAME}_objects
    DEPENDS ${SIZE_RESULT}
    COMMAND
        ${SUM_SIZES} ${PROJECT_BINARY_DIR} ${SIZE_RESULT}
)

add_custom_command (OUTPUT ${SIZE_RESULT}
  COMMAND ${SUM_SIZES} ${PROJECT_BINARY_DIR} ${SIZE_RESULT}
  DEPENDS ${PROJECT_NAME}_objects
)

cmake_minimum_required(VERSION 2.8.12 FATAL_ERROR)

project (flex-2.6.0)

set (PROJECT_SOURCE_DIR ${CSiBE_SRC_DIR}/${PROJECT_NAME}/src)
set (PROJECT_INCLUDE_DIR ${PROJECT_SOURCE_DIR})

include_directories (AFTER ${PROJECT_SOURCE_DIR}/src)
include_directories (AFTER ${PROJECT_SOURCE_DIR}/lib)
include_directories (AFTER ${PROJECT_SOURCE_DIR}/test)
include_directories (AFTER ${CSiBE_GEN_DIR}/${PROJECT_NAME})

set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DHAVE_CONFIG_H")
set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -DLOCALEDIR=${PROJECT_SOURCE_DIR}/intl")

include(${CSiBE_GEN_DIR}/CMakeLists.inc)


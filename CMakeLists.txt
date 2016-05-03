cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project("CSiBE")

# CSiBE base directory
set (CSiBE_DIR ${CMAKE_CURRENT_LIST_DIR})

# Inlcude CSiBE's environment
include(${CSiBE_DIR}/cmake/csibe-env.cmake)
include(${CSiBE_DIR}/cmake/subprojects.cmake)

set (CMAKE_BINARY_DIR ${PROJECT_BINARY_DIR})
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set (LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

add_custom_target (size
       COMMAND ${SUM_RESULT} ${CMAKE_BINARY_DIR}/all_results.csv ${CMAKE_C_COMPILER} ${CMAKE_C_FLAGS})

if (NOT DEFINED ENV{CSiBE_SUBPROJECTS})
  # Add bzip2 project
  list (APPEND SUBPROJECTS "bzip2-1.0.6")

  # Add CMSIS project subprojects
  # 'Generic' CMAKE_SYSTEM_NAME means 'an embedded system without OS' here.
  if ((CMAKE_SYSTEM_NAME STREQUAL "Generic"))
    list (APPEND SUBPROJECTS "CMSIS")
  endif ()

  # Add flex project except on embedded
  if ((NOT CMAKE_SYSTEM_NAME MATCHES "Generic"))
    list (APPEND SUBPROJECTS "flex-2.6.0")
    list (APPEND SUBPROJECTS "CSiBE-v2.1.1")
  endif ()

else ()

  set (SUBPROJECTS $ENV{CSiBE_SUBPROJECTS})
  if ("${SUBPROJECTS}" MATCHES " ")
    string (REPLACE " " ";" SUBPROJECTS $ENV{CSiBE_SUBPROJECTS})
  endif()
endif ()

adopt_subprojects()

# Setup the path and target names
foreach (ELEM ${SUBPROJECTS})
  set (NAME)
  string(REGEX REPLACE ".*/" "" NAME ${ELEM})
  add_subdirectory(${CSiBE_GEN_DIR}/${ELEM})
  add_dependencies(size ${NAME}_size)
endforeach(ELEM)

if (NOT SUBPROJECTS)
  message(FATAL_ERROR "No projects to build!")
endif ()


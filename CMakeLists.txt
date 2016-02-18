cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project("CSiBE")

set (CSiBE_VERSION_MAJOR 3)
set (CSiBE_VERSION_MINOR 0)
set (CSiBE_PATCH_VERSION 0)

set (CMAKE_BINARY_DIR ${PROJECT_BINARY_DIR})
set (EXECUTABLE_OUTPUT_PATH ${CMAKE_BINARY_DIR})
set (LIBRARY_OUTPUT_PATH ${CMAKE_BINARY_DIR})

set (CSiBE_DIR ${CMAKE_CURRENT_LIST_DIR})
set (CSiBE_BIN_DIR ${CSiBE_DIR}/bin)
set (CSiBE_GEN_DIR ${CSiBE_DIR}/gen)
set (CSiBE_SRC_DIR ${CSiBE_DIR}/src)

set (DUMP_OBJ_SIZE ${CSiBE_BIN_DIR}/dump_obj_size)
set (SUM_SIZES ${CSiBE_BIN_DIR}/sum_sizes)
set (SUM_RESULT ${CSiBE_BIN_DIR}/sum_results)

add_custom_target (size
       COMMAND ${SUM_RESULT} ${CMAKE_BINARY_DIR}/all_results.csv ${CMAKE_C_COMPILER} ${CMAKE_C_FLAGS})

# PROJECTS
set (PROJECT_LIST)

# Add bzip2 project
list (APPEND SUBPROJECTS "bzip2-1.0.6")

# Add CMSIS project subprojects
# 'Generic' CMAKE_SYSTEM_NAME means 'an embedded system without OS' here.
if ((CMAKE_SYSTEM_NAME STREQUAL "Generic"))
  set (CMSIS_BASE_DIR ${CSiBE_SRC_DIR}/CMSIS)
  set (CMSIS_SUBPROJECTS CMSIS/BasicMathFunctions CMSIS/CommonTables CMSIS/ComplexMathFunctions
        CMSIS/ControllerFunctions CMSIS/FastMathFunctions CMSIS/FilteringFunctions CMSIS/MatrixFunctions
        CMSIS/StatisticsFunctions CMSIS/SupportFunctions CMSIS/TransformFunctions)
  list(APPEND SUBPROJECTS ${CMSIS_SUBPROJECTS})
endif ()

# Add flex project except on embedded
if ((NOT CMAKE_SYSTEM_NAME MATCHES "Generic"))
  list (APPEND SUBPROJECTS "flex-2.6.0")
endif ()

# Setup the path and target names
foreach (ELEM ${SUBPROJECTS})
  set (NAME)
  string(REGEX REPLACE ".*/" "" NAME ${ELEM})
  add_subdirectory(${CSiBE_GEN_DIR}/${ELEM})
  add_dependencies(size ${NAME}_size)
  list(APPEND PROJECT_LIST ${NAME})
endforeach(ELEM)

if (NOT PROJECT_LIST)
  message(FATAL_ERROR "No projects to build!")
endif ()


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
	COMMAND ${SUM_RESULT} ${CMAKE_BINARY_DIR}/all_results.csv)

# PROJECTS
set (PROJECT_LIST)

set (P1 "bzip2-1.0.6")
add_subdirectory(${CSiBE_GEN_DIR}/${P1})
add_dependencies (size ${P1}_size)
list (APPEND PROJECT_LIST ${P1})

# 'Generic' CMAKE_SYSTEM_NAME means 'an embedded system without OS' here.
if ((CMAKE_SYSTEM_NAME STREQUAL "Generic"))
  set (CMSIS_BASE_DIR ${CSiBE_SRC_DIR}/CMSIS)
  set (CMSIS_SUBPROJECTS BasicMathFunctions CommonTables ComplexMathFunctions ControllerFunctions)
  foreach (SUBPROJECT ${CMSIS_SUBPROJECTS})
    add_subdirectory(${CSiBE_GEN_DIR}/CMSIS/${SUBPROJECT})
    add_dependencies(size ${SUBPROJECT}_size)
    list(APPEND PROJECT_LIST ${SUBPROJECT})
  endforeach(SUBPROJECT)
else ()
  set (P2 "flex-2.6.0")
  add_subdirectory(${CSiBE_GEN_DIR}/${P2})
  add_dependencies (size ${P2}_size)
  list (APPEND PROJECT_LIST ${P2})
endif ()

if (NOT PROJECT_LIST)
  message(FATAL_ERROR "No projects to build!")
endif ()


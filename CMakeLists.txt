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

# PROJECTS
set (P1 "bzip2-1.0.6")
add_subdirectory(${CSiBE_GEN_DIR}/${P1})

set (P2 "flex-2.6.0")
add_subdirectory(${CSiBE_GEN_DIR}/${P2})

add_custom_target (size 
	COMMAND ${SUM_RESULT} ${CMAKE_BINARY_DIR}/all_results.csv
	DEPENDS ${P1}_size ${P2}_size)


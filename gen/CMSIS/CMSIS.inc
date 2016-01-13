set (PROJECT_SOURCE_DIR ${CMSIS_BASE_DIR}/CMSIS/DSP_Lib/Source/${PROJECT_NAME})
set (PROJECT_INCLUDE_DIR ${CMSIS_BASE_DIR}/CMSIS/Include)

include_directories (${PROJECT_INCLUDE_DIR})

if (CMAKE_SYSTEM_PROCESSOR STREQUAL "Cortex-M0")
  add_compile_options(-DARM_MATH_CM0)
elseif (CMAKE_SYSTEM_PROCESSOR STREQUAL "Cortex-M4")
  add_compile_options(-DARM_MATH_CM4)
else ()
  message (FATAL_ERROR "Can't compile CMSIS to target CPU!")
endif ()

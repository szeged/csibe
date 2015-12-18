set (PROJECT_SOURCE_DIR ${CMSIS_BASE_DIR}/CMSIS/DSP_Lib/Source/${PROJECT_NAME})
set (PROJECT_INCLUDE_DIR ${CMSIS_BASE_DIR}/CMSIS/Include)

include_directories (${PROJECT_INCLUDE_DIR})

# TODO: Create logic for different target CPUs.
add_compile_options(-DARM_MATH_CM0)

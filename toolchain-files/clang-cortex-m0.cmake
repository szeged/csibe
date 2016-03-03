set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR Cortex-M0)

set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

set(triple arm-none-eabi)

set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

set(CORTEX_M0_FLAGS "--target=${triple} -Os -mcpu=cortex-m0 -mthumb")
set(CMAKE_C_FLAGS "${CORTEX_M0_FLAGS}" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS "${CORTEX_M0_FLAGS}" CACHE STRING "" FORCE)

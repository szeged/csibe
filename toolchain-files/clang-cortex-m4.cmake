set(CMAKE_SYSTEM_NAME Generic)
set(CMAKE_SYSTEM_PROCESSOR Cortex-M4)

set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

set(triple arm-none-eabi)

set(CMAKE_C_COMPILER clang)

set(CORTEX_M4_FLAGS "--target=${triple} -Os -mcpu=cortex-m4 -mthumb -msoft-float")
set(CMAKE_C_FLAGS "${CORTEX_M4_FLAGS}" CACHE STRING "" FORCE)

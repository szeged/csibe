set (PROJECT_RELATIVE_SOURCE_PATH ${PROJECT_NAME})

if ((PROJECT_NAME STREQUAL "flex-2.5.31"))
  add_compile_options (-DHAVE_CONFIG_H)
endif ()

if ((PROJECT_NAME STREQUAL "jikespg-1.3"))
  #set (PROJECT_RELATIVE_SOURCE_PATH "${PROJECT_RELATIVE_SOURCE_PATH}/src")
endif ()

if ((PROJECT_NAME STREQUAL "libmspack"))
  add_compile_options (-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE)
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/libmspack/mspack)
  #set (PROJECT_RELATIVE_SOURCE_PATH "${PROJECT_RELATIVE_SOURCE_PATH}/mspack")
endif ()

if ((PROJECT_NAME STREQUAL "mpeg2dec-0.3.1"))
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/mpeg2dec-0.3.1/include)
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/include)
  # This define has been dropped since glibc 2.17
  add_compile_options (-D__GLIBC_HAVE_LONG_LONG)
  #set (PROJECT_RELATIVE_SOURCE_PATH "${PROJECT_RELATIVE_SOURCE_PATH}/src")
endif ()

# DEBUG
message ("PROJECT_RELATIVE_SOURCE_PATH: ${PROJECT_RELATIVE_SOURCE_PATH}")

if ((PROJECT_NAME STREQUAL "libpng-1.2.5"))
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/zlib)
endif ()

set (PROJECT_SOURCE_DIR ${OLD_CSIBE_BASE_DIR}/CSiBE/src/${PROJECT_RELATIVE_SOURCE_PATH})
set (PROJECT_INCLUDE_DIR ${OLD_CSIBE_BASE_DIR}/CSiBE/src/include)

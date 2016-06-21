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
  if ((CMAKE_SYSTEM_NAME STREQUAL "Generic"))
    include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/include)
  endif ()
  #set (PROJECT_RELATIVE_SOURCE_PATH "${PROJECT_RELATIVE_SOURCE_PATH}/mspack")
endif ()

if ((PROJECT_NAME STREQUAL "libpng-1.2.5"))
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/include/zlib)
endif ()

if ((PROJECT_NAME STREQUAL "mpeg2dec-0.3.1"))
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/mpeg2dec-0.3.1/include)
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/include)
  # This define has been dropped since glibc 2.17
  add_compile_options (-D__GLIBC_HAVE_LONG_LONG)
  add_compile_options (-DDUMMY_ENUM_VALUE=CSIBE_ENUM_VALUE=0xFFFFFFFF)
  #set (PROJECT_RELATIVE_SOURCE_PATH "${PROJECT_RELATIVE_SOURCE_PATH}/src")
endif ()

if ((PROJECT_NAME STREQUAL "OpenTCP-1.0.4"))
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/OpenTCP-1.0.4/include)
  add_compile_options (-D__IO_NEAR -D__io=)
endif ()

if ((PROJECT_NAME STREQUAL "teem-1.6.0-src"))
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/teem-1.6.0-src/include)
  add_compile_options (-DTEEM_32BIT=1
                       -DTEEM_ENDIAN=1234
                       -DTEEM_QNANHIBIT=1
                       -DTEEM_BIGBITFIELD=1
                       -DTEEM_DIO=0
                       -DTEEM32BIT=1)
endif ()

if ((PROJECT_NAME STREQUAL "unrarlib-0.4.0"))
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/unrarlib-0.4.0/unrarlib)
endif ()

# DEBUG
#message ("PROJECT_RELATIVE_SOURCE_PATH: ${PROJECT_RELATIVE_SOURCE_PATH}")

if ((PROJECT_NAME STREQUAL "libpng-1.2.5"))
  include_directories (${OLD_CSIBE_BASE_DIR}/CSiBE/src/zlib)
endif ()

set (PROJECT_SOURCE_DIR ${OLD_CSIBE_BASE_DIR}/CSiBE/src/${PROJECT_RELATIVE_SOURCE_PATH})
set (PROJECT_INCLUDE_DIR ${OLD_CSIBE_BASE_DIR}/CSiBE/src/include)

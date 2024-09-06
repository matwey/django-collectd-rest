cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES C)

set(CMAKE_C_STANDARD 99)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(PkgConfig REQUIRED)
pkg_check_modules(LIBRRD REQUIRED IMPORTED_TARGET librrd)

python_add_library(rrd MODULE c_src/rrd.c WITH_SOABI)
target_link_libraries(rrd PRIVATE PkgConfig::LIBRRD)
set_property(TARGET rrd PROPERTY INTERPROCEDURAL_OPTIMIZATION True)

install(TARGETS rrd DESTINATION collectd_rest)

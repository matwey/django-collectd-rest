cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES C)

include(CheckCSourceCompiles)

set(CMAKE_C_STANDARD 99)

function(check_mutable_argv)
    set(CMAKE_REQUIRED_LIBRARIES PkgConfig::LIBRRD)
    check_c_source_compiles(
        "
        #include <rrd.h>

        int main() {
            (void)rrd_graph_v(0, (char**)NULL);
            return 0;
        }
        "
        LIBRRD_HAS_MUTABLE_ARGV)
    unset(CMAKE_REQUIRED_LIBRARIES)
endfunction()

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(PkgConfig REQUIRED)
pkg_check_modules(LIBRRD REQUIRED IMPORTED_TARGET librrd)

check_mutable_argv()

python_add_library(rrd MODULE c_src/rrd.c WITH_SOABI)
target_link_libraries(rrd PRIVATE PkgConfig::LIBRRD)
if(LIBRRD_HAS_MUTABLE_ARGV)
    target_compile_definitions(rrd PRIVATE LIBRRD_HAS_MUTABLE_ARGV)
endif()
set_property(TARGET rrd PROPERTY INTERPROCEDURAL_OPTIMIZATION True)

install(TARGETS rrd DESTINATION collectd_rest)

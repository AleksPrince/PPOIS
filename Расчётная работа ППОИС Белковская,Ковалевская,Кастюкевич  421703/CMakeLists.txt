file(GLOB SOURCES CONFIGURE_DEPENDS "*.cpp" "*.hpp" "agent/*.cpp" "agent/*.hpp" "keynodes/*.hpp")

add_library(network_module SHARED ${SOURCES})

target_link_libraries(network_module LINK_PUBLIC sc-machine::sc-memory
  LINK_PUBLIC sc-machine::sc-core)
target_include_directories(network_module PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

find_package(GTest REQUIRED)
include(GoogleTest)

file(GLOB TEST_SOURCES CONFIGURE_DEPENDS "test/*.cpp")
add_executable(network_module-tests ${TEST_SOURCES})

target_link_libraries(network_module-tests LINK_PRIVATE GTest::gtest_main LINK_PRIVATE network_module)
target_include_directories(network_module-tests PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

if(NOT DEFINED SC_EXTENSIONS_DIRECTORY)
    set(SC_EXTENSIONS_DIRECTORY "${CMAKE_BINARY_DIR}/lib/extensions")
endif()

set_target_properties(network_module PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${SC_EXTENSIONS_DIRECTORY}")

gtest_discover_tests(network_module-tests TEST_LIST ${TEST_SOURCES} WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/test)

cmake_minimum_required(VERSION 3.16)
project(cpp_linux_backend_mini LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(echo_server
    src/echo_server.cpp
)
target_include_directories(echo_server PUBLIC include)

add_executable(echo_server_main
    src/main.cpp
)
target_link_libraries(echo_server_main PRIVATE echo_server)

add_executable(test_echo_server
    tests/test_echo_server.cpp
)
target_link_libraries(test_echo_server PRIVATE echo_server)

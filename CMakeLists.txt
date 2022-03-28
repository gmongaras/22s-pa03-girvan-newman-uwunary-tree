# Version Requirement
cmake_minimum_required(VERSION 3.15)

# Project Name
project(22s-pa03-girvan-newman-uwunary-tree)

# Executable
add_executable(22s-pa03-girvan-newman-uwunary-tree src/main.cpp)

# Configure Files
file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/data DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# Other Important Functions
# set(CMAKE_CXX_STANDARD 14)
# configure_file(output/outfile.csv output/outfile.csv COPYONLY)
# file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/data DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
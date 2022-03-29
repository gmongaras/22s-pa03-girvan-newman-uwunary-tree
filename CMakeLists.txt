# Fantastic Linking Article: https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory?page=2&tab=scoredesc#tab-top

# Version Requirement
cmake_minimum_required(VERSION 3.15)

# Project Name
project(22s-pa03-girvan-newman-uwunary-tree)

# Executable
add_executable(22s-pa03-girvan-newman-uwunary-tree src/main.cpp src/dataGenerator.py)

# Configure Files
file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/data DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# Boost Basic Settings
set(Boost_USE_STATIC_LIBS OFF)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)

# Finds Boost Packages (Minimum 1.71.0 Requirement, Will Output)
find_package(Boost 1.71.0 REQUIRED COMPONENTS graph system filesystem)
message(STATUS "Boost version: ${Boost_VERSION}")

# Necessary Statement If Cmake Ver < Boost Ver
# if(NOT TARGET Boost::filesystem)
#     add_library(Boost::filesystem IMPORTED INTERFACE)
#     set_property(TARGET Boost::filesystem PROPERTY INTERFACE_INCLUDE_DIRECTORIES ${Boost_INCLUDE_DIR})
#     set_property(TARGET Boost::filesystem PROPERTY INTERFACE_LINK_LIBRARIES ${Boost_LIBRARIES})
# endif()

# Find Python Packages (Interpreter and Development Artifacts)
find_package(Python REQUIRED COMPONENTS Interpreter Development)
message(STATUS "Python version: ${Python_VERSION}")
find_package(PythonLibs REQUIRED)

# Include Python Directories (Important Stuff)
include_directories(${PYTHON_INCLUDE_DIRS})

# Linking Correct Libraries (In Find Package) (Must End File)
target_link_libraries(22s-pa03-girvan-newman-uwunary-tree
        PUBLIC Boost::graph
        PUBLIC Boost::system
        PUBLIC Boost::filesystem
        PUBLIC ${PYTHON_LIBRARIES})

# Only One Target Link is Allowed, See Above
# target_link_libraries(22s-pa03-girvan-newman-uwunary-tree ${PYTHON_LIBRARIES})

# Other Important Functions
# set(CMAKE_CXX_STANDARD 14)
# configure_file(output/outfile.csv output/outfile.csv COPYONLY)
# file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/data DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

# Basic Template For Cmake File:
# Version
# Project
# Executable Configuration
# File Configuration
# Find Packages/Settings
# Include Directories
# Link Libraries
# Note: There Can Only Be One Library Link!
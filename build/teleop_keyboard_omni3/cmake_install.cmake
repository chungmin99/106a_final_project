# Install script for directory: /home/thitikhomin/ros_workspaces/106a_final_project/src/teleop_keyboard_omni3

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/thitikhomin/ros_workspaces/106a_final_project/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/thitikhomin/ros_workspaces/106a_final_project/build/teleop_keyboard_omni3/catkin_generated/installspace/teleop_keyboard_omni3.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/teleop_keyboard_omni3/cmake" TYPE FILE FILES
    "/home/thitikhomin/ros_workspaces/106a_final_project/build/teleop_keyboard_omni3/catkin_generated/installspace/teleop_keyboard_omni3Config.cmake"
    "/home/thitikhomin/ros_workspaces/106a_final_project/build/teleop_keyboard_omni3/catkin_generated/installspace/teleop_keyboard_omni3Config-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/teleop_keyboard_omni3" TYPE FILE FILES "/home/thitikhomin/ros_workspaces/106a_final_project/src/teleop_keyboard_omni3/package.xml")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/teleop_keyboard_omni3" TYPE PROGRAM FILES "/home/thitikhomin/ros_workspaces/106a_final_project/build/teleop_keyboard_omni3/catkin_generated/installspace/teleop_keyboard_omni3.py")
endif()

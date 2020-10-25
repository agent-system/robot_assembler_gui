cmake_minimum_required(VERSION 3.0.2)
project(robot_assembler_gui)
find_package(catkin REQUIRED)
catkin_package()
catkin_python_setup()

install(FILES plugin.xml
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

install(DIRECTORY launch resources
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

#catkin_install_python(PROGRAMS scripts/robot_assembler_gui
#  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
#)

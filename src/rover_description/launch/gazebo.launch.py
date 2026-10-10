import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # Find the robot file and the Gazebo launch file
    pkg_share = get_package_share_directory('rover_description')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')
    xacro_file = os.path.join(pkg_share, 'urdf', 'rover.urdf.xacro')

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str)

    # 1. Start Gazebo (empty world)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')))

    # 2. Share the robot description
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True}],
        output='screen')

    # 3. Spawn the rover into Gazebo
    spawn_rover = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-entity', 'rover',
                   '-z', '0.05'],
        output='screen')

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_rover,
    ])
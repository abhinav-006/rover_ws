import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    nav_share = get_package_share_directory('rover_navigation')
    params_file = os.path.join(nav_share, 'config', 'slam_params.yaml')

    slam = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[params_file, {'use_sim_time': True}])

    return LaunchDescription([slam])
import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os



def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='robovolc_rosys').find('robovolc_rosys')
    default_model_path = os.path.join(pkg_share, 'urdf/robovolc.urdf')
    default_world_path = os.path.join(pkg_share, 'world/gazebo_ros_imu_sensor.world')

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': Command(['xacro ', LaunchConfiguration('model')]),
            'use_sim_time': True
        }]
    )

    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': True}]
    )

    spawn_entity = launch_ros.actions.Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'robovolc', '-topic', 'robot_description', '-z', '0.45'],
        output='screen'
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='world', default_value=default_world_path,
                                            description='Absolute path to Gazebo world file'),
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', LaunchConfiguration('world'), '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'], output='screen'),
        joint_state_publisher_node,
        robot_state_publisher_node,
        spawn_entity,
    ])
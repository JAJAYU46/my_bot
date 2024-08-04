#下面這個launch檔就是會直接在3個terminal連做下面三件事直接包成一個launch檔, 這樣就會比較輕鬆, 但做起來是一樣的
'''
ros2 launch my_bot rsp.launch.py use_sim_time:=true #把這個urdf file publish到re.._description這個topic上(use_sim_time:=true要讓這個程式跑得是gazebo simulation的時間不然會出錯)
ros2 launch gazebo_ros gazebo.launch.py #開啟一個空白的gazebo(gazebo_ros是一個gazebo內建的ros package裡面有很多功能)
ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity my_little_bot #"spawn"就是把urdf檔轉成stf檔(for gazebo的模型檔)
(用gazebo_ros的package裡的spawn_entity.py把topic robot_description上面的urdf file輸入到我的gazebo環境)
(這隻robot的entity叫做my_little_bot(robot_name))
'''
import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!
    #要從你的my_bot>>launch>>rsp.launch.py去include檔案rsp.launch.py, 所以下面要改成你的package_name
    package_name='my_bot' #<--- [CHANGE ME]

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py' #launch rsp.launch.py
                )]), launch_arguments={'use_sim_time': 'true'}.items() #use_sim_time'要為'true'
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')



    # Launch them all!
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])
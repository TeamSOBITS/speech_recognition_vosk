from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    stt_name_arg = DeclareLaunchArgument(
        "stt_name",
        default_value="vosk",
        description="STT engine name (whisper, vosk, etc.)"
    )

    model_arg = DeclareLaunchArgument(
        "model",
        default_value="vosk-model-small-en-us-0.15",
        description="Vosk model name"
    )
    mic_volume_arg = DeclareLaunchArgument(
        "mic_volume",
        default_value="",
        description="Microphone volume percentage"
    )
    use_echo_cancel_arg = DeclareLaunchArgument(
        "use_echo_cancel",
        default_value="False",
        description="Enable WebRTC echo cancellation"
    )
    noise_suppression_arg = DeclareLaunchArgument(
        "noise_suppression",
        default_value="False",
        description="Enable noise suppression"
    )
    analog_gain_arg = DeclareLaunchArgument(
        "analog_gain_control",
        default_value="False",
        description="Enable automatic analog gain control"
    )
    digital_gain_arg = DeclareLaunchArgument(
        "digital_gain_control",
        default_value="False",
        description="Enable digital gain control"
    )

    vosk_node = Node(
        package='speech_recognition_vosk',
        executable='vosk_node',
        name='vosk_node',
        output='screen',
        parameters=[{
            'stt_name': LaunchConfiguration('stt_name'), # ここが重要
            'model': LaunchConfiguration('model'),
            'mic_volume': LaunchConfiguration('mic_volume'),
            'use_echo_cancel': LaunchConfiguration('use_echo_cancel'),
            'noise_suppression': LaunchConfiguration('noise_suppression'),
            'analog_gain_control': LaunchConfiguration('analog_gain_control'),
            'digital_gain_control': LaunchConfiguration('digital_gain_control'),
        }],
    )

    return LaunchDescription([
        stt_name_arg,
        model_arg,
        mic_volume_arg,
        use_echo_cancel_arg,
        noise_suppression_arg,
        analog_gain_arg,
        digital_gain_arg,
        vosk_node
    ])
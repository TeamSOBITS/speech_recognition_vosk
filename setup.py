from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'speech_recognition_vosk'

setup(
    name=package_name,
    version='0.0.0',
    # packages=find_packages(exclude=['test']),
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'sound_file'), glob('sound_file/*.wav')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sobits',
    maintainer_email='sobits@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    entry_points={
        'console_scripts': [
            'model_downloader = speech_recognition_vosk.model_downloader:main',
            'vosk_node = speech_recognition_vosk.vosk_node:main',
        ],
    },
)
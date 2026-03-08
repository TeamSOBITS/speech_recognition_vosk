#!/bin/bash

echo "╔══╣ Install: Speech Recognition Vosk for ROS (OPTIMIZED) ╠══╗"

export PIP_BREAK_SYSTEM_PACKAGES=1

CURRENT_DIR=$(pwd)

sudo apt update
sudo apt install -y \
    python3-tk \
    pulseaudio-utils \
    libc++1 \

python3 -m pip install -U pip
python3 -m pip install \
    vosk \

pip3 install -U "numpy==1.26.4" \

cd ..
if [ ! -d "sobits_interfaces" ]; then
    git clone -b jazzy-devel https://github.com/TeamSOBITS/sobits_interfaces.git
else
    echo "sobits_interfaces already exists. Skipping clone."
fi

cd "$CURRENT_DIR"

echo "╚══╣ Install: Speech Recognition Vosk for ROS (FINISHED) ╠══╝"
<a name="readme-top"></a>

[JA](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# Speech Recognition VOSK

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#introduction">Introduction</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#model-download-instructions">Model Download Instructions</a></li>
    <li><a href="#launch-and-usage">Launch and Usage</a></li>
    <li><a href="#parameters">Parameters</a></li>
    <li><a href="#milestones">Milestones</a></li>
  </ol>
</details>


## Introduction

This repository provides the automatic speech recognition (ASR) capabilities of OpenAI's [Vosk](https://github.com/alphacep/vosk-api) and [ros_vosk](https://github.com/alphacep/ros-vosk) adapted for ROS2 action communication.

It runs in a local environment.

<!-- GETTING STARTED -->
## Getting Started

This section describes how to set up this repository.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Prerequisites

First, please set up the following environment before proceeding to the next installation stage.

| System  | Version |
| ------------- | ------------- |
| Ubuntu | 24.04 (Noble Numbat) |
| ROS | Jazzy Jalisco |
| Python | 3.12 |


<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Installation

1. Navigate to your ROS2 src folder.
    ```sh
    cd ~/colcon_ws/src/
    ```
2. Clone this repository．
    ```sh
    git clone -b jazzy-devel https://github.com/TeamSOBITS/speech_recognition_vosk.git
    ```
3. Move into the repository directory.
    ```sh
    cd speech_recognition_vosk/
    ```
4. Install dependent packages
    ```sh
    bash install.sh
    ```
5. Compile the package.
    ```sh
    cd ~/colcon_ws/
    ```
    ```sh
    colcon build --symlink-install
    ```
    ```sh
    source ~/colcon_ws/install/setup.sh
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Model Download Instructions

1. **Launch the GUI** using the following command:
    ```bash
    ros2 run speech_recognition_vosk model_downloader
    ```

> **Note**
> You can use any language model from the [list of models compatible with Vosk-API](https://alphacephei.com/vosk/models).

2. The following GUI will appear:
    ![img1](img/image.png)  
    - To use English:
      - Select language: English
      - Select model: vosk-model-small-en-us-0.15

    - To use Japanese:
      - Select Model: Japanese
      - Select model: vosk-model-ja-0.22
    - You can verify the downloaded models by running:
      ```bash
      ls ~/.vosk_models/
      ```


## Launch and Usage

1. In Ubuntu settings, set the input device for sound to the microphone you intend to use.

2. Start the Action Server. Please wait for **Vosk Server READY** to appear before sending any goals.
    ```sh
    ros2 launch speech_recognition_vosk speech_recognition_vosk.launch.py 
    ```
3. Start the Action Client and send the text you want to speak.
    - timeout_sec: Duration (in seconds) to keep the microphone open. If a negative value is provided, it continues to return feedback until a cancel request is sent.
    - silent_mode: If set to `true`, the start and end notification sounds will not be played.
    - feedback_rate: Specifies the frequency of intermediate speech recognition results when `use_feedback` is `True` and `vad_name` is `None`.

    ```sh
    ros2 action send_goal /speech_recognition sobits_interfaces/action/SpeechRecognition "timeout_sec: 5
    silent_mode: false
    feedback_rate: 0.5" -f
    ```
    Recorded audio is saved in the sound_file directory.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Parameters

The following parameters can be set in [speech_recognition_vosk.launch.py](launch/speech_recognition_vosk.launch.py).

| Parameter | Description | Default Value |
| :--- | :--- | :--- |
| **`model`** | The VOSK model to use. *1 | `vosk-model-small-en-us-0.15` |
| **`mic_volume`** | Sets the microphone input volume as a percentage. When finish program, the original volume will be restored. e.g., "150%" | `""` |
| **`use_feedback`** | Whether to enable work-in-progress (WIP) speech recognition feedback. | `True` |

The following are parameters related to echo cancellation.

| Parameter | Description | Default Value |
| :--- | :--- | :--- |
| **`use_echo_cancel`** | Whether to use echo cancellation. | `False` |
| **`noise_suppression`** | Whether to use noise suppression. | `False` |
| **`analog_gain_control`** | Whether to use analog gain control. | `False` |
| **`digital_gain_control`** | Whether to use digital gain control. | `False` |


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Milestone

See the [open issues][issues-url] for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/TeamSOBITS/speech_recognition_vosk.svg?style=for-the-badge
[contributors-url]: https://github.com/TeamSOBITS/speech_recognition_vosk/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TeamSOBITS/speech_recognition_vosk.svg?style=for-the-badge
[forks-url]: https://github.com/TeamSOBITS/speech_recognition_vosk/network/members
[stars-shield]: https://img.shields.io/github/stars/TeamSOBITS/speech_recognition_vosk.svg?style=for-the-badge
[stars-url]: https://github.com/TeamSOBITS/speech_recognition_vosk/stargazers
[issues-shield]: https://img.shields.io/github/issues/TeamSOBITS/speech_recognition_vosk.svg?style=for-the-badge
[issues-url]: https://github.com/TeamSOBITS/speech_recognition_vosk/issues
[license-shield]: https://img.shields.io/github/license/TeamSOBITS/speech_recognition_vosk.svg?style=for-the-badge
[license-url]: LICENSE
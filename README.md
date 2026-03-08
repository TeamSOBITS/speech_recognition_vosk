<a name="readme-top"></a>

[JA](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

# Speech Recognition VOSK
<!-- 目次 -->
<details>
  <summary>目次</summary>
  <ol>
    <li>
      <a href="#概要">概要</a>
    </li>
    <li>
      <a href="#セットアップ">セットアップ</a>
      <ul>
        <li><a href="#環境条件">環境条件</a></li>
        <li><a href="#インストール方法">インストール方法</a></li>
      </ul>
    </li>
    <li><a href="#モデルダウンロード方法">モデルダウンロード方法</a></li>
    <li><a href="#実行操作方法">実行・操作方法</a></li>
    <li><a href="#パラメータ">パラメータ</a></li>
    <li><a href="#マイルストーン">マイルストーン</a></li>
  </ol>
</details>



## 概要
これ本リポジトリは，[Vosk](https://github.com/alphacep/vosk-api)と[ros_vosk](https://github.com/alphacep/ros-vosk)の自動音声認識（ASR）機能を
ROS2のアクション通信に対応させたものです．

ローカル環境で動作します．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- セットアップ -->
## セットアップ

ここで，本レポジトリのセットアップ方法について説明します．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


### 環境条件

まず，以下の環境を整えてから，次のインストール段階に進んでください．

| System  | Version |
| ------------- | ------------- |
| Ubuntu | 24.04 (Noble Numbat) |
| ROS | Jazzy Jalisco |
| Python | 3.12 |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


### インストール方法

1. ROSの`src`フォルダに移動します．
   ```sh
   cd ~/colcon_ws/src/
   ```
2. 本レポジトリをcloneします．
   ```sh
   git clone -b jazzy-devel https://github.com/TeamSOBITS/speech_recognition_vosk.git
   ```
3. レポジトリの中へ移動します．
   ```sh
   cd speech_recognition_vosk
   ```
4. 依存パッケージをインストールします．
   ```sh
   bash install.sh
   ```
5. パッケージをコンパイルします．
   ```sh
   cd ~/colcon_ws/
   ```
   ```
   colcon build --symlink-install
   ```
   ```
   source ~/colcon_ws/install/setup.sh
   ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>



## モデルダウンロード方法

1. 以下のコマンドでGUIを起動します．

    ```bash
    ros2 run speech_recognition_vosk model_downloader
    ```

> **Note**
> [list of models compatible with Vosk-API](https://alphacephei.com/vosk/models).の言語モデルを使用できます．


2. 以下のようなGUIが表示されます．
    ![img1](img/image.png)  
    - 英語を使用する場合：
      - Select language：English
      - Select model：vosk-model-small-en-us-0.15

    - 日本語を使用する場合：
      - Select Model：Japanese
      - Select model：vosk-model-ja-0.22
    - ダウンロードしたモデルは以下のコマンドでも確認できます
      ```sh
      ls ~/.vosk_models/
      ```

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


## 実行・操作方法

1. Ubuntuの設定で，サウンドの入力デバイスを使用するマイクに設定します．

2. Action Serverを起動します．

  ```sh
  ros2 launch speech_recognition_vosk speech_recognition_vosk.launch.py
  ```

3. Action Clientを起動します．
  - timeout_sec: マイクを開く秒数．負の値のときキャンセルを送信するまでフィードバックを返し続ける
  - silent_mode: trueのときは検出時と終了時に音がならない
  - feedback_rate: use_feedbackがTrueでvad_nameがNoneのときに返ってくる途中の音声認識結果の頻度
  ```sh
  ros2 action send_goal /speech_recognition sobits_interfaces/action/SpeechRecognition "timeout_sec: 5
  silent_mode: false
  feedback_rate: 0.5" -f
  ```
  録音された音声はsound_fileディレクトリに保存されます．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## パラメータ

`speech_recognition_vosk.launch.py` では以下のパラメータを指定できます．

| パラメータ名   | 説明                                                                                  | デフォルト値                                                   |
|---------------|---------------------------------------------------------------------------------------|--------------------------------------------------------------|
| model| 使用するVOSKモデル．軽量モデルや大容量モデルなどを選択できる．| vosk-model-small-en-us-0.15|
| mic_volume | マイクの入力音量をパーセンテージで設定する．プログラム終了後は元の音量に戻る．例: "150%" | "" |
| use_feedback | 音声認識の途中結果(フィードバック)を有効にするかどうか | True |

以下はエコーキャンセルに関するパラメータです．
`use_echo_cancel`が`True`のときに有効です．

| パラメータ | 説明 | デフォルト値 |
| - | - | - |
| use_echo_cancel | そのPCのスピーカーからの音をマイクが拾わないようにする． | False |
| noise_suppression | ノイズを抑制する． | False |
| analog_gain_control | マイクのハードウェアレベルで入力音量を自動調整する．大きな音は抑え，小さな音は増幅することで音割れや聞き取りにくさを防ぐ． | False |
| digital_gain_control | ソフトウェアレベルで入力音量を自動調整する．音声データがデジタル化された後に振幅を調整する． | False |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


<!-- MILESTONE -->
## マイルストーン
現時点のバッグや新規機能の依頼を確認するために[Issueページ][license-url] をご覧ください．


<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

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

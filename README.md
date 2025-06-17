<a name="readme-top"></a>

[JA](README.md) | [EN](README.en.md)

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]

Speech Recognition VOSK
======================
<!--  TABLE OF CONTENTS -->
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
    <li><a href="#インターフェイス">インターフェイス</a></li>
    <li><a href="#マイルストーン">マイルストーン</a></li>
  </ol>
</details>



## 概要
これは,[Vosk](https://github.com/alphacep/vosk-api)と[ros_vosk](https://github.com/alphacep/ros-vosk)に基づく音声テキストサービス用のROSパッケージになります.
ローカルで動作する，音声認識パッケージです.
他の音声認識パッケージと同じように，Action通信で使えます．
また，性質上GPUのPCを推奨します．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

<!-- セットアップ -->
## セットアップ

ここで，本レポジトリのセットアップ方法について説明します．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


### 環境条件

まず，以下の環境を整えてから，次のインストール段階に進んでください．

| System  | Version |
| ------------- | ------------- |
| Ubuntu | 22.04 (Jammy Jellyfish) |
| ROS | Humble Hawksbill |
| Python | 3.10 |実行・操作方法


<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


### インストール方法

1. ROSの`src`フォルダに移動します．
   ```sh
   cd ~/colcon_ws/src/
   ```
2. 本レポジトリをcloneします．
   ```sh
   git clone -b humble-devel https://github.com/TeamSOBITS/speech_recognition_vosk.git
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

1. 使用したいモデルをダウンロードします．
```bash
ros2 run speech_recognition_vosk model_downloader
```

> **Note**
> [list of models compatible with Vosk-API](https://alphacephei.com/vosk/models).の言語モデルを使用できます．

> **Note**
> モデルがデータベースに存在すれば，自動的にダウンロードされるはずです．

2. モデルを選択する．

最初の実行では，モデルをダウンロードするために以下のようなGUI画面が表示されます．
![img1](img/image.png)  
- 英語を使用する場合：
  - Select language：English
  - Select model：vosk-model-small-en-us-0.15

- 日本語を使用する場合：
  - Select Model：Japanese
  - Select model：vosk-model-ja-0.22

> [!WARNING]
>　モデルを入れる階層は~/colcon_ws/src/speech_recognition_vosk/modelsに入れてください．


<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


## 実行・操作方法

1.Action Serverを起動します．
```
ros2 launch speech_recognition_vosk speech_recognition_vosk.launch.py
```
2.Action Clientを起動します．

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>

## パラメータ

`speech_recognition_vosk.launch.py` では以下のパラメータを指定できます．

| パラメータ名   | 説明                                                                                  | デフォルト値                                                   |
|---------------|---------------------------------------------------------------------------------------|--------------------------------------------------------------|
| `model`       | 使用するVOSKモデル．軽量モデルや大容量モデルなどを選択できる．                                | `models/vosk-model-small-en-us-0.15`                        |
| `sample_rate` | 1秒あたりの音声データ変換回数．高いほど音質が向上し，拾える周波数範囲が広がる．高くするとデータ量と負荷が増え，低くすると音質が劣化する可能性がある． | `44100`                                                      |
| `blocksize`   | 一度に処理する音声データの塊のサイズ．リアルタイム性と処理負荷のバランスを決定する．大きくすると応答が遅くなり，小さくするとCPU負荷が高まる可能性がある．                                | `16000`                                                      |

<p align="right">(<a href="#readme-top">上に戻る</a>)</p>


## インターフェイス

### Topics
- （※現状，音声結果はトピックでは配信していません）

### Services
- `/vosk_node/describe_parameters`  
- `/vosk_node/get_parameter_types`  
- `/vosk_node/get_parameters`  
- `/vosk_node/list_parameters`  
- `/vosk_node/set_parameters`  
- `/vosk_node/set_parameters_atomically`  

### Actions
- `/speech_recognition`  
  - リクエスト：`sobits_interfaces/action/SpeechRecognition`  
  - 途中経過を `feedback`，最終結果を `result` で受け取る

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

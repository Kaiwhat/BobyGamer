# Playing Classic Game with Body Gestures using Pose Detection

## Overview
本專案結合 **Mediapipe** 和 **OpenCV**，使用 **Python** 實做一個能用肢體動作來遊玩遊戲的專案。通過姿勢檢測捕捉玩家的動作，並將其轉換為對應的遊戲操作，例如跳躍、蹲下及左右閃避。

## Features
- **Pose Detection**: 利用 Mediapipe 的肢體辨識模型來即時偵測與追蹤玩家動作。
- **Gesture Mapping**: 將特定手勢（如舉手、下蹲）映射到遊戲內的動作。
- **Seamless Integration**: 可與正在運行的遊戲配合，檢測姿勢模擬鍵盤輸入。

## Prerequisites
### Hardware Requirements
- 鏡頭或外接相機，用於捕捉玩家動作。
- 配備足夠運算能力的電腦，作即時影像處理。

### Software Requirements
- Python 3.7 或更高版本
- Subway Surfers game installed (preferably on a Windows system for easy keyboard emulation).

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Kaiwhat/BobyGamer.git
   cd BodyGamer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Ensure the following libraries are included in `requirements.txt`:
   - mediapipe
   - opencv-python
   - pyautogui

3. Test the environment:
   ```bash
   python3 app.py
   ```
   This script will verify the webcam functionality and Mediapipe pose detection.

## Usage
1. 允許 http 網站打開攝影機
2. 打開 google chrome 的實驗性功能，在 chrome 網址打上：
   ```
   chrome://flags/#unsafely-treat-insecure-origin-as-secure
   ```
3. 在 Insecure origins treated as secure 打上 http://我們的server IP，然後 enable
4. 最後 Relaunch，左上角會跳出使用攝影機的請求

1. 啟動遊戲，進入遊戲畫面。
2. 打開主程式
3. 執行以下動作以控制遊戲：
   - **跳躍**: 遊戲中跳躍
   - **蹲下**: 遊戲中蹲下
   - **往左平移**: 遊戲中左閃
   - **往右平移**: 遊戲中右閃

4. 使用肢體手勢享受新的遊戲體驗！

## Project Structure
```
subway-surfers-gesture-control/
├── README.md            # Project documentation
├── requirements.txt     # List of dependencies
├── pose_detection_test.py # Script to test pose detection
├── gesture_control.py   # Main script for gesture-based game control
├── utils/               # Utility scripts for gesture mapping and debugging
│   ├── gesture_mapping.py
│   ├── video_utils.py
```

## How It Works
1. **姿勢檢測**：
   - Mediapipe 識別身體關鍵點（肩膀、嘴巴）。
   - 處理檢測到的關鍵點以判斷手勢。

2. **手勢映射**：
   - 使用 `gesture_mapping.py` 中的自定義邏輯將特定手勢映射到遊戲操作。

3. **鍵盤模擬**：
   - 檢測到的手勢通過 `pyautogui` libary 觸發對應的鍵盤輸入。

## Acknowledgments
- [Mediapipe](https://google.github.io/mediapipe/) for pose detection.
- [OpenCV](https://opencv.org/) for video processing.
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for keyboard emulation.

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

Enjoy playing Subway Surfers with your body movements! 🚀

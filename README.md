# Playing Classic Game with Body Gestures using Pose Detection

## Concept Development
本專案結合 **Mediapipe** 與 **OpenCV**，基於 **Python** 開發一個利用肢體動作進行遊戲操控的系統。通過姿態檢測技術，實時捕捉玩家的動作並將其轉換為遊戲中的操作指令，例如跳躍、蹲下以及左右閃避。此系統旨在提供更直觀的互動方式，實現肢體動作與數位遊戲的無縫結合

## Implementation Resources(硬體資源)
- 有鏡頭的電腦
- CPU運算能力: i5 4210u UP

## Existing Library/Software
- **Python**: 3.7 或更高版本
- **Mediapipe**: 用於肢體辨識模型來即時偵測與追蹤玩家動作。
  Git: [Mediapipe](https://github.com/google-ai-edge/mediapipe)
- **Open-CV** : 用於影像處理
  Git: [OpenCV](https://github.com/opencv/opencv)
- **PyAutoGUI** : 用指令操作鍵盤
  Git: [PyAutoGUI](https://github.com/asweigart/pyautogui)
- **Gesture Mapping**: 將特定手勢（如舉手、下蹲）映射到遊戲內的動作。
- **Seamless Integration**: 可與正在運行的遊戲配合，檢測姿勢模擬鍵盤輸入。

## Architecture

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
## Implementation Process
1. **姿勢檢測**：
   - Mediapipe 識別身體關鍵點（肩膀、嘴巴）。
   - 處理檢測到的關鍵點以判斷手勢。

2. **手勢映射**：
   - 使用 `gesture_mapping.py` 中的自定義邏輯將特定手勢映射到遊戲操作。

3. **鍵盤模擬**：
   - 檢測到的手勢通過 `pyautogui` libary 觸發對應的鍵盤輸入。

-  for keyboard emulation.

## Ref.
https://youtu.be/Z2EGhplFOHs?feature=shared
https://github.com/web-tunnel/lite-http-tunnel
https://blog.csdn.net/qq_43530326/article/details/130974058

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

Enjoy playing Subway Surfers with your body movements! 🚀

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


## 遇到問題

## 分工表

## 感謝名單

## Reference


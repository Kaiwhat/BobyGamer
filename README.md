# Playing Classic Game with Body Gestures using Pose Detection

## Concept Development
本專案結合 **Mediapipe** 與 **OpenCV**，基於 **Python** 開發一個利用肢體動作進行遊戲操控的系統。通過姿態檢測技術，實時捕捉玩家的動作並將其轉換為遊戲中的操作指令，例如跳躍、蹲下以及左右閃避。此系統旨在提供更直觀的互動方式，實現肢體動作與數位遊戲的無縫結合

## Implementation Resources(硬體資源)
- 有鏡頭的電腦
- CPU運算能力: i5 4210u UP

## Existing Library/Software
- **Python**: 3.7 UP
- **[Mediapipe](https://github.com/google-ai-edge/mediapipe)**: 用於肢體辨識模型來即時偵測與追蹤玩家動作。
- **[Open-CV](https://github.com/opencv/opencv)** : 用於影像處理
- **[PyAutoGUI](https://github.com/asweigart/pyautogui)** : 用指令操作鍵盤
- **[Gesture Mapping](https://github.com/dang-hai/GestureMap)**: 將特定手勢（如舉手、下蹲）映射到遊戲內的動作。
- **[Seamless Integration]**: 可與正在運行的遊戲配合，檢測姿勢模擬鍵盤輸入。
- **[mySQL]**: 紀錄 flappy bird 的英雄榜。
- **[Flask]**: 用於架設網站。
- **[Socket]**
- **[Express]**
- **[cors]**

## Architecture
![image](https://github.com/user-attachments/assets/0e320176-1129-4dd9-812f-f1a853d5c44a)



## Implementation Process
### 遊戲:
   1. **姿勢檢測**：
      - Mediapipe 識別身體關鍵點（肩膀、嘴巴）。
      - 處理檢測到的關鍵點以判斷手勢。
   
   2. **手勢映射**：
      - 使用 `gesture_mapping.py` 中的自定義邏輯將特定手勢映射到遊戲操作。
   
   3. **鍵盤模擬**：
      - 檢測到的手勢通過 `pyautogui` libary 觸發對應的鍵盤輸入。
### 伺服器:
  



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
   - flask

3. Test the environment:
   ```bash
   python3 app.py
   ```
   This script will verify the webcam functionality and Mediapipe pose detection.
   
## Usage
1. 允許 http 網站打開攝影機
  - step 1.
    ![image](https://github.com/user-attachments/assets/60db5236-a05f-4a8f-914d-273a53745faf)
  - step 2.
    ![image](https://github.com/user-attachments/assets/3c647c32-7640-4483-a192-11c22765102d)

3. 打開 google chrome 的實驗性功能，在 chrome 網址打上：
   ```
   chrome://flags/#unsafely-treat-insecure-origin-as-secure
   ```
4. 在 Insecure origins treated as secure 打上 http://我們的server IP，然後 enable
![image](https://github.com/user-attachments/assets/c73462e6-a4f0-433d-90bf-47b3e83607d0)
5. 最後 Relaunch，左上角會跳出使用攝影機的請求
6. 啟動遊戲，進入遊戲畫面。
7. 執行以下動作以控制遊戲：
- **水管鳥**:
   - **跳躍**: 遊戲中跳躍
- **地鐵跑酷**:
   - **跳躍**: 遊戲中跳躍
   - **蹲下**: 遊戲中蹲下
   - **往左平移**: 遊戲中左閃
   - **往右平移**: 遊戲中右閃
- **乒乓球**:
   - **左/右手觸碰鏡頭畫面邊框**: 球拍左/右移動
- **身體指令**:
   - **OK手勢**：執行ENTER動作
   - **鳥手勢**：開啟 _Flappy Bird_ 網頁遊戲
   - **握球拍手勢**：開啟 _Ping Pong_ 網頁遊戲
     
     ![image](https://github.com/user-attachments/assets/41076220-01dc-49fe-9ba1-3da28f39f4de)


---

Enjoy playing Subway Surfers with your body movements! 🚀

## 遇到問題

- 用http無法開啟鏡頭
  解決方法：https://blog.csdn.net/qq_43530326/article/details/130974058 (也可查看## Usage)
- flappy bird 與subway 遊戲，如果架到server上，server無法控制我們自己的的鍵盤
  解決方法：自己寫一個flappy bird遊戲，
- 後端運算後再傳到前端會延遲
  解決方法：改在前端做運算

## 未來展望
- 我們的 flappy bird 運行速度會取決於CPU的效能，希望能改善
- 

## 分工表
| 組員 | 工作內容 | 
| :---: | :---: | 
| 吳楷賀 | 乒乓球 | 
| 陳子晴 | 水管鳥| 
| 廖志賢 | 地鐵跑酷 | 
| 楊立楚 | 用手勢或身體打指令| 
| 葉芷妤 | 伺服器設定、 |  

## 感謝名單
- BlueT
- 柏偉學長
- Josh學長
- Reg 學長
- Chat GPT :D))

## Reference
https://youtu.be/Z2EGhplFOHs?feature=shared

https://github.com/web-tunnel/lite-http-tunnel

https://blog.csdn.net/qq_43530326/article/details/130974058

https://www.youtube.com/watch?v=P_Mtzj-oLdk



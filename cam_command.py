import cv2
import mediapipe as mp
import math
import pyautogui
import webbrowser

# 初始化 MediaPipe 手部追蹤器
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# 門檻值
OK_THRESHOLD = 0.05  # OK 手勢的距離閾值
FIVE_THUMBINDEX = 0.15  # 食指和拇指間距的閾值
FIST_THRESHOLD = 0.07  # 握拳手勢的距離閾值

# 開啟攝影機
cap = cv2.VideoCapture(0)

def is_not_both_hands(hand_landmarks_list):
    return len(hand_landmarks_list) < 2

# 判斷 OK 手勢
def is_ok_gesture(thumb_tip, index_tip, other_fingers):
    thumb_index_distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    other_finger_distances = [
        math.sqrt((finger.x - thumb_tip.x)**2 + (finger.y - thumb_tip.y)**2)
        for finger in other_fingers
    ]
    return thumb_index_distance < OK_THRESHOLD and all(dist > 0.1 for dist in other_finger_distances)
    

# 判斷 握拳 手勢
def is_fist_gesture(hand_landmarks):
    wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    
    palm_center_x = (wrist.x + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x) / 2
    palm_center_y = (wrist.y + hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y) / 2
    palm_center = type('Point', (object,), {'x': palm_center_x, 'y': palm_center_y})

    # 判斷所有手指尖端是否靠近手掌中心
    finger_distances = [
        math.sqrt((thumb_tip.x - palm_center.x)**2 + (thumb_tip.y - palm_center.y)**2),
        math.sqrt((index_tip.x - palm_center.x)**2 + (index_tip.y - palm_center.y)**2),
        math.sqrt((middle_tip.x - palm_center.x)**2 + (middle_tip.y - palm_center.y)**2),
        math.sqrt((ring_tip.x - palm_center.x)**2 + (ring_tip.y - palm_center.y)**2),
        math.sqrt((pinky_tip.x - palm_center.x)**2 + (pinky_tip.y - palm_center.y)**2),
    ]

    # 判斷手指是否彎曲（全部指尖接近手掌中心）
    is_fist = all(distance < FIST_THRESHOLD for distance in finger_distances)

    # 檢測手背朝向攝像頭
    middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    hand_direction = middle_mcp.y < wrist.y  # MCP 在手腕上方表示手背向上

    return is_fist and hand_direction

# 計算兩個向量的內積
def dot_product(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

# 計算向量的模長
def magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2)


# 偵測拇指是否與其他四指垂直
def check_thumb_perpendicular(thumb_ip, thumb_tip, index_tip):
    # 計算拇指指根到指尖的向量
    thumb_to_tip = (thumb_tip.x - thumb_ip.x, thumb_tip.y - thumb_ip.y)
    # 計算拇指指根到食指指尖的向量
    thumb_to_index = (index_tip.x - thumb_ip.x, index_tip.y - thumb_ip.y)

    # 計算內積
    dot = dot_product(thumb_to_tip, thumb_to_index)
    # 計算兩個向量的模長
    dist_A = magnitude(thumb_to_tip)
    dist_B = magnitude(thumb_to_index)

    # 計算兩向量的夾角
    if dist_A == 0 or dist_B == 0:
        return False  # 防止除零錯誤
    angle = math.acos(dot / (dist_A * dist_B))

    # 判斷兩個向量是否垂直
    if 75 <= math.degrees(angle) <= 115: 
        return True
    return False


    
def is_bird_gesture(hand_landmarks_list):
    hand1 = hand_landmarks_list[0]
    hand2 = hand_landmarks_list[1]

    # 提取第一隻手的節點
    thumb_ip_1 = hand1.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_tip_1 = hand1.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip_1 = hand1.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # 提取第二隻手的節點
    thumb_ip_2 = hand2.landmark[mp_hands.HandLandmark.THUMB_IP]
    thumb_tip_2 = hand2.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip_2 = hand2.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    return (
        check_thumb_perpendicular(thumb_ip_1, thumb_tip_1, index_tip_1) and
        check_thumb_perpendicular(thumb_ip_2, thumb_tip_2, index_tip_2)
    )

# 初始化手部追蹤器
with mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.5) as hands:
    trigger_time = 0

    while True:
        # 讀取每一幀影像
        ret, frame = cap.read()
        if not ret:
            print("無法讀取影像，請確認攝影機是否開啟")
            break

        # 轉換顏色從 BGR 到 RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 偵測手部
        results = hands.process(rgb_frame)

        # 如果偵測到手部
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 畫出手部關節點和連線
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # 手部節點
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]  # 拇指尖端
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]  # 食指尖端
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]  # 中指尖端
                ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]  # 無名指尖端
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]  # 小指尖端

            if is_not_both_hands(results.multi_hand_landmarks):
                # 比 OK 觸發
                if is_ok_gesture(thumb_tip, index_tip, [middle_tip, ring_tip, pinky_tip]) and trigger_time < 1:
                    cv2.putText(frame, "Enter!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    trigger_time += 1
                    pyautogui.press("enter")  # 模擬按下 Enter 鍵
                    print("OK 手勢觸發：Enter")
                    continue

                # 比握拳觸發
                if is_fist_gesture(hand_landmarks) and trigger_time < 1:
                    cv2.putText(frame, "Ping pong!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    trigger_time += 1
                    url = "www.pingpong.leafish.xyz"  # 模擬輸入啟動指令
                    webbrowser.open(url)
                    print("Ping pong started!")
                    continue

            else:
                # 檢查是否符合雙手 "鳥" 手勢條件
                if is_bird_gesture(results.multi_hand_landmarks) and trigger_time < 1:
                    cv2.putText(frame, "Bird!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    trigger_time += 1
                    url = "www.flappybird.leafish.xyz"  # 模擬輸入啟動指令
                    webbrowser.open(url)
                    print("Flappy Bird started!")
                    continue

        else:
            trigger_time = 0  # 若未偵測到手部，重置觸發時間

        # 顯示攝影機畫面
        cv2.imshow("Hand Gesture Detection", frame)

        # 按 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 釋放攝影機並關閉視窗
cap.release()
cv2.destroyAllWindows()

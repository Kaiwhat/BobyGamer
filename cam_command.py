import cv2
import mediapipe as mp
import math
import pyautogui
import time

# 初始化 MediaPipe 手部追蹤器
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

OK_THRESHOLD = 0.05  # OK 手勢的距離閾值
SUDO_THRESHOLD = 0.2  # SUDO 手勢的距離閾值（食指和中指間距離）
FIVE_THRESHOLD = 0.05  # 5 手勢的間距閾值
FIVE_THUMBINDEX = 0.15  # 食指和拇指間距的閾值

# 拇指與四指垂直的閾值
PERPENDICULAR_THRESHOLD = 0.1  # 假設角度接近90度的閾值

# 開啟攝影機
cap = cv2.VideoCapture(0)

def is_both_hands(hand_landmarks_list):
    if len(hand_landmarks_list) < 2:
        return True
    
    return False

# 判斷 OK 手勢
def is_ok_gesture(thumb_tip, index_tip, other_fingers):
    thumb_index_distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    other_finger_distances = [
        math.sqrt((finger.x - thumb_tip.x)**2 + (finger.y - thumb_tip.y)**2)
        for finger in other_fingers
    ]
    return thumb_index_distance < OK_THRESHOLD and all(dist > 0.1 for dist in other_finger_distances)

# 判斷 SUDO 手勢
def is_sudo_gesture(thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip):
    thumb_pinky_distance = math.sqrt((thumb_tip.x - pinky_tip.x)**2 + (thumb_tip.y - pinky_tip.y)**2)
    index_middle_distance = math.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2)
    middle_ring_distance = math.sqrt((middle_tip.x - ring_tip.x)**2 + (middle_tip.y - ring_tip.y)**2)
    return thumb_pinky_distance > SUDO_THRESHOLD and index_middle_distance < 0.05 and middle_ring_distance < 0.05

# 判斷 5 手勢
def is_five_gesture(thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip):
    distances = [
        math.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2),
        math.sqrt((middle_tip.x - ring_tip.x)**2 + (middle_tip.y - ring_tip.y)**2),
        math.sqrt((ring_tip.x - pinky_tip.x)**2 + (ring_tip.y - pinky_tip.y)**2)
    ]
    THUM_DIST = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    return all(dist > FIVE_THRESHOLD for dist in distances) and THUM_DIST < FIVE_THUMBINDEX

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

                #手部節點
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]  # 拇指指根
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP] # 拇指尖端
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP] # 食指尖端
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP] # 中指尖端
                ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP] # 無名指尖端
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP] # 小指尖端
                
                # 比OK觸發
                if is_both_hands(results.multi_hand_landmarks):
                    if is_ok_gesture(thumb_tip, index_tip, [middle_tip, ring_tip, pinky_tip]) and trigger_time < 1:
                        cv2.putText(frame, "send command!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        trigger_time += 1
                        pyautogui.press("enter")  # 模擬按下 Enter 鍵
                        print("OK 手勢觸發：Enter")
                        continue
                    
                    # 比SUDO觸發
                    if is_sudo_gesture(thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip) and trigger_time < 1:
                        cv2.putText(frame, "SUDO！！！", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        trigger_time += 1
                        pyautogui.write("sudo ")  # 模擬輸入 "sudo"
                        print("SUDO 手勢觸發：sudo ")
                        continue

                    # 比5手勢觸發
                    if is_five_gesture(thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip) and trigger_time < 1:
                        cv2.putText(frame, "List items!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        trigger_time += 1
                        pyautogui.write("ls ")  # 模擬輸入 "ls"
                        print("ls typed")
                        continue

                else:
                    # 檢查是否符合雙手 "鳥" 手勢條件
                    if is_bird_gesture(results.multi_hand_landmarks) and trigger_time < 1:
                        cv2.putText(frame, "Bird!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        trigger_time += 1
                        pyautogui.write("flappy bird")  # 模擬輸入啟動指令
                        pyautogui.press("enter")
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

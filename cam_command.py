import cv2
import mediapipe as mp
import math
import pyautogui

# 初始化 MediaPipe 手部追蹤器
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

OK_THRESHOLD = 0.05  # OK 手勢的距離閾值
SUDO_THRESHOLD = 0.2  # SUDO 手勢的距離閾值（食指和中指間距離）
FIVE_THRESHOLD = 0.05  # 五手手勢的距離閾值
FIVE_THUMBINDEX = 0.05  # 拇指和食指之間的最大距離閾值

# 開啟攝影機
cap = cv2.VideoCapture(0)

def is_ok_gesture(thumb_tip, index_tip, other_fingers):
    thumb_index_distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    other_finger_distances = [
        math.sqrt((finger.x - thumb_tip.x)**2 + (finger.y - thumb_tip.y)**2)
        for finger in other_fingers
    ]
    return thumb_index_distance < OK_THRESHOLD and all(dist > 0.1 for dist in other_finger_distances)

def is_sudo_gesture(thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip):
    thumb_pinky_distance = math.sqrt((thumb_tip.x - pinky_tip.x)**2 + (thumb_tip.y - pinky_tip.y)**2)
    index_middle_distance = math.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2)
    middle_ring_distance = math.sqrt((middle_tip.x - ring_tip.x)**2 + (middle_tip.y - ring_tip.y)**2)
    return thumb_pinky_distance > SUDO_THRESHOLD and index_middle_distance < 0.05 and middle_ring_distance < 0.05

def is_five_gesture(thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip):
    # 計算各個手指間的距離
    distances = [
        math.sqrt((index_tip.x - middle_tip.x)**2 + (index_tip.y - middle_tip.y)**2),
        math.sqrt((middle_tip.x - ring_tip.x)**2 + (middle_tip.y - ring_tip.y)**2),
        math.sqrt((ring_tip.x - pinky_tip.x)**2 + (ring_tip.y - pinky_tip.y)**2)
    ]
    thumb_index_distance = math.sqrt((thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2)
    
    # 確保手指之間的距離符合五指伸展的條件
    return all(dist > FIVE_THRESHOLD for dist in distances) and thumb_index_distance > FIVE_THUMBINDEX

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
            # 假設只需要檢測第一隻手
            hand_landmarks_1 = results.multi_hand_landmarks[0]

            # 畫出手部關節點和連線
            mp_drawing.draw_landmarks(frame, hand_landmarks_1, mp_hands.HAND_CONNECTIONS)

            # 偵測 OK 手勢
            thumb_tip_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            other_fingers_1 = [hand_landmarks_1.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP], 
                               hand_landmarks_1.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                               hand_landmarks_1.landmark[mp_hands.HandLandmark.PINKY_TIP]]
            
            # 比OK觸發
            if is_ok_gesture(thumb_tip_1, index_tip_1, other_fingers_1) and trigger_time < 1:
                trigger_time += 1
                pyautogui.press("enter")  # 模擬按下 Enter 鍵
                print("OK 手勢觸發：Enter")
            
            # 偵測 SUDO 手勢
            thumb_tip_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip_1 = hand_landmarks_1.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # 比6觸發
            if is_sudo_gesture(thumb_tip_1, index_tip_1, middle_tip_1, ring_tip_1, pinky_tip_1) and trigger_time < 1:
                trigger_time += 1
                pyautogui.write("sudo ")  # 模擬輸入 "sudo"
                print("SUDO 手勢觸發：sudo ")

            # 比5觸發
            if is_five_gesture(thumb_tip_1, index_tip_1, middle_tip_1, ring_tip_1, pinky_tip_1) and trigger_time < 1:
                trigger_time += 1
                pyautogui.write("ls ")  # 模擬輸入 "5"
                print("ls typed")
            
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

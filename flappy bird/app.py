from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np
import base64
import socketio

app = Flask(__name__)
sio = socketio.Server()

# 初始化MediaPipe
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

# 儲存當前的跳躍狀態
jumping = {}

# 監聽WebSocket連接
@sio.event
def connect(sid, environ):
    print(f"User {sid} connected.")
    jumping[sid] = False

@sio.event
def disconnect(sid):
    print(f"User {sid} disconnected.")
    del jumping[sid]

@sio.event
def image(sid, img_data):
    global jumping
    # 解碼收到的影像數據
    img_data = base64.b64decode(img_data.split(',')[1])
    img = np.array(bytearray(img_data), dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)

    # 進行人體姿態偵測
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)

    line_y = 250  # 基準線位置
    cv2.line(img, (0, line_y), (img.shape[1], line_y), (0, 0, 255), 2)
    if result.pose_landmarks:
        # 畫出關鍵點
        mpDraw.draw_landmarks(
            img,
            result.pose_landmarks,
            mpPose.POSE_CONNECTIONS
        )

        # 取得左肩和右肩位置
        landmarks = result.pose_landmarks.landmark
        left_shoulder = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value]

        # 將肩膀位置轉換為像素座標
        left_shoulder_y = int(left_shoulder.y * img.shape[0])
        right_shoulder_y = int(right_shoulder.y * img.shape[0])

        # 判斷是否跳躍
        if left_shoulder_y < line_y and right_shoulder_y < line_y:
            cv2.putText(img, "Jump!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            jumping[sid] = True
        else:
            jumping[sid] = False

    # 回傳影像數據給前端
    _, buffer = cv2.imencode('.jpg', img)
    frame = buffer.tobytes()
    sio.emit('image', {'image': base64.b64encode(frame).decode()}, to=sid)

# 初始化Flask應用
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
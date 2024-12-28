import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
from flask import Flask, render_template, Response, request
import base64
import numpy as np

app = Flask(__name__)



def flappy_play():
    #開啟鏡頭
    cap = cv2.VideoCapture(0)

    keyboard = Controller()#鍵盤

    #初始化mediapipe 
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    # 點跟線的樣式
    poseLmsStyle = mpDraw.DrawingSpec(color=(255, 0, 0), thickness=5)
    poseConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=2)

    line_y =250 #線的位置
    jumping = False #使否跳過

    while True:
        ret, img = cap.read()
        img = cv2.flip(img, 1)#掀翻轉
        cv2.line(img, (0, line_y), (img.shape[1], line_y), (0, 0, 255), 2)
        if ret:
            # 轉換圖像為RGB
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 處理圖像以檢測身體節點
            result = pose.process(imgRGB)

            if result.pose_landmarks:
                mpDraw.draw_landmarks(
                    img,
                    result.pose_landmarks,
                    mpPose.POSE_CONNECTIONS,
                    poseLmsStyle,
                    poseConStyle
                )
            
                landmarks = result.pose_landmarks.landmark
                left_shoulder = landmarks[mpPose.PoseLandmark.LEFT_SHOULDER.value]
                right_shoulder = landmarks[mpPose.PoseLandmark.RIGHT_SHOULDER.value]

                #將節點轉為像素座標
                left_shoulder_y = int(left_shoulder.y * img.shape[0])
                right_shoulder_y = int(right_shoulder.y * img.shape[0])

                #如果超過設定的那條線，就偵測為jump
                if left_shoulder_y < line_y and right_shoulder_y < line_y:
                    cv2.putText(img, "Jump!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                    if jumping==False:
                        keyboard.press(Key.space)
                        keyboard.release(Key.space)
                        jumping=True
                else:
                    jumping=False
            
            

        _, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        #按下q退出
        if cv2.waitKey(1) == ord("q"):
            break

@app.route('/')
def flappy():
    return render_template('main.html')

@app.route('/video_feed')
def video_feed():

    return Response(flappy_play(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

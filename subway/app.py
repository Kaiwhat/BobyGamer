import cv2
import pyautogui
from time import time
from myPose import myPose
import webbrowser
from flask import Flask, render_template, Response

app = Flask(__name__)

class myGame():
    def __init__(self):
        self.pose = myPose()
        self.game_started = False
        self.x_pos_index = 1
        self.y_pos_index = 1
        self.counter = 0
        self.time1 = 0
        self.MID_Y = None
        self.num_of_frames = 10
        self.webpage_opened = False

    def move_LRC(self, LRC):
        if (LRC == 'Left' and self.x_pos_index != 0) or (
                LRC == 'Center' and self.x_pos_index == 2):
            pyautogui.press('left')
            self.x_pos_index -= 1
        elif (LRC == 'Right' and self.x_pos_index != 2) or (
                LRC == 'Center' and self.x_pos_index == 0):
            pyautogui.press('right')
            self.x_pos_index += 1
        return

    def move_JSD(self, JSD):
        if JSD == 'Jumping' and self.y_pos_index == 1:
            pyautogui.press('up')
            self.y_pos_index += 1
        elif JSD == 'Crouching' and self.y_pos_index == 1:
            pyautogui.press('down')
            self.y_pos_index -= 1
        elif JSD == 'Standing' and self.y_pos_index != 1:
            self.y_pos_index = 1
        return

    def play(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 960)

        while True:
            ret, image = cap.read()
            if not ret:
                print("Failed to capture image from camera")
                continue
            else:
                image = cv2.flip(image, 1)
                image_height, image_width, _ = image.shape
                image, results = self.pose.detectPose(image, self.pose.pose_video, draw=self.game_started)

                if results.pose_landmarks:
                    if self.game_started:
                        image, LRC = self.pose.checkPose_LRC(image, results, draw=True)
                        self.move_LRC(LRC)

                        if self.MID_Y:
                            image, JSD = self.pose.checkPose_JSD(image, results, self.MID_Y, draw=True)
                            self.move_JSD(JSD)

                        ret, buffer = cv2.imencode('.jpg', image)
                        frame = buffer.tobytes()
                        yield (b'--frame\r\n'
                               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                    else:
                        cv2.putText(image, 'JOIN BOTH HANDS TO START THE GAME.', (5, image_height - 10),
                                    cv2.FONT_HERSHEY_PLAIN,
                                    2, (0, 255, 0), 3)

                    if self.pose.checkHandsJoined(image, results)[1] == 'Hands Joined':
                        if not self.webpage_opened:
                            #webbrowser.open("https://poki.com/en/g/subway-surfers")
                            self.webpage_opened = True

                        self.counter += 1
                        if self.counter == self.num_of_frames:
                            if not self.game_started:
                                self.game_started = True
                                left_y = int(results.pose_landmarks.landmark[
                                                 self.pose.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height)
                                right_y = int(results.pose_landmarks.landmark[
                                                  self.pose.mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height)
                                self.MID_Y = abs(right_y + left_y) // 2
                                pyautogui.click(x=440, y=200, button='left')
                            else:
                                pyautogui.press('space')
                            self.counter = 0
                    else:
                        self.counter = 0
                else:
                    self.counter = 0

                time2 = time()
                if (time2 - self.time1) > 0:
                    frames_per_second = 1.0 / (time2 - self.time1)
                    cv2.putText(image, 'FPS: {}'.format(int(frames_per_second)), (10, 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (0, 255, 0), 3)
                self.time1 = time2

                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



# 初始化 myGame 類
my_game = myGame()

@app.route('/')
def home():
    return render_template('game.html')

@app.route('/video_feed')
def video_feed():
    """串流視頻處理後的影像"""
    return Response(my_game.play(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

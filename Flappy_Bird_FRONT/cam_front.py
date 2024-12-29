import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
from flask import Flask, render_template, Response, request,jsonify
import base64
import numpy as np
from flask_socketio import SocketIO

app = Flask(__name__)

@app.route('/')
def flappy():
    return render_template('cam_front.html') 

keyboard = Controller()

@app.route('/jump', methods=['POST'])
def jump():
    # 模拟按下空格键
    keyboard.press(Key.space)
    keyboard.release(Key.space)
    return "Jump simulated", 200

if __name__ == '__main__':
    #socketio.run(app, host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000)

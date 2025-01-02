import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js";
import Ball from "./ball.js";
import Player from "./player.js";

let startBtn = document.getElementById('startBtn');
startBtn.addEventListener('click', startGame);

let message = document.getElementById('message');

let canvas_l = document.getElementById('canvas_l');
let canvas_r = document.getElementById('canvas_r');
let ctx_l = canvas_l.getContext('2d');
let ctx_r = canvas_r.getContext('2d');

let player1;
let player2;
let ball;

let isGameStarted = false;
let playerNo = 0;
let roomID;

const socket = io("http://localhost:3000", {
    transports: ['websocket']
});

function startGame() {
    startBtn.style.display = 'none';

    if (socket.connected) {
        socket.emit('join');
        message.innerText = "Waiting for other player..."
    }
    else {
        message.innerText = "Refresh the page and try again..."
    }
}

socket.on("playerNo", (newPlayerNo) => {
    console.log(newPlayerNo);
    playerNo = newPlayerNo;
});

socket.on("startingGame", () => {
    isGameStarted = true;
    message.innerText = "We are going to start the game...";
});

socket.on("startedGame", (room) => {
    console.log(room);

    roomID = room.id;
    message.innerText = "";
    message.style.display = 'none';

    player1 = new Player(room.players[0].x, room.players[0].y, 60, 20, 'red');
    player2 = new Player(room.players[1].x, room.players[1].y, 60, 20, 'blue');

    player1.score = room.players[0].score;
    player2.score = room.players[1].score;


    ball = new Ball(room.ball.x, room.ball.y, 10, 'white');

    window.addEventListener('keydown', (e) => {
        if (isGameStarted) {
            if (e.keyCode === 37) {
                console.log("player move 1 left")
                socket.emit("move", {
                    roomID: roomID,
                    playerNo: playerNo,
                    direction: 'left'
                })
            } else if (e.keyCode === 39) {
                console.log("player move 1 right")
                socket.emit("move", {
                    roomID: roomID,
                    playerNo: playerNo,
                    direction: 'right'
                })
            }
        }
    });

    draw();
});

socket.on("updateGame", (room) => {
    player1.x = room.players[0].x;
    player2.x = room.players[1].x;

    player1.score = room.players[0].score;
    player2.score = room.players[1].score;

    ball.x = room.ball.x;
    ball.y = room.ball.y;

    if (playerNo==1){
        draw_l();
        canvas_r.style.display="none";
        document.getElementsByClassName("container")[0].style.flexDirection = "row";
    }
    if (playerNo==2){
        draw_r();
        canvas_l.style.display="none";
        document.getElementsByClassName("container")[0].style.flexDirection = "row";

    }
});

socket.on("endGame", (room) => {
    isGameStarted = false;
    socket.emit("leave", roomID);
});



function draw_l() {
    // player 1 view
    ctx_l.clearRect(0, 0, 450, 600);

    player1.draw_l(ctx_l);
    player2.draw_l(ctx_l);
    ball.draw_l(ctx_l);

    // center line
    ctx_l.strokeStyle = 'white';
    ctx_l.beginPath();
    ctx_l.setLineDash([10, 10])
    ctx_l.moveTo(5, 300);
    ctx_l.lineTo(450, 300);
    ctx_l.stroke();
}

function draw_r(){
    // player 2 view
    ctx_r.clearRect(0, 0, 450, 600);

    player1.draw_r(ctx_r);
    player2.draw_r(ctx_r);
    ball.draw_r(ctx_r);

    // center line
    ctx_r.strokeStyle = 'white';
    ctx_r.beginPath();
    ctx_r.setLineDash([10, 10])
    ctx_r.moveTo(5, 300);
    ctx_r.lineTo(450, 300);
    ctx_r.stroke();
}

//import { POSE_CONNECTIONS } from '@mediapipe/pose';//新增
//初始化 Video 和 Canvas 元素
const videoElement = document.getElementById('video');
const canvasElement = document.getElementById('canvas_v');
const canvasCtx = canvasElement.getContext('2d');

//初始化 MediaPipe 模組
const pose = new Pose({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
});

pose.setOptions({
    modelComplexity: 1,
    smoothLandmarks: true,
    enableSegmentation: false,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});

//監聽結果
pose.onResults((results) => {
//清空Canvas
canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

//鏡像
canvasCtx.save();
canvasCtx.scale(-1, 1);
canvasCtx.translate(-canvasElement.width, 0);

//畫在圖片上
canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

//畫出跳躍基準線
const lineY = 75;
const lineX = 50;
const lineX2 = 250;//300為畫面長度
canvasCtx.beginPath();
canvasCtx.moveTo(lineX, 0);
canvasCtx.lineTo(lineX, canvasElement.height);
canvasCtx.moveTo(lineX2, 0);
canvasCtx.lineTo(lineX2, canvasElement.height);
canvasCtx.strokeStyle = '#0000FF';
canvasCtx.lineWidth = 2;
canvasCtx.stroke();

//畫出點跟線
if (results.poseLandmarks) {
    drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, {
    color: '#00FF00',
    lineWidth: 2,
    });
    drawLandmarks(canvasCtx, results.poseLandmarks, {
    color: '#FF0000',
    lineWidth: 2,
    radius: 2,
    });

    //左右手的節點
    const leftHand = results.poseLandmarks[19];
    const rightHand = results.poseLandmarks[20];

    //將y座標轉為像素
    const leftX = leftHand.x * canvasElement.width;
    const rightX = rightHand.x * canvasElement.width;
    
    //如果左手或右手超過左邊的線
    if (leftX>lineX2 || rightX>lineX2){
        canvasCtx.fillStyle = 'green';
        canvasCtx.font = '24px Arial';
        canvasCtx.fillText('LEFT!', 250, 50);
        press_left(); //按下向左鍵
    }
    //如果右手超過右邊的線
    if (rightX<lineX || leftX<lineX){
        canvasCtx.fillStyle = 'green';
        canvasCtx.font = '24px Arial';
        canvasCtx.fillText('RIGHT!', 50, 50);
        press_right(); //按下向右鍵
    }
}

canvasCtx.restore();
});

//left key
function press_left() {
    const event = new KeyboardEvent('keydown', {
        key: 'ArrowLeft',
        keyCode: 37,  // 空白鍵的鍵值
        code: 'ArrowLeft',
        bubbles: true,
    });
    document.dispatchEvent(event);
}

//right key
function press_right() {
    const event = new KeyboardEvent('keydown', {
        key: 'ArrowRight',
        keyCode: 39,  // 空白鍵的鍵值
        code: 'ArrowRight',
        bubbles: true,
    });
    document.dispatchEvent(event);
}

// 啟動攝影機
const camera = new Camera(videoElement, {
onFrame: async () => {
    await pose.send({ image: videoElement });
},
width: 640,
height: 480,
});
camera.start();


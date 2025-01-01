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

    draw();
});

socket.on("endGame", (room) => {
    isGameStarted = false;
    socket.emit("leave", roomID);
});



function draw() {
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
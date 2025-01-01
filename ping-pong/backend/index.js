const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
const cors = require('cors');
const { futimesSync } = require('fs');

app.use(cors({
    origin: '*'
}));

app.get('/', (req, res) => {
    res.send('<h1>PING PONG SERVER -- </h1>');
});

let rooms = [];

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on("join", () => {
        console.log(rooms);

        // get room 
        let room;
        if (rooms.length > 0 && rooms[rooms.length - 1].players.length === 1) {
            room = rooms[rooms.length - 1];
        }

        if (room) {
            socket.join(room.id);
            socket.emit('playerNo', 2);

            // add player to room
            room.players.push({
                socketID: socket.id,
                playerNo: 2,
                score: 0,
                x: 210,
                y: 30,
            });

            // send message to room
            io.to(room.id).emit('startingGame');

            setTimeout(() => {
                io.to(room.id).emit('startedGame', room);

                // start game
                startGame(room);
            }, 3000);
        }
        else {
            room = {
                id: rooms.length + 1,
                players: [{
                    socketID: socket.id,
                    playerNo: 1,
                    score: 0,
                    x: 210,
                    y: 550,
                }],
                ball: {
                    x: 210,
                    y: 300,
                    dx: 1,
                    dy: 1,
                },
                winner: 0,
            }
            rooms.push(room);
            socket.join(room.id);
            socket.emit('playerNo', 1);
        }
    });

    socket.on("move", (data) => {
        let room = rooms.find(room => room.id === data.roomID);

        if (room) {
            if (data.direction === 'left') {
                if (data.playerNo == 2) room.players[data.playerNo - 1].x += 10;
                else room.players[data.playerNo - 1].x -= 10;
            }
            else if (data.direction === 'right') {
                if (data.playerNo == 2) room.players[data.playerNo - 1].x -= 10;
                else room.players[data.playerNo - 1].x += 10;
            }
            if (room.players[data.playerNo - 1].x > 390) {
                room.players[data.playerNo - 1].x = 390;
            }
            if (room.players[data.playerNo - 1].x < 0) {
                room.players[data.playerNo - 1].x = 0;
            }
        }

        // update rooms
        rooms = rooms.map(r => {
            if (r.id === room.id) {
                return room;
            }
            else {
                return r;
            }
        });

        io.to(room.id).emit('updateGame', room);
    });

    socket.on("leave", (roomID) => {
        socket.leave(roomID);
    });



    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

function startGame(room) {
    let interval = setInterval(() => {
        room.ball.y += room.ball.dy * 2;
        room.ball.x += room.ball.dx * 2;

        // check if ball hits player 1
        if (room.ball.y == 550 && room.ball.x > room.players[0].x && room.ball.x < room.players[0].x + 60) {
            room.ball.dx *= 1;
            room.ball.dy *= -1;
        }

        // check if ball hits player 2
        if (room.ball.y == 50 && room.ball.x > room.players[1].x && room.ball.x < room.players[1].x + 60) {
            room.ball.dx *= 1;
            room.ball.dy *= -1;
        }

        // left and right walls
        if (room.ball.x < 5 || room.ball.x > 450) {
            room.ball.dx *= -1;
        }


        // up and down walls
        if (room.ball.y < 5) {
            room.players[0].score += 1;
            room.ball.y = 300;
            room.ball.x = 210;
            room.ball.dx *= 1;
            room.ball.dy *= 1;
        }

        if (room.ball.y > 595) {
            room.players[1].score += 1;
            room.ball.y = 300;
            room.ball.x = 210;
            room.ball.dx *= 1;
            room.ball.dy *= 1;
        }


        if (room.players[0].score === 10) {
            room.winner = 1;
            rooms = rooms.filter(r => r.id !== room.id);
            io.to(room.id).emit('endGame', room);
            clearInterval(interval);
        }

        if (room.players[1].score === 10) {
            room.winner = 2;
            rooms = rooms.filter(r => r.id !== room.id);
            io.to(room.id).emit('endGame', room);
            clearInterval(interval);
        }

        io.to(room.id).emit('updateGame', room);
    }, 1000 / 60);
}



server.listen(3000, () => {
    console.log('listening on *:3000');
});
// 畫布與繪圖相關設定
let board, context;
const boardWidth = 580; // 原本 360
const boardHeight = 640;

// 小鳥相關參數
const birdWidth = 34;
const birdHeight = 24;
const birdX = boardWidth / 8;
const birdY = boardHeight / 2;
let bird = {
  x: birdX,
  y: birdY,
  width: birdWidth,
  height: birdHeight
};

let birdImg;
// 物理參數（單位：像素/秒 或 像素/秒²）
let velocityY = 0;
const gravity = 400; // 重力加速度

// 管道參數
let pipeArray = [];
const pipeWidth = 64;
const pipeHeight = 512;
const pipeX = boardWidth;
const pipeY = 0;
const velocityX = -100; // 管道水平移動速度

// 管道圖片（全域變數）
let topPipeImg, bottomPipeImg;

// 遊戲狀態與計分
let gameOver = false; // 遊戲失敗時才改為 true
let gameStarted = false; // 控制是否已正式開始
let score = 0;
let max_score = parseInt(window.max_score_backend) || 0;

// 時間控制變數（以 delta time 更新物理運算）
let lastTime = performance.now();
let pipeTimer = 0;
const pipeInterval = 3; // 每2.5秒產生一組管道

// 初始化遊戲畫布與圖片資源
window.addEventListener("load", () => {
  board = document.getElementById("board");
  board.width = boardWidth;
  board.height = boardHeight;
  context = board.getContext("2d");
  
  // 載入小鳥圖片
  birdImg = new Image();
  birdImg.src = "img/flappybird.png";
  birdImg.onload = () => {
    // 初始狀態只畫一次小鳥
    context.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);
  };

  // 載入管道圖片
  topPipeImg = new Image();
  topPipeImg.src = "img/toppipe.png";
  bottomPipeImg = new Image();
  bottomPipeImg.src = "img/bottompipe.png";

  // 監聽鍵盤事件（空白鍵控制跳躍）
  document.addEventListener("keydown", moveBird);

  // 初始不啟動 update 物理運算，僅持續渲染初始狀態
  requestAnimationFrame(update);
});

function update(currentTime) {
  // 若遊戲尚未開始，僅顯示靜態初始畫面
  if (!gameStarted) {
    context.clearRect(0, 0, boardWidth, boardHeight);
    context.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);
    requestAnimationFrame(update);
    return;
  }

  // 遊戲正式進行後，若遊戲結束則顯示 GAME OVER
  if (gameOver) {
    drawGameOver();
    return;
  }
  
  // 計算與上一幀的時間差（秒）
  const deltaTime = (currentTime - lastTime) / 1000;
  lastTime = currentTime;
  
  // 清除畫布
  context.clearRect(0, 0, boardWidth, boardHeight);
  
  // 更新小鳥物理：重力影響速度並更新位置
  velocityY += gravity * deltaTime;
  bird.y += velocityY * deltaTime;
  bird.y = Math.max(bird.y, 0);
  context.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);
  
  // 累計管道生成時間，達到間隔則生成新管道
  pipeTimer += deltaTime;
  if (pipeTimer >= pipeInterval) {
    placePipes();
    pipeTimer -= pipeInterval;
  }
  
  // 更新管道位置與檢查碰撞
  for (let i = 0; i < pipeArray.length; i++) {
    let pipe = pipeArray[i];
    pipe.x += velocityX * deltaTime;
    context.drawImage(pipe.img, pipe.x, pipe.y, pipe.width, pipe.height);
    
    // 當小鳥通過管道，累計分數 (每組管道上下各計 0.5 分)
    if (!pipe.passed && bird.x > pipe.x + pipe.width) {
      score += 0.5;
      pipe.passed = true;
    }
    
    // 檢查碰撞
    if (detectCollision(bird, pipe)) {
      if (max_score < score) {
        max_score = score;
        reloadMaxScore(max_score);
        document.getElementById("max_score_input_button").style.display = "block";
      }
      gameOver = true;
    }
  }
  
  // 移除超出畫布的管道
  while (pipeArray.length > 0 && pipeArray[0].x < -pipeWidth) {
    pipeArray.shift();
  }
  
  // 若小鳥掉出畫布下方，結束遊戲
  if (bird.y > boardHeight) {
    if (max_score < score) {
      max_score = score;
      reloadMaxScore(max_score);
      document.getElementById("max_score_input_button").style.display = "block";
    }
    gameOver = true;
  }
  
  // 畫出分數
  context.fillStyle = "white";
  context.font = "45px sans-serif";
  context.fillText(Math.floor(score), 5, 45);
  
  requestAnimationFrame(update);
}

// 生成一組上下管道
function placePipes() {
  const randomPipeY = pipeY - pipeHeight / 4 - Math.random() * (pipeHeight / 2);
  const openingSpace = boardHeight / 4;
  
  const topPipe = {
    img: topPipeImg,
    x: pipeX,
    y: randomPipeY,
    width: pipeWidth,
    height: pipeHeight,
    passed: false
  };
  pipeArray.push(topPipe);
  
  const bottomPipe = {
    img: bottomPipeImg,
    x: pipeX,
    y: randomPipeY + pipeHeight + openingSpace,
    width: pipeWidth,
    height: pipeHeight,
    passed: false
  };
  pipeArray.push(bottomPipe);
}

// 軸對齊包圍盒碰撞檢測
function detectCollision(a, b) {
  return a.x < b.x + b.width &&
         a.x + a.width > b.x &&
         a.y < b.y + b.height &&
         a.y + a.height > b.y;
}

// 鍵盤事件：空白鍵控制小鳥跳躍；若遊戲未開始則啟動遊戲，若遊戲結束則重啟
function moveBird(e) {
  if (e.code === "Space") {
    if (!gameStarted) {
      // 第一次跳躍，啟動遊戲
      gameStarted = true;
      velocityY = -200;
    } else if (gameOver) {
      // 若遊戲結束則重置遊戲狀態並跳躍
      bird.y = birdY;
      score = 0;
      velocityY = -200;
      pipeArray = [];
      gameOver = false;
      document.getElementById("max_score_input_button").style.display = "none";
      lastTime = performance.now();
      pipeTimer = 0;
      requestAnimationFrame(update);
    } else {
      // 遊戲進行中，執行跳躍
      velocityY = -200;
    }
  }
}

// 傳送最高分給後端
async function reloadMaxScore(maxScore) {
  await fetch("/reload_max_score", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ re_max: maxScore })
  });
}

// 遊戲結束時顯示文字
function drawGameOver() {
  context.fillStyle = "white";
  context.font = "45px sans-serif";
  context.fillText("GAME OVER", 5, 90);
}

  const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const player = { x: 230, y: 550, width: 30, height: 20, color: "cyan" };
let bullets = [];
let enemies = [];
let enemyBullets = [];
let keys = {};
let score = 0;
let gameOver = false;

// 키 입력 처리
document.addEventListener("keydown", (e) => (keys[e.code] = true));
document.addEventListener("keyup", (e) => (keys[e.code] = false));

// 초기 적 편대 생성
function createEnemies() {
  enemies = [];
  for (let row = 0; row < 4; row++) {
    for (let col = 0; col < 8; col++) {
      enemies.push({
        x: 60 + col * 50,
        y: 50 + row * 40,
        width: 30,
        height: 20,
        color: ["red", "orange", "yellow", "lime"][row],
        dx: 1,
      });
    }
  }
}
createEnemies();

// 플레이어 총알 발사
function shoot() {
  if (!player.shooting) {
    bullets.push({ x: player.x + 13, y: player.y, width: 4, height: 10, color: "white" });
    player.shooting = true;
    setTimeout(() => (player.shooting = false), 200);
  }
}

// 적 총알 발사
function enemyShoot(enemy) {
  enemyBullets.push({
    x: enemy.x + enemy.width / 2 - 2,
    y: enemy.y + enemy.height,
    width: 4,
    height: 10,
    color: "red",
    dy: 4,
  });
}

// 게임 루프
function update() {
  if (gameOver) {
    ctx.fillStyle = "white";
    ctx.font = "36px Arial";
    ctx.fillText("GAME OVER", 150, 300);
    ctx.font = "20px Arial";
    ctx.fillText("Press R to Restart", 170, 340);
    return;
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 플레이어 이동
  if (keys["ArrowLeft"] && player.x > 0) player.x -= 5;
  if (keys["ArrowRight"] && player.x < canvas.width - player.width) player.x += 5;
  if (keys["Space"]) shoot();
  if (keys["KeyR"]) restart();

  // 총알 이동
  for (let b of bullets) {
    b.y -= 8;
    ctx.fillStyle = b.color;
    ctx.fillRect(b.x, b.y, b.width, b.height);
  }
  bullets = bullets.filter((b) => b.y > 0);

  // 적 이동 (좌우 왕복)
  let edge = false;
  for (let e of enemies) {
    e.x += e.dx;
    if (e.x < 20 || e.x + e.width > canvas.width - 20) edge = true;
  }
  if (edge) {
    for (let e of enemies) {
      e.dx *= -1;
      e.y += 15;
    }
  }

  // 적 렌더링 및 랜덤 발사
  for (let e of enemies) {
    ctx.fillStyle = e.color;
    ctx.fillRect(e.x, e.y, e.width, e.height);
    if (Math.random() < 0.002) enemyShoot(e);
  }

  // 적 총알 이동
  for (let eb of enemyBullets) {
    eb.y += eb.dy;
    ctx.fillStyle = eb.color;
    ctx.fillRect(eb.x, eb.y, eb.width, eb.height);
  }
  enemyBullets = enemyBullets.filter((b) => b.y < canvas.height);

  // 충돌 감지 (플레이어 총알 vs 적)
  for (let b of bullets) {
    for (let e of enemies) {
      if (
        b.x < e.x + e.width &&
        b.x + b.width > e.x &&
        b.y < e.y + e.height &&
        b.y + b.height > e.y
      ) {
        e.hit = true;
        b.hit = true;
        score += 10;
      }
    }
  }
  enemies = enemies.filter((e) => !e.hit);
  bullets = bullets.filter((b) => !b.hit);

  // 충돌 감지 (적 총알 vs 플레이어)
  for (let eb of enemyBullets) {
    if (
      eb.x < player.x + player.width &&
      eb.x + eb.width > player.x &&
      eb.y < player.y + player.height
    ) {
      gameOver = true;
    }
  }

  // 플레이어 그리기
  ctx.fillStyle = player.color;
  ctx.fillRect(player.x, player.y, player.width, player.height);

  // 점수 표시
  ctx.fillStyle = "white";
  ctx.font = "16px Arial";
  ctx.fillText("Score: " + score, 10, 20);

  // 모든 적 제거 시 재생성
  if (enemies.length === 0) createEnemies();

  requestAnimationFrame(update);
}

// 재시작
function restart() {
  enemies = [];
  bullets = [];
  enemyBullets = [];
  score = 0;
  gameOver = false;
  player.x = 230;
  createEnemies();
}

update();

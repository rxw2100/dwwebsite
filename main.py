import pygame
import random
import sys

# 초기화
pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Python Galaga Clone")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)

# 플레이어 클래스
class Player:
    def __init__(self):
        self.width, self.height = 40, 25
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 60
        self.speed = 6
        self.color = CYAN
        self.bullets = []

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed

    def shoot(self):
        if len(self.bullets) < 4:  # 최대 4발 제한
            self.bullets.append(Bullet(self.x + self.width // 2 - 2, self.y))

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        for bullet in self.bullets:
            bullet.update()
            bullet.draw()

# 총알 클래스
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.color = YELLOW
        self.speed = 8

    def update(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# 적 클래스
class Enemy:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 20
        self.color = color
        self.dx = 2
        self.dy = 0
        self.alive = True

    def update(self):
        self.x += self.dx
        if self.x <= 0 or self.x + self.width >= WIDTH:
            self.dx *= -1
            self.y += 20

    def draw(self):
        if self.alive:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# 적 편대 생성
def create_enemies():
    enemies = []
    colors = [RED, (255, 165, 0), YELLOW, GREEN]
    for row in range(4):
        for col in range(8):
            enemies.append(Enemy(50 + col * 50, 50 + row * 40, colors[row]))
    return enemies

# 메인 게임 함수
def main():
    player = Player()
    enemies = create_enemies()
    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(60)
        screen.fill(BLACK)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()

        # 게임 로직
        if not game_over:
            player.move(keys)

            # 총알 이동
            for bullet in player.bullets[:]:
                bullet.update()
                if bullet.y < 0:
                    player.bullets.remove(bullet)

            # 적 이동 및 충돌 체크
            for enemy in enemies[:]:
                enemy.update()
                for bullet in player.bullets[:]:
                    if (bullet.x < enemy.x + enemy.width and
                        bullet.x + bullet.width > enemy.x and
                        bullet.y < enemy.y + enemy.height and
                        bullet.y + bullet.height > enemy.y):
                        enemies.remove(enemy)
                        player.bullets.remove(bullet)
                        score += 10
                        break
                if enemy.y + enemy.height >= player.y:
                    game_over = True

            # 모든 적 제거 시 재생성
            if not enemies:
                enemies = create_enemies()

            # 그리기
            player.draw()
            for enemy in enemies:
                enemy.draw()

            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        else:
            game_over_text = font.render("GAME OVER! Press R to Restart", True, WHITE)
            screen.blit(game_over_text, (120, HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__":
    main()

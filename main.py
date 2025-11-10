import pygame, sys, random

pygame.init()

# 화면 설정
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Python Galaga")

# 기본 설정
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
BLACK, WHITE = (0,0,0), (255,255,255)

# 플레이어
player = pygame.Rect(WIDTH//2-20, HEIGHT-60, 40, 25)
player_speed = 6
bullets = []
enemies = []
score = 0
game_over = False

# 적 생성
def create_enemies():
    colors = [(255,0,0), (255,165,0), (255,255,0), (0,255,0)]
    e = []
    for row in range(4):
        for col in range(8):
            e.append(pygame.Rect(50+col*50, 50+row*40, 30, 20))
    return e

enemies = create_enemies()

# 게임 루프
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(pygame.Rect(player.x+18, player.y, 4, 10))
            if game_over and event.key == pygame.K_r:
                enemies = create_enemies()
                bullets.clear()
                score = 0
                game_over = False

    if not game_over:
        # 이동
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH-player.width:
            player.x += player_speed

        # 총알 이동
        for b in bullets[:]:
            b.y -= 8
            if b.y < 0:
                bullets.remove(b)

        # 적 이동
        for e in enemies[:]:
            e.y += 0.3
            # 충돌 확인
            for b in bullets[:]:
                if e.colliderect(b):
                    if e in enemies:
                        enemies.remove(e)
                    bullets.remove(b)
                    score += 10

            if e.y > HEIGHT - 60:
                game_over = True

        # 그리기
        pygame.draw.rect(screen, (0,255,255), player)
        for b in bullets:
            pygame.draw.rect(screen, (255,255,0), b)
        for e in enemies:
            pygame.draw.rect(screen, (255,0,0), e)

        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))
    else:
        msg = font.render("GAME OVER! Press R to restart", True, WHITE)
        screen.blit(msg, (100, HEIGHT//2))

    pygame.display.flip()

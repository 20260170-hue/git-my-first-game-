import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bullet Dodge Game")

WHITE = (255, 255, 255)

clock = pygame.time.Clock()
running = True

# 🔵 플레이어
x = 400
y = 300
radius = 50
color = (0, 0, 255)

# 🔤 폰트
font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 60)

prev_keys = pygame.key.get_pressed()

# 🔶 탄막
bullets = []

# 🎯 점수 & 난이도
score = 0
start_time = pygame.time.get_ticks()
spawn_rate = 0.02  # 초기 생성 확률
bullet_speed = 5

# 💀 게임 상태
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # ⏱️ 시간 기반 점수
        current_time = pygame.time.get_ticks()
        score = (current_time - start_time) // 1000  # 초 단위 점수

        # 🔥 난이도 증가
        spawn_rate = 0.02 + score * 0.002
        bullet_speed = 5 + score * 0.2

        # 🚀 속도
        speed = 10
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            speed = 20

        # 🎨 색 변경
        if keys[pygame.K_LEFT] and not prev_keys[pygame.K_LEFT]:
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if keys[pygame.K_RIGHT] and not prev_keys[pygame.K_RIGHT]:
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if keys[pygame.K_UP] and not prev_keys[pygame.K_UP]:
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if keys[pygame.K_DOWN] and not prev_keys[pygame.K_DOWN]:
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

        # 🚀 이동
        if keys[pygame.K_LEFT]:
            x -= speed
        if keys[pygame.K_RIGHT]:
            x += speed
        if keys[pygame.K_UP]:
            y -= speed
        if keys[pygame.K_DOWN]:
            y += speed

        # 🚧 화면 제한
        if x - radius < 0:
            x = radius
        if x + radius > 800:
            x = 800 - radius
        if y - radius < 0:
            y = radius
        if y + radius > 600:
            y = 600 - radius

        # 🔶 탄막 생성 (난이도 반영)
        if random.random() < spawn_rate:
            bullet_x = random.randint(0, 780)
            bullets.append([bullet_x, 0])

        # 🔶 탄막 이동 (속도 증가)
        for bullet in bullets:
            bullet[1] += bullet_speed

        # 🔶 화면 밖 제거
        bullets = [b for b in bullets if b[1] < 600]

        # 💥 충돌 체크
        player_rect = pygame.Rect(x - radius, y - radius, radius*2, radius*2)

        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 20, 20)
            if player_rect.colliderect(bullet_rect):
                game_over = True

    # 🎨 화면 그리기
    screen.fill(WHITE)

    # 🔵 플레이어
    pygame.draw.circle(screen, color, (x, y), radius)

    # 🔶 탄막
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], 20, 20))

    # 📊 FPS
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))

    # 🎯 점수 표시
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 40))

    # 💀 게임오버 화면
    if game_over:
        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (250, 250))

    pygame.display.flip()
    clock.tick(60)

    prev_keys = keys

pygame.quit()
sys.exit()
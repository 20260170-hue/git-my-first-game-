import pygame
import sys
import random
import time

pygame.init()

# 화면 설정
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bullet Survival Game")

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 글꼴
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
game_over_font = pygame.font.SysFont(None, 60)

# 플레이어 원 설정
initial_x = SCREEN_WIDTH // 2
initial_y = SCREEN_HEIGHT // 2
x = initial_x
y = initial_y
radius = 50
speed = 10
color = BLUE

# 탄막 설정
bullets = []  # [x, y, dx, dy, color]
bullet_speed = 3
bullet_size = 30
base_spawn_prob = 0.02  # 기본 탄막 출현 확률

# 방향키 색 변경 처리
color_changed = False

# 점수
score = 0
start_ticks = pygame.time.get_ticks()  # 게임 시작 시간

# 게임 상태
running = True
game_over = False

while running:
    shift_pressed = False
    moved = False  # 방향키 누름 체크

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Shift 키 확인
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        shift_pressed = True

    move_speed = speed * 2 if shift_pressed else speed

    if not game_over:
        # 방향키 이동
        if keys[pygame.K_LEFT]:
            x -= move_speed
            moved = True
        if keys[pygame.K_RIGHT]:
            x += move_speed
            moved = True
        if keys[pygame.K_UP]:
            y -= move_speed
            moved = True
        if keys[pygame.K_DOWN]:
            y += move_speed
            moved = True

        # 한 번만 색 변경
        if moved and not color_changed:
            color = (random.randint(0, 255),
                     random.randint(0, 255),
                     random.randint(0, 255))
            color_changed = True
        if not moved:
            color_changed = False

        # 화면 밖으로 나가지 않게 제한
        if x < radius:
            x = radius
        if x > SCREEN_WIDTH - radius:
            x = SCREEN_WIDTH - radius
        if y < radius:
            y = radius
        if y > SCREEN_HEIGHT - radius:
            y = SCREEN_HEIGHT - radius

        # 🔹 난이도 상승: 시간이 지날수록 탄막 출현 확률 증가
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        spawn_prob = base_spawn_prob + 0.0005 * elapsed_seconds  # 점점 증가

        # 🔹 탄막 생성 (모든 방향)
        if random.random() < spawn_prob:
            side = random.choice(["top", "bottom", "left", "right"])
            if side == "top":
                bx = random.randint(bullet_size, SCREEN_WIDTH - bullet_size)
                by = -bullet_size
                dx, dy = 0, bullet_speed
            elif side == "bottom":
                bx = random.randint(bullet_size, SCREEN_WIDTH - bullet_size)
                by = SCREEN_HEIGHT + bullet_size
                dx, dy = 0, -bullet_speed
            elif side == "left":
                bx = -bullet_size
                by = random.randint(bullet_size, SCREEN_HEIGHT - bullet_size)
                dx, dy = bullet_speed, 0
            else:  # right
                bx = SCREEN_WIDTH + bullet_size
                by = random.randint(bullet_size, SCREEN_HEIGHT - bullet_size)
                dx, dy = -bullet_speed, 0
            bullets.append([bx, by, dx, dy, RED])

        # 화면 채우기
        screen.fill(WHITE)

        # 플레이어 원 그리기
        pygame.draw.circle(screen, color, (x, y), radius)

        # 탄막 이동 및 충돌 처리
        new_bullets = []
        for bullet in bullets:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            rect = pygame.Rect(bullet[0]-bullet_size//2, bullet[1]-bullet_size//2,
                               bullet_size, bullet_size)
            pygame.draw.rect(screen, bullet[4], rect)

            # 충돌 감지
            dist_x = abs(x - rect.centerx)
            dist_y = abs(y - rect.centery)
            if dist_x < radius + bullet_size/2 and dist_y < radius + bullet_size/2:
                game_over = True  # 충돌 시 게임 오버
            else:
                # 화면 밖이 아니면 유지
                if -bullet_size <= bullet[0] <= SCREEN_WIDTH + bullet_size and -bullet_size <= bullet[1] <= SCREEN_HEIGHT + bullet_size:
                    new_bullets.append(bullet)
        bullets = new_bullets

        # 🔹 점수 증가 (원 오래 버틸수록)
        score = int(elapsed_seconds * 10)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 40))

    else:
        # 게임 오버 화면
        screen.fill(WHITE)
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 - 50))
        score_text = font.render(f"Final Score: {score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 + 20))
        restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 + 60))

        # 게임 오버 상태에서 키 입력 처리
        if keys[pygame.K_r]:
            # 초기화
            x, y = initial_x, initial_y
            bullets.clear()
            score = 0
            start_ticks = pygame.time.get_ticks()
            game_over = False
        if keys[pygame.K_q]:
            running = False

    # FPS 표시
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, BLACK)
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exi
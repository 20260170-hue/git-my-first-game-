import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Collision: Circle / AABB / OBB (SAT)")

# 색상
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)
BLACK = (0, 0, 0)

# 폰트
font = pygame.font.SysFont(None, 36)

# 플레이어
player_x, player_y = 100, 100
size = 100
speed = 5

# 고정 오브젝트 (회전)
fixed_x, fixed_y = 400, 300
angle = 0
rotation_speed = 1

clock = pygame.time.Clock()

# OBB 꼭짓점 계산
def get_rotated_corners(cx, cy, w, h, angle):
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    hw, hh = w / 2, h / 2

    corners = [
        (-hw, -hh), (hw, -hh),
        (hw, hh), (-hw, hh)
    ]

    rotated = []
    for x, y in corners:
        rx = x * cos_a - y * sin_a + cx
        ry = x * sin_a + y * cos_a + cy
        rotated.append((rx, ry))
    return rotated

# SAT 충돌
def project(axis, points):
    dots = [p[0]*axis[0] + p[1]*axis[1] for p in points]
    return min(dots), max(dots)

def normalize(v):
    length = math.sqrt(v[0]**2 + v[1]**2)
    return (v[0]/length, v[1]/length)

def sat_collision(poly1, poly2):
    edges = []

    for poly in (poly1, poly2):
        for i in range(len(poly)):
            p1 = poly[i]
            p2 = poly[(i+1)%len(poly)]
            edge = (p2[0]-p1[0], p2[1]-p1[1])
            axis = (-edge[1], edge[0])
            axis = normalize(axis)
            edges.append(axis)

    for axis in edges:
        min1, max1 = project(axis, poly1)
        min2, max2 = project(axis, poly2)

        if max1 < min2 or max2 < min1:
            return False
    return True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 입력
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_RIGHT]:
        player_x += speed
    if keys[pygame.K_UP]:
        player_y -= speed
    if keys[pygame.K_DOWN]:
        player_y += speed

    if keys[pygame.K_z]:
        rotation_speed += 0.05

    angle += rotation_speed

    # 플레이어
    player_rect = pygame.Rect(player_x, player_y, size, size)
    player_center = player_rect.center

    # 고정 오브젝트
    fixed_center = (fixed_x, fixed_y)
    fixed_corners = get_rotated_corners(fixed_x, fixed_y, size, size, angle)

    # 🔴 AABB (고정 크기!)
    fixed_aabb = pygame.Rect(
        fixed_x - size // 2,
        fixed_y - size // 2,
        size,
        size
    )
    aabb_collision = player_rect.colliderect(fixed_aabb)

    # 🔵 Circle
    player_radius = size // 2
    fixed_radius = size // 2

    dx = player_center[0] - fixed_center[0]
    dy = player_center[1] - fixed_center[1]
    distance = math.sqrt(dx**2 + dy**2)

    circle_collision = distance < (player_radius + fixed_radius)

    # 🟢 OBB (SAT)
    player_corners = [
        player_rect.topleft,
        player_rect.topright,
        player_rect.bottomright,
        player_rect.bottomleft
    ]

    obb_collision = sat_collision(player_corners, fixed_corners)

    # 🎨 배경 (노란색으로 변경)
    any_collision = circle_collision or aabb_collision or obb_collision
    screen.fill(YELLOW if any_collision else WHITE)

    # 텍스트 색
    text_color = BLACK if any_collision else BLACK  # 노란 배경이라 검정 유지

    # 텍스트
    circle_text = font.render(f"Circle: {'HIT' if circle_collision else 'MISS'}", True, text_color)
    aabb_text = font.render(f"AABB: {'HIT' if aabb_collision else 'MISS'}", True, text_color)
    obb_text = font.render(f"OBB: {'HIT' if obb_collision else 'MISS'}", True, text_color)

    screen.blit(circle_text, (10, 10))
    screen.blit(aabb_text, (10, 40))
    screen.blit(obb_text, (10, 70))

    # 🔳 오브젝트
    pygame.draw.rect(screen, GRAY, player_rect)
    pygame.draw.polygon(screen, GRAY, fixed_corners)

    # 🔴 AABB (고정 크기 표시)
    pygame.draw.rect(screen, RED, player_rect, 2)
    pygame.draw.rect(screen, RED, fixed_aabb, 2)

    # 🔵 Circle
    pygame.draw.circle(screen, BLUE, player_center, player_radius, 2)
    pygame.draw.circle(screen, BLUE, fixed_center, fixed_radius, 2)

    # 🟢 OBB
    pygame.draw.polygon(screen, GREEN, fixed_corners, 2)

    pygame.display.flip()
    clock.tick(60)
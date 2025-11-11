import pygame
from rec_object import RecObject


# 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Physics Engine Base Structure")

# 게임 오브젝트 생성
rec1 = RecObject(100, 100, 50, 50)
rec2 = RecObject(200, 200, 50, 50)
game_objects = [rec1, rec2]


# ---- 드래그 상태 변수 ----
dragging = False
drag_target = None
offset_x, offset_y = 0, 0

# 메인 루프
running = True
while running:
    dt = clock.tick(60) / 1000.0  # deltaTime (초 단위)
    
    # ---- 이벤트 처리 ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---- 업데이트 ----
    for obj in game_objects:
        obj.update(dt, game_objects)

    # ---- 렌더링 ----
    screen.fill((25, 25, 25))
    for obj in game_objects:
        obj.render(screen)
    pygame.display.flip()

pygame.quit()

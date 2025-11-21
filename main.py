import pygame
from GameObject.rec_object import RecObject, RecObject2
from GameObject.floor import Floor
from GameObject.rotated_object import RotatedRecObject, RotatedRecObject2

# 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Physics Engine Base Structure")

# 게임 오브젝트 생성
rec1 = RecObject(100, 100, 50, 50)
rec2 = RecObject(200, 200, 50, 50)
rotated_rec = RotatedRecObject(400, 200, 100, 50, 75)
rotated_rec2 = RotatedRecObject2(400, 400, 100, 50, 225)
rec3 = RecObject2(600, 100, 80, 80)
floor = Floor(0, 550, 800, 50)

game_objects = [rec1, floor]
#game_objects = [rec1, rec2]
#game_objects_rigid = [rec3, floor]
#rotated_game_objects = [rotated_rec, rotated_rec2]


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

    #for obj in rotated_game_objects:
    #    obj.update(dt, rotated_game_objects)

    #for obj in game_objects_rigid:
    #    obj.update(dt, game_objects_rigid)

    # ---- 렌더링 ----
    screen.fill((25, 25, 25))
    for obj in game_objects:
        obj.render(screen)
    #for obj in game_objects_rigid:
    #    obj.render(screen)
    #for obj in rotated_game_objects:
    #    obj.render(screen)

    pygame.display.flip()

pygame.quit()

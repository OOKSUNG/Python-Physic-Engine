import pygame
from engine.Collider.AABBTree import AABBTree
from GameObject.rec_object import RecObject
from GameObject.floor import Floor
from GameObject.rotated_object import RotatedRecObject, RotatedRecObject2
from GameObject.swept_object import SweptRecObject

# 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Physics Engine Base Structure")

# 폰트 초기화 
pygame.font.init() 
font = pygame.font.SysFont('malgungothic', 30)

text_to_render = "Click and drag to move"
color_white = (138, 184, 91)
text_surface = font.render(text_to_render, True, color_white)


# 게임 오브젝트 생성
rec1 = RecObject(100, 100, 50, 50)
rec2 = RecObject(200, 100, 50, 50)
rec3 = RecObject(300, 100, 50, 50)
rec4 = RecObject(100, 200, 50, 50)
rec5 = RecObject(200, 200, 50, 50)
rec6 = RecObject(300, 200, 50, 50)

# obb 오브젝트
rotated_rec = RotatedRecObject(500, 200, 100, 50, 75)
rotated_rec2 = RotatedRecObject2(500, 400, 100, 50, 225)

# swept 오브젝트
swept_rec = SweptRecObject(600, 100, 150, 150)

# 바닥 오브젝트
floor = Floor(25, 525, 750, 50)

game_objects = [rec1, rec2, rec3, rec4, rec5, rec6, floor]
swept_objects = [swept_rec, floor]
rotated_game_objects = [rotated_rec, rotated_rec2]

# AABB 트리 생성 및 초기화
aabb_tree = AABBTree()

# 삽입하면서 node를 얻어 저장
for obj in game_objects:
    node = aabb_tree.insert(obj, obj.collider.aabb_box())
    obj.tree_node = node

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
        obj.update(dt) 
    
    for obj in game_objects:
        # 이동했으면 AABB 업데이트
        new_aabb = obj.collider.aabb_box()
        new_node = aabb_tree.update(obj.tree_node, new_aabb)
        obj.tree_node = new_node
        # Broadphase: AABB 후보 획득
        candidates = aabb_tree.query(obj.collider.aabb_box())
        for other in candidates:
            if other is obj:
                continue
            obj.on_collision(other, dt)

    #obb 충돌체크
    for obj in rotated_game_objects:
        obj.update(dt, rotated_game_objects)

    #swept 충돌체크
    for obj in swept_objects:
        obj.update(dt, swept_objects)

    # ---- 렌더링 ----
    screen.fill((40, 40, 40))
    for obj in game_objects:
        obj.render(screen)
    
    for obj in rotated_game_objects:
        obj.render(screen)

    for obj in swept_objects:
        obj.render(screen)
    
    aabb_tree.draw_tree(screen)

    screen.blit(text_surface, (30, 20))
    pygame.display.flip()

pygame.quit()

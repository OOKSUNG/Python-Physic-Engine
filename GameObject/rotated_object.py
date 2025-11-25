from engine.Entity.Rectangle import Rectangle
from engine.Collider.OBB import OBB
from engine.Phisic.RigidBody import RigidBody
import pygame

# 마우스 클릭 가능 범위
MARGIN = 10 

Gravity = [0, 0]  # 중력 가속도 벡터

class RotatedRecObject(Rectangle):
    def __init__(self, x, y, width, height, rotation):
        super().__init__(x, y, width, height, rotation)
        self.collider = OBB(self)
        self.color = (0, 0, 255)
        self.rigid_body = RigidBody(self, mass=1.0)

    def update(self, dt, game_objects=None):
        self.color = (0, 0, 255)

        # RigidBody 업데이트
        self.rigid_body.apply_force(Gravity)  # 중력 적용
        self.rigid_body.update(dt)
        
        update_drag(self)

        # 충돌 체크
        for obj in game_objects:
            if obj is not self and self.collider.obb(obj.collider):
                self.color = (255, 255, 0)
                break

    def render(self, screen):
        import pygame
        points = self.get_world_vertices()
        pygame.draw.polygon(screen, self.color, points)


class RotatedRecObject2(Rectangle):
    def __init__(self, x, y, width, height, rotation):
        super().__init__(x, y, width, height, rotation)
        self.collider = OBB(self)
        self.color = (0, 0, 255)

    def update(self, dt, game_objects=None):
        self.color = (0, 0, 255)

        update_drag(self)
        
        # 충돌 체크
        for obj in game_objects:
            if obj is not self and self.collider.obb(obj.collider):
                #print("Collision detected between RotatedRecObjects")
                self.color = (255, 255, 0)
                break

    def render(self, screen):
        import pygame
        points = self.get_world_vertices()
        pygame.draw.polygon(screen, self.color, points)

def update_drag(game_object):
    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()

    # 1. 사각형을 중심(center) 기준으로 생성
    # self.transform.position이 중심 좌표라고 가정
    temp_rect = pygame.Rect(0, 0, game_object.width, game_object.height)
    temp_rect.center = (game_object.transform.position[0], game_object.transform.position[1])

    # 2. 확장된 클릭 영역을 만듭니다. (.inflate 사용)
    extended_rect = temp_rect.inflate(2 * MARGIN, 2 * MARGIN)

    # 마우스 클릭 시 충돌 검사
    if mouse_pressed and extended_rect.collidepoint(mouse_pos):
        
        # 드래그 시작: drag_offset이 없으면 계산하여 저장
        if not hasattr(game_object, 'drag_offset'):
            # 마우스 위치와 사각형 중심 위치 사이의 벡터 차이
            game_object.drag_offset = [
                mouse_pos[0] - game_object.transform.position[0],
                mouse_pos[1] - game_object.transform.position[1]
            ]
            
        # 3. 사각형의 새 중심 위치 설정
        # 마우스 새 위치 - 드래그 오프셋 = 사각형의 새 중심 위치
        game_object.transform.position[0] = mouse_pos[0] - game_object.drag_offset[0]
        game_object.transform.position[1] = mouse_pos[1] - game_object.drag_offset[1]
        
    else:
        # 마우스 클릭 해제 시 drag_offset 제거
        if hasattr(game_object, 'drag_offset'):
            del game_object.drag_offset
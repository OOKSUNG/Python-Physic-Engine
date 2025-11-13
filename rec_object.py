from engine.Entity.Rectangle import Rectangle
from engine.Collider.AABB import AABB
from engine.Collider.OBB import OBB
from engine.Phisic.RigidBody import RigidBody
import pygame

Gravity = [0, 98.1]  # 중력 가속도 벡터

class RecObject(Rectangle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.collider = AABB(self)
        self.color = (255, 0, 0)

    def update(self, dt, game_objects=None):
        self.color = (255, 0, 0)

        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        rect = pygame.Rect(self.transform.position[0], self.transform.position[1], self.width, self.height)
        if mouse_pressed and rect.collidepoint(mouse_pos):
            if not hasattr(self, 'drag_offset'):
                self.drag_offset = [
                    mouse_pos[0] - self.transform.position[0],
                    mouse_pos[1] - self.transform.position[1]
                ]
            self.transform.position[0] = mouse_pos[0] - self.drag_offset[0]
            self.transform.position[1] = mouse_pos[1] - self.drag_offset[1]
        else:
            if hasattr(self, 'drag_offset'):
                del self.drag_offset

        # 충돌 체크
        for obj in game_objects:
            if obj is not self and self.collider.aabb(obj.collider):
                print("Collision detected between RecObjects")
                self.color = (0, 255, 0)
                break

    def render(self, screen):
        import pygame
        pygame.draw.rect(screen, self.color,
                         (self.transform.position[0], self.transform.position[1], self.width, self.height))
        
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
        
        # 충돌 체크
        for obj in game_objects:
            if obj is not self and self.collider.obb(obj.collider):
                print("Collision detected between RotatedRecObjects")
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

        
        # 충돌 체크
        for obj in game_objects:
            if obj is not self and self.collider.obb(obj.collider):
                print("Collision detected between RotatedRecObjects")
                self.color = (255, 255, 0)
                break

    def render(self, screen):
        import pygame
        points = self.get_world_vertices()
        pygame.draw.polygon(screen, self.color, points)
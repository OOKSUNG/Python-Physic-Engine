from engine.Entity.Rectangle import Rectangle
from engine.Collider.AABB import AABB
from engine.Phisic.RigidBody import RigidBody
import pygame

Gravity = [0, 98.1]  # 중력 가속도 벡터

class SweptRecObject(Rectangle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.collider = AABB(self)
        self.color = (255, 0, 0)
        self.rigidbody = RigidBody(self, mass=1.0)
        self.tree_node = None
        #self.rigidbody.velocity = [0, 50]  # 초기 속도 설정

    def update(self, dt, game_objects=None):
        self.color = (255, 0, 255)

        # RigidBody 업데이트
        self.rigidbody.apply_force(Gravity)  # 중력 적용
        self.rigidbody.update(dt)

        update_drag(self)
        
        # 충돌 체크
        for obj in game_objects:
            if obj is not self:
                if self.collider.aabb(obj.collider):
                    self.rigidbody.resolve_collision(obj.collider) 
                    self.color = (0, 255, 0)
                t_entry, normal = self.collider.swept_aabb(obj.collider, dt)
                self.rigidbody.swept_resolve_collision(obj.collider, normal, t_entry, dt)
                
                
    def render(self, screen):
        import pygame
        pygame.draw.rect(screen, self.color,
                         (self.transform.position[0], self.transform.position[1], self.width, self.height))
        
#드래그 처리
def update_drag(game_object):
    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(game_object.transform.position[0], game_object.transform.position[1], game_object.width, game_object.height)
    if mouse_pressed and rect.collidepoint(mouse_pos):
        if not hasattr(game_object, 'drag_offset'):
            game_object.drag_offset = [
                mouse_pos[0] - game_object.transform.position[0],
                mouse_pos[1] - game_object.transform.position[1]
            ]
        game_object.transform.position[0] = mouse_pos[0] - game_object.drag_offset[0]
        game_object.transform.position[1] = mouse_pos[1] - game_object.drag_offset[1]
    else:
        if hasattr(game_object, 'drag_offset'):
            del game_object.drag_offset         
        
       
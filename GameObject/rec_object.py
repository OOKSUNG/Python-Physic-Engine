from engine.Entity.Rectangle import Rectangle
from engine.Collider.AABB import AABB
from engine.Phisic.RigidBody import RigidBody
import pygame

Gravity = [0, 0]  # 중력 가속도 벡터

class RecObject(Rectangle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.collider = AABB(self)
        self.color = (255, 165, 0)
        self.rigidbody = RigidBody(self, mass=1.0)
        self.colliding = False

    def update(self, dt, game_objects=None):
        self.color = (255, 165, 0)

        #드래그 처리
        update_drag(self)

        # RigidBody 업데이트
        if self.colliding is False : self.rigidbody.apply_force(Gravity)  # 중력 적용
        self.rigidbody.update(dt)

    def render(self, screen):
        import pygame
        pygame.draw.rect(screen, self.color,
                         (self.transform.position[0], self.transform.position[1], self.width, self.height))

    def on_collision(self, other, dt):
        try:
            self.color = (0, 255, 0)
            # 충돌 시 반응 처리 (RigidBody 가지고 있으면)
            if hasattr(self, "rigidbody") and self.collider.aabb(other.collider):
                #self.rigidbody.resolve_collision(other.collider)
                pass
        except Exception as e:
            print("Error in on_collision:", e)
            
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
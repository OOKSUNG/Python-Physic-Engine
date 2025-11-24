from engine.Entity.Rectangle import Rectangle
from engine.Collider.AABB import AABB
from engine.Collider.OBB import OBB
from engine.Phisic.RigidBody import RigidBody
import pygame

class Floor(Rectangle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.collider = AABB(self)
        self.color = (255, 0, 0)
        self.rigidbody = RigidBody(self, mass=1.0)

    def update(self, dt, game_objects=None):
        self.color = (255, 0, 0)

        # RigidBody 업데이트
        self.rigidbody.update(dt)
        """
        # 충돌 체크
        for obj in game_objects:
            #if obj is not self and self.collider.aabb(obj.collider):
                #print("Collision detected between RecObjects")
                #self.rigidbody.velocity = [0, 0]
                #self.collider.resolve_collision(obj.collider)
                #self.color = (0, 255, 0)
                #break
                pass
        """
    def render(self, screen):
        import pygame
        pygame.draw.rect(screen, self.color,
                         (self.transform.position[0], self.transform.position[1], self.width, self.height)) 
        
    def check_collision(self, other):
        # NarrowPhase: 실제 AABB 충돌 체크
        return self.collider.aabb(other.collider)

    def on_collision(self, other):
        # 충돌 시 반응 처리 (RigidBody 가지고 있으면)
        if hasattr(self, "rigidbody"):
            self.rigidbody.resolve_collision(other.collider)


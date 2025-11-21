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

        # 충돌 체크
        for obj in game_objects:
            #if obj is not self and self.collider.aabb(obj.collider):
                #print("Collision detected between RecObjects")
                #self.rigidbody.velocity = [0, 0]
                #self.collider.resolve_collision(obj.collider)
                #self.color = (0, 255, 0)
                #break
                pass

    def render(self, screen):
        import pygame
        pygame.draw.rect(screen, self.color,
                         (self.transform.position[0], self.transform.position[1], self.width, self.height)) 
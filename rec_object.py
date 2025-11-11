from engine.Entity import Rectangle
from engine.Collider.AABB import AABB
import pygame

class RecObject(Rectangle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.collider = AABB(self, width, height)
        self.color = (255, 0, 0)

    def update_center(self):
        self.center[0] = self.transform.position[0] + self.width / 2
        self.center[1] = self.transform.position[1] + self.height / 2

    def update(self, dt, game_objects=None):
        self.color = (255, 0, 0)

        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        rect = pygame.Rect(self.transform.position[0], self.transform.position[1], self.width, self.height)
        if mouse_pressed and rect.collidepoint(mouse_pos):
            self.transform.position[0] = mouse_pos[0] - self.width / 2
            self.transform.position[1] = mouse_pos[1] - self.height / 2

        self.update_center()

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
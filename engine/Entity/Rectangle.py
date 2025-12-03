from engine.Entity.Entity import Entity

class Rectangle(Entity):
    def __init__(self, x, y, width, height, rotation = 0):
        super().__init__(x, y, rotation)
        self.width = width
        self.height = height
        self.center = [x + width / 2, y + height / 2]
        self.local_vertices = self.get_local_vertices()
        
    def get_local_vertices(self):
        half_w = self.width / 2
        half_h = self.height / 2
        return[
            [-half_w,-half_h],
            [half_w, -half_h],
            [half_w, half_h],
            [-half_w, half_h]
        ]  
    
    def render(self, screen):
        import pygame
        verts = self.get_world_vertices()
        pygame.draw.polygon(screen, (255, 0, 0), verts, 2)
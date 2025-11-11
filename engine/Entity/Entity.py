from engine.Entity.Transform import Transform

class Entity:
    def __init__(self, x, y):
        self.transform = Transform(x, y)
        self.center = self.transform.center

    def update(self, dt, game_objects=None):
        pass

    def render(self, screen):
        pass

class Rectangle(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.center = [x + width / 2, y + height / 2]


class Circle(Entity):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius


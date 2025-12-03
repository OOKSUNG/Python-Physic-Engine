from engine.Entity.Transform import Transform

class Entity:
    def __init__(self, x=0, y=0, rotation=0):
        self.transform = Transform([x, y], rotation)
        self.local_vertices = []

    def get_world_vertices(self):
        return [self.transform.apply(v) for v in self.local_vertices]

    def update(self, dt, game_objects=None):
        pass

    def render(self, screen):
        pass

class Circle(Entity):
    def __init__(self, x, y, radius):
        super().__init__(x, y)
        self.radius = radius


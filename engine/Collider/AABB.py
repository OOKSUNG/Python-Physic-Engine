from .Collider import Collider

class AABB(Collider):
    def __init__(self, entity, width, height):
        super().__init__(entity)
        self.width = width
        self.height = height

    def aabb(self, other):
        distance_x = abs(self.entity.center[0] - other.entity.center[0])
        distance_y = abs(self.entity.center[1] - other.entity.center[1])
        rect1_radius = [self.width / 2, self.height / 2]
        rect2_radius = [other.width / 2, other.height / 2]
        if distance_x > (rect1_radius[0] + rect2_radius[0]):
            return False
        if distance_y > (rect1_radius[1] + rect2_radius[1]):
            return False
        return True
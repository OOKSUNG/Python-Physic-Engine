from .Collider import Collider

class AABB(Collider):
    def __init__(self, entity):
        super().__init__(entity)
        self.width = entity.width
        self.height = entity.height

    def get_center(self):
        """Entity 위치 기준으로 현재 center 계산"""
        px, py = self.entity.transform.position
        return [px + self.width / 2, py + self.height / 2]

    def aabb(self, other):
        center1 = self.get_center()
        center2 = other.get_center()

        distance_x = abs(center1[0] - center2[0])
        distance_y = abs(center1[1] - center2[1])
        rect1_radius = [self.width / 2, self.height / 2]
        rect2_radius = [other.width / 2, other.height / 2]

        if distance_x > (rect1_radius[0] + rect2_radius[0]):
            return False
        if distance_y > (rect1_radius[1] + rect2_radius[1]):
            return False
        return True
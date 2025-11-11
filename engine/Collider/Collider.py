from engine import Entity as Entity

class Collider:
    def __init__(self, entity: Entity):
        self.entity = entity

    def aabb(self):
        pass
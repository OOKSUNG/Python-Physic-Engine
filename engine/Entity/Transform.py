from engine.Vector import rotate, translate
import math

class Transform:
    def __init__(self, position = [0, 0], rotation=0):
        self.position = position  # [x, y]
        self.rotation = math.radians(rotation)  # rad

    def apply(self, point):
        rotated = rotate(point, self.rotation)
        translated = translate(rotated, self.position)
        return translated

class AABBBox:
    def __init__(self, minx, miny, maxx, maxy):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def area(self):
        return (self.maxx - self.minx) * (self.maxy - self.miny)

    def merge(self, other):
        return AABBBox(
            min(self.minx, other.minx),
            min(self.miny, other.miny),
            max(self.maxx, other.maxx),
            max(self.maxy, other.maxy)
        )

    def intersects(self, other):
        return not (
            self.maxx < other.minx or
            self.minx > other.maxx or
            self.maxy < other.miny or
            self.miny > other.maxy
        )

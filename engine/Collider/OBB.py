from .Collider import Collider
from engine.Vector import dot, normalize

class OBB(Collider):
    def __init__(self, entity):
        super().__init__(entity)
        self.width = entity.width
        self.height = entity.height
        self.rotation = entity.transform.rotation  # Rotation in degrees

        # 꼭짓점 좌표들
        self.vertices = entity.get_world_vertices() 
        self.axes = self.get_axes()

    def get_axes(self):
        verts = self.vertices
        axes = []
        for i in range(2):
            p1 = verts[i]
            p2 = verts[i + 1]
            edge = [p2[0] - p1[0], p2[1] - p1[1]]
            normal = [-edge[1], edge[0]]  # 수직 벡터
            axes.append(normalize(normal))  # 단위 벡터로 정규화
        return axes

    def obb(self, other):
        self.vertices = self.entity.get_world_vertices()
        other.vertices = other.entity.get_world_vertices()
        axes = self.get_axes() + other.get_axes()

        for axis in axes:
            min_self, max_self = float('inf'), float('-inf')
            min_other, max_other = float('inf'), float('-inf')

            for v in self.vertices:
                p = dot(v, axis)
                min_self = min(min_self, p)
                max_self = max(max_self, p)

            for v in other.vertices:
                p = dot(v, axis)
                min_other = min(min_other, p)
                max_other = max(max_other, p)

            # 겹치는지 체크
            if max_self < min_other or max_other < min_self:
                return False  # 분리 축 발견 → 충돌 없음
        
        return True  # 모든 축에서 겹침 → 충돌


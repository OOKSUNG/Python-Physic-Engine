from .Collider import Collider
from .AABBBox import AABBBox

class AABB(Collider):
    def __init__(self, entity):
        super().__init__(entity)
        self.width = entity.width
        self.height = entity.height

    def get_center(self):
        """Entity 위치 기준으로 현재 center 계산"""
        px, py = self.entity.transform.position
        return [px + self.width / 2, py + self.height / 2]

    """AABB 박스 계산"""
    def aabb_box(self):
        x = self.entity.transform.position[0]
        y = self.entity.transform.position[1]

        half_w = self.width / 2
        half_h = self.height / 2
        """
        minx = x - half_w
        miny = y - half_h
        maxx = x + half_w
        maxy = y + half_h
        """
        minx = x
        miny = y
        maxx = x + half_w * 2
        maxy = y + half_h * 2

        return AABBBox(minx, miny, maxx, maxy)

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
    
    def swept_aabb(self, other, dt):
        print(type(self.entity.rigidbody.velocity), self.entity.rigidbody.velocity)
        vx = self.entity.rigidbody.velocity[0]
        vy = self.entity.rigidbody.velocity[1]

        ovx = other.entity.rigidbody.velocity[0] #if hasattr(other.entity, "rigidbody") else 0
        ovy = other.entity.rigidbody.velocity[1] #if hasattr(other.entity, "rigidbody") else 0

        # 상대 속도
        rvx = vx - ovx
        rvy = vy - ovy
        #print(type(vx), vx, type(vy), vy, type(ovx), ovx, type(ovy), ovy)
        

        # 현재 박스 bounds
        x = self.entity.transform.position[0]
        y = self.entity.transform.position[1]
        w = self.width
        h = self.height

        ox = other.entity.transform.position[0]
        oy = other.entity.transform.position[1]
        ow = other.width
        oh = other.height

        # Expanded AABB
        ex_left   = ox - w
        ex_top    = oy - h
        ex_right  = ox + ow
        ex_bottom = oy + oh

        #ex_left, ex_top, ex_right, ex_bottom = get_expanded_rect(self, other)

        # t_entry / t_exit 계산
        if rvx > 0:
            tx_entry = (ex_left - x) / rvx
            tx_exit  = (ex_right - x) / rvx
        elif rvx < 0:
            tx_entry = (ex_right - x) / rvx
            tx_exit  = (ex_left - x) / rvx
        else:
            tx_entry = -999999
            tx_exit  = 999999

        if rvy > 0:
            ty_entry = (ex_top - y) / rvy
            ty_exit  = (ex_bottom - y) / rvy
        elif rvy < 0:
            ty_entry = (ex_bottom - y) / rvy
            ty_exit  = (ex_top - y) / rvy
        else:
            ty_entry = -999999
            ty_exit  = 999999

        # 최종 충돌 시간
        t_entry = max(tx_entry, ty_entry)
        t_exit = min(tx_exit, ty_exit)

        # 충돌 조건 체크
        if t_entry > t_exit:
            return 1.0, None  # 충돌 없음
        if t_entry < 0 or t_entry > 1:
            return 1.0, None  # 프레임 범위를 벗어남 → 충돌 없음

        # 충돌 방향 계산
        if tx_entry > ty_entry:
            normal = [-1, 0] if rvx > 0 else [1, 0]
        else:
            normal = [0, -1] if rvy > 0 else [0, 1]

        return t_entry, normal
     
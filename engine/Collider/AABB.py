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
    
    def swept_aabb(self, other, dt):
        #print(type(self.entity.rigidbody.velocity), self.entity.rigidbody.velocity)
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
    """
    def check_swept_collision(self, dt, game_objects):
        
        #dt: 프레임 시간
        #game_objects: 충돌 체크 대상 리스트
        
        earliest_t = 1.0
        collision_normal = None
        collided_obj = None

        for obj in game_objects:
            if obj is self:
                continue

            t, normal = self.entity.collider.swept_aabb(obj.collider, dt)
            if t < earliest_t:
                earliest_t = t
                collision_normal = normal
                collided_obj = obj

        # 예상 이동 거리 계산
        dx = self.entity.rigidbody.velocity[0] * dt
        dy = self.entity.rigidbody.velocity[1] * dt

        # 충돌이 있으면 이동 거리 조정
        self.entity.transform.position[0] += dx * earliest_t
        self.entity.transform.position[1] += dy * earliest_t

        # 충돌 처리
        if collision_normal:
            if collision_normal[0] != 0:
                self.entity.rigidbody.velocity[0] = 0
            if collision_normal[1] != 0:
                self.entity.rigidbody.velocity[1] = 0

            # 남은 시간 동안 속도 적용
            remaining_dt = dt * (1 - earliest_t)
            self.entity.transform.position[0] += self.entity.rigidbody.velocity[0] * remaining_dt
            self.entity.transform.position[1] += self.entity.rigidbody.velocity[1] * remaining_dt
        
        self
        return collided_obj, collision_normal, t
    """
    # AABB 클래스 안에 추가
    def get_expanded_rect(self, other):
        """
        other 를 self 크기만큼 확장한 rect 반환: (left, top, width, height)
        self: moving box
        other: target box
        """
        ox = other.entity.transform.position[0]
        oy = other.entity.transform.position[1]
        ow = other.width
        oh = other.height

        # other 를 self의 크기만큼 확장 (left-top 기준)
        left = ox - self.width
        top  = oy - self.height
        width = ow + self.width
        height = oh + self.height
        return (left, top, width, height)



    
    def resolve_collision(self, static):

        mx, my = self.entity.transform.position
        mw, mh = self.width, self.height
        sx, sy = static.entity.transform.position
        sw, sh = static.width, static.height

        # 중심 좌표
        dx = (mx + mw / 2) - (sx + sw / 2)
        dy = (my + mh / 2) - (sy + sh / 2)

        # 겹친 거리 계산
        overlap_x = (mw / 2 + sw / 2) - abs(dx)
        overlap_y = (mh / 2 + sh / 2) - abs(dy)

        if overlap_x > 0 and overlap_y > 0:  # 충돌함
            # 더 적게 겹친 축으로 보정
            if overlap_x < overlap_y:
                move_x = overlap_x if dx < 0 else -overlap_x
                self.entity.transform.position[0] += move_x
                self.entity.rigidbody.velocity[0] = 0
            else:
                move_y = overlap_y if dy < 0 else -overlap_y
                self.entity.transform.position[1] += move_y
                self.entity.rigidbody.velocity[1] = 0
            return True
        return False

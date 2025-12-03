
class RigidBody:
    def __init__(self, entity, mass=1.0, restitution=0.0):
        self.entity = entity
        self.mass = mass
        self.velocity = [0.0, 0.0]  # [vx, vy]
        self.acceleration = [0.0, 0.0]  # [ax, ay]
        self.restitution = restitution

    def apply_force(self, force):
        # F = m * a → a = F / m
        self.acceleration[0] += force[0] / self.mass
        self.acceleration[1] += force[1] / self.mass

    def update(self, dt):
        # 속도 갱신
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        # 위치 업데이트
        self.entity.transform.position[0] += self.velocity[0] * dt
        self.entity.transform.position[1] += self.velocity[1] * dt
        
        # 가속도 초기화 (다음 프레임 계산용)
        self.acceleration = [0.0, 0.0]

    def resolve_collision(self, other_collider, axis=None):
        if not self.entity.collider.aabb(other_collider):
            return  # 충돌이 아니면 무시

        # self가 아래로 이동해서 other와 겹칠 때
        my = self.entity.transform.position[1]
        oy = other_collider.entity.transform.position[1]

        if my + self.entity.height > oy and self.velocity[1] > 0:
            # self를 겹치지 않게 위치 수정
            self.entity.transform.position[1] = oy - self.entity.height
            # 속도 반사 (반발계수 적용)
            self.velocity[1] = -self.velocity[1] * self.restitution
        
    def swept_resolve_collision(self, other_collider, normal, t_entry, dt):
        if normal is None:
            # 충돌이 없으면 아무 작업도 하지 않음
            self.entity.transform.position[0] += self.entity.rigidbody.velocity[0] * dt
            self.entity.transform.position[1] += self.entity.rigidbody.velocity[1] * dt
            return
        print("Swept Collision Detected")

        # 충돌 발생 전 이동분 적용
        dx = self.velocity[0] * t_entry * dt
        dy = self.velocity[1] * t_entry * dt
        self.entity.transform.position[0] += dx
        self.entity.transform.position[1] += dy
        print(type(dx), dx, type(dy), dy)
        
        self.velocity = [0, 0]  # 충돌 시 속도 0으로 설정

        self.color = (0, 255, 0)
        # 남은 시간 동안 이동 
        remaining_dt = dt * (1 - t_entry)
        self.entity.transform.position[0] += self.velocity[0] * remaining_dt
        self.entity.transform.position[1] += self.velocity[1] * remaining_dt
        
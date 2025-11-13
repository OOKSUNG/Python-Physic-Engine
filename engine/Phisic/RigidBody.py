from engine.Entity.Entity import Entity

class RigidBody:
    def __init__(self, entity, mass=1.0):
        self.entity = entity
        self.mass = mass
        self.velocity = [0.0, 0.0]  # [vx, vy]
        self.acceleration = [0.0, 0.0]  # [ax, ay]

    def apply_force(self, force):
        # F = m * a → a = F / m
        self.acceleration[0] += force[0] / self.mass
        self.acceleration[1] += force[1] / self.mass

    def update(self, dt):
        # 속도 갱신
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt
        # 위치 갱신
        self.entity.transform.position[0] += self.velocity[0] * dt
        self.entity.transform.position[1] += self.velocity[1] * dt
        # 가속도 초기화 (다음 프레임 계산용)
        self.acceleration = [0.0, 0.0]
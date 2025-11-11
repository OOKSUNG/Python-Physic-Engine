class Transform:
    def __init__(self, x=0, y=0, rotation=0):
        self.position = [x, y]  # [x, y]
        self.center = [x, y]
        self.rotation = rotation  # rad
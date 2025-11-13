import math

def add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

def sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def mul_scalar(v, s):
    return [v[0] * s, v[1] * s]

def rotate(v, angle, origin=[0, 0]):
    """
    v : [x, y]
    angle : rad
    origin : 회전 중심
    """
    x, y = v[0] - origin[0], v[1] - origin[1]
    cos_r = math.cos(angle)
    sin_r = math.sin(angle)
    x_new = x * cos_r - y * sin_r
    y_new = x * sin_r + y * cos_r
    return [x_new + origin[0], y_new + origin[1]]

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def normalize(v):
    length = math.sqrt(v[0] ** 2 + v[1] ** 2)
    if length == 0:
        return [0, 0]
    return [v[0] / length, v[1] / length]   

def translate(v, offset):
    return add(v, offset)
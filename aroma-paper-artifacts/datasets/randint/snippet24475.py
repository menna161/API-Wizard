import math, random, flow_field


def __init__(self):
    self.pos = Vector(x=random.randint(0, flow_field.dimensions[0]), y=random.randint(0, flow_field.dimensions[1]))
    self.velocity = Vector(x=0, y=0)
    self.acc = Vector(x=0, y=0)
    self.max_speed = 15

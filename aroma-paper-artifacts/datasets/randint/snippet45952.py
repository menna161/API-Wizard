from fake_rpi.wrappers import printf
from random import randint
from fake_rpi.Base import Base


@printf
def read_i2c_block_data(self, a, b, c):
    return ([randint(0, ((2 ** 8) - 1))] * c)

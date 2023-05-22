from fake_rpi.wrappers import printf
from random import randint
from fake_rpi.Base import Base


@printf
def read_byte_data(self, i2c_addr, register):
    return randint(0, ((2 ** 8) - 1))

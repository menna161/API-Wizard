from fake_rpi.wrappers import printf
from fake_rpi.Base import Base
from random import randint


@printf
def input(self, channel):
    if ((channel in self._inputs) and (self._inputs[channel] is not None)):
        return self._inputs[channel]
    return randint(0, 1)

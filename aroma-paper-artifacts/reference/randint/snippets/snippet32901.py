import os
from rsa import common, transform
from rsa._compat import byte


def randint(maxvalue):
    'Returns a random integer x with 1 <= x <= maxvalue\n\n    May take a very long time in specific situations. If maxvalue needs N bits\n    to store, the closer maxvalue is to (2 ** N) - 1, the faster this function\n    is.\n    '
    bit_size = common.bit_size(maxvalue)
    tries = 0
    while True:
        value = read_random_int(bit_size)
        if (value <= maxvalue):
            break
        if (tries and ((tries % 10) == 0)):
            bit_size -= 1
        tries += 1
    return value

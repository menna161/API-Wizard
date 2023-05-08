import random
import string


def gen_rand_keys(size, _min, _max):
    return [random.randint(_min, _max) for _ in range(size)]

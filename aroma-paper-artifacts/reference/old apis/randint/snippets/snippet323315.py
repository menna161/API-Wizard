import string
import unittest
from random import choice, randint
from ands.algorithms.recursion.make_decimal import make_decimal


@staticmethod
def generate_number(base: int):

    def build_possible_digits(base: int):
        possible_digits = list(string.digits)
        if (base < 10):
            possible_digits = possible_digits[0:base]
        elif (base > 10):
            possible_digits += list(string.ascii_lowercase)[0:(base - 10)]
        return possible_digits
    pd = build_possible_digits(base)
    length = randint(1, 10)
    return ''.join([choice(pd) for _ in range(length)])

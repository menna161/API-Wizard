import string
import unittest
from random import choice, randint
from ands.algorithms.recursion.make_decimal import make_decimal


def test_random_base(self):
    for _ in range(randint(100, 1000)):
        b = randint(2, 36)
        n = TestMakeDecimal.generate_number(b)
        self.assertEqual(make_decimal(n, b), int(n, b))

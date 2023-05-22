import unittest
from random import randint
from ands.algorithms.recursion.power import power


def test_random_base_power_1(self):
    a = randint(2, 100)
    b = randint((- 100), (- 2))
    self.assertEqual(power(a, 1), a)
    self.assertEqual(power(b, 1), b)

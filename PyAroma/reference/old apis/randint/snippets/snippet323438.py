import unittest
from random import randint
from ands.algorithms.recursion.power import power


def test_random_base_random_positive_power(self):
    b = randint((- 100), 100)
    p = randint(2, 100)
    self.assertEqual(power(b, p), (b ** p))

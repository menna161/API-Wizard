import unittest
from random import randint
from ands.algorithms.recursion.power import power


def test_base_random_base_power_0(self):
    self.assertEqual(power(randint(2, 100), 0), 1)
    self.assertEqual(power(randint((- 100), (- 2)), 0), 1)

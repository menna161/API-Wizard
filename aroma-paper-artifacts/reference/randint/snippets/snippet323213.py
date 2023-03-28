import unittest
from random import randint, random
from ands.algorithms.dp.fibonacci import bottom_up_fibonacci, memoized_fibonacci, recursive_fibonacci


def test_input_is_negative(self):
    n = randint((- 1000), (- 1))
    self.assertRaises(ValueError, recursive_fibonacci, n)
    self.assertRaises(ValueError, memoized_fibonacci, n)
    self.assertRaises(ValueError, bottom_up_fibonacci, n)

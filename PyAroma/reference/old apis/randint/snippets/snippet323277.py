import unittest
from random import randint
from ands.algorithms.recursion.is_sorted import *


def test_random_size_tuple_sorted(self):
    tup = [randint((- 100), 100) for _ in range(randint(3, 300))]
    tup.sort()
    tup = tuple(tup)
    self.assertTrue(is_sorted(tup))
    self.assertTrue(iterative_is_sorted(tup))
    self.assertTrue(pythonic_is_sorted(tup))

import unittest
from random import randint
from ands.algorithms.recursion.is_sorted import *


def test_random_size_tuple_rev(self):
    tup = [randint((- 100), 100) for _ in range(randint(3, 300))]
    tup.sort(reverse=True)
    tup = tuple(tup)
    self.assertTrue(is_sorted(tup, True))
    self.assertTrue(iterative_is_sorted(tup, True))
    self.assertTrue(pythonic_is_sorted(tup, True))

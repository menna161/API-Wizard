import unittest
from random import randint
from ands.algorithms.recursion.is_sorted import *


def test_random_size_list_sorted(self):
    ls = [randint((- 100), 100) for _ in range(randint(3, 300))]
    ls.sort()
    self.assertTrue(is_sorted(ls))
    self.assertTrue(iterative_is_sorted(ls))
    self.assertTrue(pythonic_is_sorted(ls))

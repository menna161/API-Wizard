import unittest
from random import randint
from ands.algorithms.recursion.is_sorted import *


def test_random_size_list_rev(self):
    ls = [randint((- 100), 100) for _ in range(randint(3, 300))]
    ls.sort(reverse=True)
    self.assertTrue(is_sorted(ls, True))
    self.assertTrue(iterative_is_sorted(ls, True))
    self.assertTrue(pythonic_is_sorted(ls, True))

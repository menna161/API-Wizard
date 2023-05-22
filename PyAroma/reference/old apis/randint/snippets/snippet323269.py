import unittest
from random import randint
from ands.algorithms.recursion.is_sorted import *


def test_size_1_list(self):
    r = randint((- 10), 10)
    self.assertTrue(is_sorted([r]))
    self.assertTrue(is_sorted([r], True))
    self.assertTrue(iterative_is_sorted([r]))
    self.assertTrue(iterative_is_sorted([r], True))
    self.assertTrue(pythonic_is_sorted([r]))
    self.assertTrue(pythonic_is_sorted([r], True))

import unittest
from random import randint
from ands.algorithms.dac.find_extrema import *


def test_list_random_size_max_and_min_are_somewhere(self):
    ls = [randint((- 100), 100) for _ in range(3, 1000)]
    self.assertEqual(find_max(ls), max(ls))
    self.assertEqual(find_min(ls), min(ls))

import unittest
from random import randint
from ands.algorithms.dac.find_extrema import *


def test_list_random_size_max_is_first_min_is_last(self):
    ls = list(range(randint(3, 1000), (- 1), (- 1)))
    self.assertEqual(find_max(ls), ls[0])
    self.assertEqual(find_min(ls), ls[(- 1)])

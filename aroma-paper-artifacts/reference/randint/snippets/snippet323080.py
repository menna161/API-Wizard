import unittest
from random import choice, randint
from ands.algorithms.dac.binary_search import *


def test_list_random_size_does_not_exist_upper(self):
    upper = 10000
    ls = list(range(randint(3, upper)))
    self.assertEqual(linear_search(ls, upper), (- 1))
    self.assertEqual(binary_search_iteratively(ls, upper), (- 1))
    self.assertEqual(binary_search_recursively_in_place(ls, upper), (- 1))
    self.assertFalse(binary_search_recursively_not_in_place(ls, upper))

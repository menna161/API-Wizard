import unittest
from random import choice, randint
from ands.algorithms.dac.binary_search import *


def test_list_random_size_does_not_exist_lower(self):
    ls = list(range(randint(3, 10000)))
    self.assertEqual(linear_search(ls, (- 1)), (- 1))
    self.assertEqual(binary_search_iteratively(ls, (- 1)), (- 1))
    self.assertEqual(binary_search_recursively_in_place(ls, (- 1)), (- 1))
    self.assertFalse(binary_search_recursively_not_in_place(ls, (- 1)))

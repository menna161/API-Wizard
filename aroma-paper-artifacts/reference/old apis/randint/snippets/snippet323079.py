import unittest
from random import choice, randint
from ands.algorithms.dac.binary_search import *


def test_list_random_size_exists(self):
    ls = list(range(randint(3, 10000)))
    item = choice(ls)
    index = ls.index(item)
    self.assertEqual(linear_search(ls, item), index)
    self.assertEqual(binary_search_iteratively(ls, item), index)
    self.assertEqual(binary_search_recursively_in_place(ls, item), index)
    self.assertTrue(binary_search_recursively_not_in_place(ls, item))

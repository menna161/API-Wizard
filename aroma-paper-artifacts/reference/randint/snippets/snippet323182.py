import unittest
from random import randint
from ands.algorithms.recursion.count import count


def test_random_size(self):
    ls = [randint((- 10), 10) for _ in range(randint(5, 15))]
    self.assertEqual(count((- 11), ls), 0)

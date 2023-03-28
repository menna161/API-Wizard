import unittest
from random import randint, randrange, sample
from ands.algorithms.dac.select import select


def test_when_list_random_size_k_is_zero(self):
    a = [randint((- 100), 100) for _ in range(randint(3, 100))]
    self.assertEqual(select(a, 0), min(a))

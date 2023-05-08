import unittest
from random import randint, randrange, sample
from ands.algorithms.dac.select import select


def test_when_list_random_size_all_elements_equal(self):
    x = randint((- 100), 100)
    a = ([x] * randint(1, 100))
    self.assertEqual(select(a, randint(0, (len(a) - 1))), x)

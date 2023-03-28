import string
import unittest
from random import choice, randint, sample, shuffle
from ands.ds.LinearProbingHashTable import LinearProbingHashTable, has_duplicates_ignore_nones


def test_put_n_distinct_keys_equal_values(self):
    t = LinearProbingHashTable()
    n = randint(2, 1000)
    population = sample(range(n), n)
    for elem in population:
        t.put(elem, elem)
    self.assertEqual(t.size, n)
    for elem in population:
        self.assertIsNotNone(t.get(elem))

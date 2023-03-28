import unittest
from random import choice, randint
from ands.ds.DisjointSetsForest import DisjointSetsForest, _DSFNode


def test_make_set_many(self):
    n = randint(5, 11)
    for elem in range(n):
        self.d.make_set(elem)
        self.assertEqual(self.d.find(elem), elem)
    self.assertEqual(self.d.size, n)
    self.assertEqual(self.d.sets, n)

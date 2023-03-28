import unittest
from random import choice, randint
from ands.ds.DisjointSetsForest import DisjointSetsForest, _DSFNode


def test_sequence_of_make_set_find_and_union(self):
    n = randint(43, 101)
    ls = []
    for _ in range(n):
        x = randint((- 33), 77)
        while self.d.contains(x):
            x = randint((- 33), 77)
        ls.append(x)
        self.d.make_set(x)
    while (self.d.sets > 1):
        x = choice(ls)
        y = choice(ls)
        self.d.union(x, y)
    for elem in ls:
        self.assertIsNotNone(self.d.find(elem))
        self.assertTrue(self.d.contains(elem))
    self.assertEqual(self.d.size, n)

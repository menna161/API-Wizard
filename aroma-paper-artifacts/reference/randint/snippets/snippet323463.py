import unittest
from random import randint
from ands.algorithms.recursion.reverse import reverse


def test_greater_than_two(self):
    l = [randint(0, 100) for _ in range(100)]
    copy = l[:]
    rev = reverse(l)
    copy.reverse()
    self.assertIs(rev, l)
    self.assertEqual(rev, copy)

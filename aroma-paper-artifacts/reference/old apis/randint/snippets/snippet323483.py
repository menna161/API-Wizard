import unittest
from random import randint
from ands.ds.Stack import Stack


def test_pop_until_empty(self):
    ls = [randint((- 10), 10) for _ in range(randint(1, 100))]
    s = Stack(ls)
    for (i, e) in enumerate(reversed(ls)):
        elem = s.pop()
        self.assertEqual(elem, e)
        self.assertEqual(s.size, (len(ls) - (i + 1)))
    self.assertTrue(s.is_empty())

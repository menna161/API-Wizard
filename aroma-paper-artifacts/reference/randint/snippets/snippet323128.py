import string
import unittest
from random import choice, randint
from ands.ds.BST import BST, _BSTNode


def test_delete_all_in_random_order(self):
    ls = [randint((- 100), 100) for _ in range(1000)]
    for e in ls:
        self.t.insert(e)
    for _ in range(len(ls)):
        elem = choice(ls)
        ls.remove(elem)
        self.assertIsNone(self.t.delete(elem))
    self.assertTrue(self.t.is_empty())

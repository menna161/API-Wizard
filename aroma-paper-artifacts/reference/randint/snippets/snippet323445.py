import unittest
from random import randint
from ands.ds.Queue import Queue


def test_creation_good_list_random_size(self):
    r = randint(2, 50)
    q = Queue([randint((- 10), 10) for _ in range(r)])
    self.assertEqual(q.size, r)

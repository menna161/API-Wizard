import unittest
from random import randint
from ands.ds.Queue import Queue


def test_enqueue_many(self):
    q = Queue()
    r = randint(2, 100)
    ls = [randint((- 100), 100) for _ in range(r)]
    for (i, elem) in enumerate(ls):
        q.enqueue(elem)
        self.assertEqual(q.size, (i + 1))

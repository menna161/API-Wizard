import unittest
from random import choice, randint, sample
from ands.ds.MinHeap import MinHeap, is_min_heap


def test_add_multiple_elements(self):
    a = [randint((- 100), 100) for _ in range(100)]
    h = MinHeap()
    for (i, elem) in enumerate(a):
        self.assertIsNone(h.add(elem))
        self.assertEqual(h.size, (i + 1))
    self.assertFalse(h.is_empty())
    self.assertEqual(h.find_min(), min(a))

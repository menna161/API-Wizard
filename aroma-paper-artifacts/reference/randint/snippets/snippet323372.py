import unittest
from random import choice, randint, sample
from ands.ds.MinHeap import MinHeap, is_min_heap


def test_remove_min_when_heap_has_random_size(self):
    size = randint(3, 100)
    a = [randint((- 100), 100) for _ in range(size)]
    h = MinHeap(a)
    m = min(a)
    self.assertEqual(h.remove_min(), m)
    self.assertFalse(h.is_empty())
    self.assertEqual(h.size, (size - 1))

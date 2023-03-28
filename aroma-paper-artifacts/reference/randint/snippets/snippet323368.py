import unittest
from random import choice, randint, sample
from ands.ds.MinHeap import MinHeap, is_min_heap


def test_find_min_when_heap_has_random_size(self):
    a = [randint((- 100), 100) for _ in range(3, 100)]
    h = MinHeap(a)
    self.assertEqual(h.find_min(), min(a))

import unittest
from random import choice, randint, sample
from ands.ds.MinMaxHeap import MinMaxHeap, is_min_max_heap


def test_find_max_when_heap_has_random_size(self):
    a = [randint((- 100), 100) for _ in range(3, 100)]
    h = MinMaxHeap(a)
    self.assertEqual(h.find_max(), max(a))

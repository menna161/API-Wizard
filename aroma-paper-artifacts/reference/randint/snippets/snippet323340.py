import unittest
from random import choice, randint, sample
from ands.ds.MaxHeap import MaxHeap, is_max_heap


def test_find_max_when_heap_has_random_size(self):
    a = [randint((- 100), 100) for _ in range(3, 100)]
    h = MaxHeap(a)
    self.assertEqual(h.find_max(), max(a))

import unittest
from random import choice, randint, sample
from ands.ds.MinMaxHeap import MinMaxHeap, is_min_max_heap


def test_remove_max_when_heap_has_random_size(self):
    size = randint(3, 100)
    a = [randint((- 100), 100) for _ in range(size)]
    h = MinMaxHeap(a)
    m = max(a)
    self.assertEqual(h.remove_max(), m)
    self.assertFalse(h.is_empty())
    self.assertEqual(h.size, (size - 1))

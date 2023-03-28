import unittest
from random import choice, randint, sample
from ands.ds.MinMaxHeap import MinMaxHeap, is_min_max_heap


def test_clear_heap_of_random_size(self):
    h = MinMaxHeap([randint((- 100), 100) for _ in range(100)])
    self.assertIsNone(h.clear())
    self.assertEqual(h.size, 0)
    self.assertTrue(h.is_empty())

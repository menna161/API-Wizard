import unittest
from random import choice, randint, sample
from ands.ds.MinHeap import MinHeap, is_min_heap


def test_clear_heap_of_random_size(self):
    h = MinHeap([randint((- 100), 100) for _ in range(100)])
    self.assertIsNone(h.clear())
    self.assertEqual(h.size, 0)
    self.assertTrue(h.is_empty())

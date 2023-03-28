import unittest
from random import choice, randint, sample
from ands.ds.MinHeap import MinHeap, is_min_heap


def test_delete_all_when_heap_of_random_size(self):
    size = randint(3, 100)
    a = [randint((- 100), 100) for _ in range(size)]
    h = MinHeap(a)
    for _ in range(size):
        self.assertIsNone(h.delete(choice(a)))
        self.assertTrue(is_min_heap(h))
    self.assertEqual(h.size, 0)
    self.assertTrue(h.is_empty())

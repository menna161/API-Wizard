import random
import string
import unittest
from ands.ds.TST import TST, _TSTNode


def test_delete_all_random_keys(self):
    t = TST()
    n = random.randint(3, 2000)
    random_pairs = {}
    for _ in range(n):
        key = TestTST.gen_rand_str(random.randint(1, 11))
        random_pairs[key] = key
        t.insert(key, key)
    for (k, v) in random_pairs.items():
        self.assertEqual(t.delete(k), v)
        self.assertIsNone(t.search(k))
        self.assertFalse(t.contains(k))
    self.assertTrue(t.is_empty())
    self.assertEqual(t.count(), 0)

import random
import string
import unittest
from ands.ds.TST import TST, _TSTNode


def test_insert_random_keys(self):
    t = TST()
    n = random.randint(4, 100)
    random_pairs = {}
    for _ in range(n):
        key = TestTST.gen_rand_str(random.randint(1, 11))
        random_pairs[key] = key
        t.insert(key, key)
        self.assertFalse(t.is_empty())
        self.assertEqual(t.count(), len(random_pairs))
    for (k, v) in random_pairs.items():
        self.assertEqual(t.search(k), v)
        self.assertTrue(t.contains(k))

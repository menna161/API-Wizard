import random
import string
import unittest
from ands.ds.TST import TST, _TSTNode


def test_keys_with_prefix_empty_prefix(self):
    t = TST()
    n = random.randint(1, 50)
    keys = set()
    for _ in range(n):
        key = TestTST.gen_rand_str(random.randint(1, 11))
        keys.add(key)
        t.insert(key, key)
    kwp = t.keys_with_prefix('')
    kwp_set = set(kwp)
    self.assertEqual(len(kwp), len(kwp_set))
    self.assertEqual(kwp_set, keys)

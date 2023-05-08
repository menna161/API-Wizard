import random
import string
import unittest
from ands.ds.TST import TST, _TSTNode


def test_all_pairs_random_size_and_strings(self):
    t = TST()
    n = random.randint(3, 1000)
    random_pairs = {}
    for _ in range(n):
        key = TestTST.gen_rand_str(random.randint(1, 17))
        random_pairs[key] = key
        t.insert(key, key)
    self.assertEqual(t.all_pairs(), random_pairs)

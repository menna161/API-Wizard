import random
import collections
import statistics
from hypothesis import given
import hypothesis.strategies as st
from hypothesis import find, settings, Verbosity
from hypothesis.strategies import lists, integers
import unittest
from strgen import StringGenerator as SG


def test_seeded_randomizer(self):
    pattern = '[\\w]{10}&([\\d]{10}|M3W9MF_lH3906I14O50)'
    for seed in [random.randint(1, 100000000) for _ in range(100)]:
        sg = SG(pattern, seed=seed)
        s1 = sg.render()
        sg = SG(pattern, seed=seed)
        s2 = sg.render()
        assert (s1 == s2)
        sg = SG(pattern, seed=seed)
        list1 = sg.render_list(100)
        sg = SG(pattern, seed=seed)
        list2 = sg.render_list(100)
        assert (collections.Counter(list1) == collections.Counter(list2))

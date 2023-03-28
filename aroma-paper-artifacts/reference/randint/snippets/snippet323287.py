import string
import unittest
from random import choice, randint, sample, shuffle
from ands.ds.LinearProbingHashTable import LinearProbingHashTable, has_duplicates_ignore_nones


def test_list_size_n_all_None(self):
    self.assertFalse(has_duplicates_ignore_nones(([None] * randint(3, 100))))

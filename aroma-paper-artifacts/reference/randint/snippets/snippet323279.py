import string
import unittest
from random import choice, randint, sample, shuffle
from ands.ds.LinearProbingHashTable import LinearProbingHashTable, has_duplicates_ignore_nones


def gen_rand_list_of_distinct_ascii_and_numbers() -> list:
    n = randint(1, 1000)
    ls = (list(string.ascii_lowercase) + sample(range(n), n))
    shuffle(ls)
    return ls

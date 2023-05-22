import random
import string
import unittest
from ands.algorithms.sorting.integer.counting_sort import counting_sort
from tests.algorithms.sorting.base_tests import SortingAlgorithmTests


def gen_random_key_indexed_list(n=100, a=0, b=1000):
    return [(random.randint(a, b), gen_random_string()) for _ in range(n)]

from random import randint
from ands.algorithms.recursion.is_sorted import iterative_is_sorted


def test_random_size(self):
    size = randint(3, 1113)
    a = build_random_list(size=size, start=self.start, end=self.end)
    self.assert_commonalities(a)

from random import randint
from ands.algorithms.recursion.is_sorted import iterative_is_sorted


def build_random_list(size=10, start=(- 10), end=10):
    'Returns a list of random elements.\n    You can specify the size of the list.\n    You can also specify the range of numbers in the list.'
    return [randint(start, end) for _ in range(size)]

from random import randint
from ands.algorithms.recursion.is_sorted import iterative_is_sorted


def __init__(self, sorting_algorithm, in_place=True, start=randint((- 10001), (- 1)), end=randint(0, 10000)):
    self.sorting_algorithm = sorting_algorithm
    self.start = start
    self.end = end
    self.in_place = in_place

import datetime
import random
import unittest
import genetic


def shuffle_in_place(genes, first, last):
    while (first < last):
        index = random.randint(first, last)
        (genes[first], genes[index]) = (genes[index], genes[first])
        first += 1

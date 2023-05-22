import datetime
import functools
import operator
import random
import unittest
import genetic


def mutate(genes, geneset):
    if (len(genes) == len(set(genes))):
        count = random.randint(1, 4)
        while (count > 0):
            count -= 1
            (indexA, indexB) = random.sample(range(len(genes)), 2)
            (genes[indexA], genes[indexB]) = (genes[indexB], genes[indexA])
    else:
        indexA = random.randrange(0, len(genes))
        indexB = random.randrange(0, len(geneset))
        genes[indexA] = geneset[indexB]

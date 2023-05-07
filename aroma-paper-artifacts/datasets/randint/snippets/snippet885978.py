import datetime
import functools
import operator
import random
import unittest
import genetic


def mutar(genes, geneSet):
    if (len(genes) == len(set(genes))):
        cuenta = random.randint(1, 4)
        while (cuenta > 0):
            cuenta -= 1
            (índiceA, índiceB) = random.sample(range(len(genes)), 2)
            (genes[índiceA], genes[índiceB]) = (genes[índiceB], genes[índiceA])
    else:
        índiceA = random.randrange(0, len(genes))
        índiceB = random.randrange(0, len(geneSet))
        genes[índiceA] = geneSet[índiceB]

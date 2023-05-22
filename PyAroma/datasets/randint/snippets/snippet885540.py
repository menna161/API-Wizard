import datetime
from fractions import Fraction
import random
import unittest
import genetic


def mutate(genes, sortedGeneset, window, geneIndexes):
    indexes = (random.sample(geneIndexes, random.randint(1, len(genes))) if (random.randint(0, 10) == 0) else [random.choice(geneIndexes)])
    window.slide()
    while (len(indexes) > 0):
        index = indexes.pop()
        genesetIndex = sortedGeneset.index(genes[index])
        start = max(0, (genesetIndex - window.Size))
        stop = min((len(sortedGeneset) - 1), (genesetIndex + window.Size))
        genesetIndex = random.randint(start, stop)
        genes[index] = sortedGeneset[genesetIndex]

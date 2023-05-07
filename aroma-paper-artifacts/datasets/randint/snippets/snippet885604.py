import datetime
import math
import random
import unittest
from itertools import chain
import genetic


def mutate(genes, fnGetFitness):
    count = random.randint(2, len(genes))
    initialFitness = fnGetFitness(genes)
    while (count > 0):
        count -= 1
        (indexA, indexB) = random.sample(range(len(genes)), 2)
        (genes[indexA], genes[indexB]) = (genes[indexB], genes[indexA])
        fitness = fnGetFitness(genes)
        if (fitness > initialFitness):
            return

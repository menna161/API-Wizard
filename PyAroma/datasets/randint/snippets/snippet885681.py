import datetime
import random
import unittest
import genetic
import lawnmower


def crossover(parent, otherParent):
    childGenes = parent[:]
    if ((len(parent) <= 2) or (len(otherParent) < 2)):
        return childGenes
    length = random.randint(1, (len(parent) - 2))
    start = random.randrange(0, (len(parent) - length))
    childGenes[start:(start + length)] = otherParent[start:(start + length)]
    return childGenes

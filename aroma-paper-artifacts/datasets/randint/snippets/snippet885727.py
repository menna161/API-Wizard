import datetime
import random
import unittest
import circuits
import genetic


def create_gene(index, gates, sources):
    if (index < len(sources)):
        gateType = sources[index]
    else:
        gateType = random.choice(gates)
    indexA = indexB = None
    if (gateType[1].input_count() > 0):
        indexA = random.randint(0, index)
    if (gateType[1].input_count() > 1):
        indexB = random.randint(0, index)
        if (indexB == indexA):
            indexB = random.randint(0, index)
    return Node(gateType[0], indexA, indexB)

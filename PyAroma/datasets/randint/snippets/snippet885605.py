import datetime
import math
import random
import unittest
from itertools import chain
import genetic


def crossover(parentGenes, donorGenes, fnGetFitness):
    pairs = {Pair(donorGenes[0], donorGenes[(- 1)]): 0}
    for i in range((len(donorGenes) - 1)):
        pairs[Pair(donorGenes[i], donorGenes[(i + 1)])] = 0
    tempGenes = parentGenes[:]
    if (Pair(parentGenes[0], parentGenes[(- 1)]) in pairs):
        found = False
        for i in range((len(parentGenes) - 1)):
            if (Pair(parentGenes[i], parentGenes[(i + 1)]) in pairs):
                continue
            tempGenes = (parentGenes[(i + 1):] + parentGenes[:(i + 1)])
            found = True
            break
        if (not found):
            return None
    runs = [[tempGenes[0]]]
    for i in range((len(tempGenes) - 1)):
        if (Pair(tempGenes[i], tempGenes[(i + 1)]) in pairs):
            runs[(- 1)].append(tempGenes[(i + 1)])
            continue
        runs.append([tempGenes[(i + 1)]])
    initialFitness = fnGetFitness(parentGenes)
    count = random.randint(2, 20)
    runIndexes = range(len(runs))
    while (count > 0):
        count -= 1
        for i in runIndexes:
            if (len(runs[i]) == 1):
                continue
            if (random.randint(0, len(runs)) == 0):
                runs[i] = [n for n in reversed(runs[i])]
        (indexA, indexB) = random.sample(runIndexes, 2)
        (runs[indexA], runs[indexB]) = (runs[indexB], runs[indexA])
        childGenes = list(chain.from_iterable(runs))
        if (fnGetFitness(childGenes) > initialFitness):
            return childGenes
    return childGenes

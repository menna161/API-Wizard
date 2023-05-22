import datetime
import random
import unittest
import genetic
import lawnmower


def mutate(genes, geneSet, minGenes, maxGenes, fnGetFitness, maxRounds):
    count = random.randint(1, maxRounds)
    initialFitness = fnGetFitness(genes)
    while (count > 0):
        count -= 1
        if (fnGetFitness(genes) > initialFitness):
            return
        adding = ((len(genes) == 0) or ((len(genes) < maxGenes) and (random.randint(0, 5) == 0)))
        if adding:
            genes.append(random.choice(geneSet)())
            continue
        removing = ((len(genes) > minGenes) and (random.randint(0, 50) == 0))
        if removing:
            index = random.randrange(0, len(genes))
            del genes[index]
            continue
        index = random.randrange(0, len(genes))
        genes[index] = random.choice(geneSet)()

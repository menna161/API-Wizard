import datetime
import random
import unittest
import circuits
import genetic


def mutate(childGenes, fnCreateGene, fnGetFitness, sourceCount):
    count = random.randint(1, 5)
    initialFitness = fnGetFitness(childGenes)
    while (count > 0):
        count -= 1
        indexesUsed = [i for i in nodes_to_circuit(childGenes)[1] if (i >= sourceCount)]
        if (len(indexesUsed) == 0):
            return
        index = random.choice(indexesUsed)
        childGenes[index] = fnCreateGene(index)
        if (fnGetFitness(childGenes) > initialFitness):
            return

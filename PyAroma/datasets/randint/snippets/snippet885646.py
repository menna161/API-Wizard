import datetime
import random
import unittest
import genetic


def mutate(genes, numbers, operations, minNumbers, maxNumbers, fnGetFitness):
    count = random.randint(1, 10)
    initialFitness = fnGetFitness(genes)
    while (count > 0):
        count -= 1
        if (fnGetFitness(genes) > initialFitness):
            return
        numberCount = ((1 + len(genes)) / 2)
        adding = ((numberCount < maxNumbers) and (random.randint(0, 100) == 0))
        if adding:
            genes.append(random.choice(operations))
            genes.append(random.choice(numbers))
            continue
        removing = ((numberCount > minNumbers) and (random.randint(0, 20) == 0))
        if removing:
            index = random.randrange(0, (len(genes) - 1))
            del genes[index]
            del genes[index]
            continue
        index = random.randrange(0, len(genes))
        genes[index] = (random.choice(operations) if ((index & 1) == 1) else random.choice(numbers))

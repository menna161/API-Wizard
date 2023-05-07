import datetime
import random
import unittest
import genetic


def generate(self, diagonalSize, maxAge):
    nSquared = (diagonalSize * diagonalSize)
    geneset = [i for i in range(1, (nSquared + 1))]
    expectedSum = ((diagonalSize * (nSquared + 1)) / 2)

    def fnGetFitness(genes):
        return get_fitness(genes, diagonalSize, expectedSum)

    def fnDisplay(candidate):
        display(candidate, diagonalSize, startTime)
    geneIndexes = [i for i in range(0, len(geneset))]

    def fnMutate(genes):
        mutate(genes, geneIndexes)

    def fnCustomCreate():
        return random.sample(geneset, len(geneset))
    optimalValue = Fitness(0)
    startTime = datetime.datetime.now()
    best = genetic.get_best(fnGetFitness, nSquared, optimalValue, geneset, fnDisplay, fnMutate, fnCustomCreate, maxAge)
    self.assertTrue((not (optimalValue > best.Fitness)))

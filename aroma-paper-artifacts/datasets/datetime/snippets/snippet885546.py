import datetime
from fractions import Fraction
import random
import unittest
import genetic


def solve_unknowns(self, numUnknowns, geneset, equations, fnGenesToInputs):
    startTime = datetime.datetime.now()
    maxAge = 50
    window = Window(max(1, int((len(geneset) / (2 * maxAge)))), max(1, int((len(geneset) / 3))), int((len(geneset) / 2)))
    geneIndexes = [i for i in range(numUnknowns)]
    sortedGeneset = sorted(geneset)

    def fnDisplay(candidate):
        display(candidate, startTime, fnGenesToInputs)

    def fnGetFitness(genes):
        return get_fitness(genes, equations)

    def fnMutate(genes):
        mutate(genes, sortedGeneset, window, geneIndexes)
    optimalFitness = Fitness(0)
    best = genetic.get_best(fnGetFitness, numUnknowns, optimalFitness, geneset, fnDisplay, fnMutate, maxAge=maxAge)
    self.assertTrue((not (optimalFitness > best.Fitness)))

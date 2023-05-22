import datetime
import math
import random
import unittest
from itertools import chain
import genetic


def solve(self, idToLocationLookup, optimalSequence):
    geneset = [i for i in idToLocationLookup.keys()]

    def fnCreate():
        return random.sample(geneset, len(geneset))

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes, idToLocationLookup)

    def fnMutate(genes):
        mutate(genes, fnGetFitness)

    def fnCrossover(parent, donor):
        return crossover(parent, donor, fnGetFitness)
    optimalFitness = fnGetFitness(optimalSequence)
    startTime = datetime.datetime.now()
    best = genetic.get_best(fnGetFitness, None, optimalFitness, None, fnDisplay, fnMutate, fnCreate, maxAge=500, poolSize=25, crossover=fnCrossover)
    self.assertTrue((not (optimalFitness > best.Fitness)))

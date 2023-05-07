import datetime
import functools
import operator
import random
import unittest
import genetic


def test(self):
    geneset = [(i + 1) for i in range(10)]
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes)

    def fnMutate(genes):
        mutate(genes, geneset)
    optimalFitness = Fitness(36, 360, 0)
    best = genetic.get_best(fnGetFitness, 10, optimalFitness, geneset, fnDisplay, custom_mutate=fnMutate)
    self.assertTrue((not (optimalFitness > best.Fitness)))

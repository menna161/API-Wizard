import datetime
import unittest
import genetic


def test(self, length=100):
    geneset = [0, 1]
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes)
    optimalFitness = length
    best = genetic.get_best(fnGetFitness, length, optimalFitness, geneset, fnDisplay)
    self.assertEqual(best.Fitness, optimalFitness)

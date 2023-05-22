import datetime
import unittest
import genetic


def test(self, size=8):
    geneset = [i for i in range(size)]
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime, size)

    def fnGetFitness(genes):
        return get_fitness(genes, size)
    optimalFitness = Fitness(0)
    best = genetic.get_best(fnGetFitness, (2 * size), optimalFitness, geneset, fnDisplay)
    self.assertTrue((not (optimalFitness > best.Fitness)))

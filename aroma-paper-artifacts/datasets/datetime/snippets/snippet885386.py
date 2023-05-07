import datetime
import unittest
import genetic


def sort_numbers(self, totalNumbers):
    geneset = [i for i in range(100)]
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes)
    optimalFitness = Fitness(totalNumbers, 0)
    best = genetic.get_best(fnGetFitness, totalNumbers, optimalFitness, geneset, fnDisplay)
    self.assertTrue((not (optimalFitness > best.Fitness)))

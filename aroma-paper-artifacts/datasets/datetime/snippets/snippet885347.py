import datetime
import random
import unittest
import genetic


def guess_password(self, target):
    startTime = datetime.datetime.now()

    def fnGetFitness(genes):
        return get_fitness(genes, target)

    def fnDisplay(candidate):
        display(candidate, startTime)
    optimalFitness = len(target)
    best = genetic.get_best(fnGetFitness, len(target), optimalFitness, self.geneset, fnDisplay)
    self.assertEqual(best.Genes, target)

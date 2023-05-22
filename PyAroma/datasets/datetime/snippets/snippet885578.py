import datetime
import random
import unittest
import genetic


def test(self):
    geneset = [i for i in range(1, (9 + 1))]
    startTime = datetime.datetime.now()
    optimalValue = 100

    def fnDisplay(candidate):
        display(candidate, startTime)
    validationRules = build_validation_rules()

    def fnGetFitness(genes):
        return get_fitness(genes, validationRules)

    def fnCreate():
        return random.sample((geneset * 9), 81)

    def fnMutate(genes):
        mutate(genes, validationRules)
    best = genetic.get_best(fnGetFitness, None, optimalValue, None, fnDisplay, fnMutate, fnCreate, maxAge=50)
    self.assertEqual(best.Fitness, optimalValue)

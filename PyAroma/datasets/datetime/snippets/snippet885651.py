import datetime
import random
import unittest
import genetic


def solve(self, operations, prioritizedOperations, optimalLengthSolution):
    numbers = [1, 2, 3, 4, 5, 6, 7]
    expectedTotal = evaluate(optimalLengthSolution, prioritizedOperations)
    minNumbers = ((1 + len(optimalLengthSolution)) / 2)
    maxNumbers = (6 * minNumbers)
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnEvaluate(genes):
        return evaluate(genes, prioritizedOperations)

    def fnGetFitness(genes):
        return get_fitness(genes, expectedTotal, fnEvaluate)

    def fnCreate():
        return create(numbers, operations, minNumbers, maxNumbers)

    def fnMutate(child):
        mutate(child, numbers, operations, minNumbers, maxNumbers, fnGetFitness)
    optimalFitness = fnGetFitness(optimalLengthSolution)
    best = genetic.get_best(fnGetFitness, None, optimalFitness, None, fnDisplay, fnMutate, fnCreate, maxAge=50)
    self.assertTrue((not (optimalFitness > best.Fitness)))

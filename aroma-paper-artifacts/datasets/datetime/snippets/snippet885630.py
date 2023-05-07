import datetime
import math
import random
import sys
import time
import unittest
import genetic


def test(self, bitValues=[512, 256, 128, 64, 32, 16, 8, 4, 2, 1], maxSeconds=None):
    geneset = [i for i in range(2)]
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime, bitValues)

    def fnGetFitness(genes):
        return get_fitness(genes, bitValues)
    optimalFitness = 3.14159

    def fnMutate(genes):
        mutate(genes, len(bitValues))
    length = (2 * len(bitValues))
    best = genetic.get_best(fnGetFitness, length, optimalFitness, geneset, fnDisplay, fnMutate, maxAge=250, maxSeconds=maxSeconds)
    return (optimalFitness <= best.Fitness)

import datetime
import random
import sys
import unittest
import genetic


def fill_knapsack(self, items, maxWeight, maxVolume, optimalFitness):
    startTime = datetime.datetime.now()
    window = Window(1, max(1, int((len(items) / 3))), int((len(items) / 2)))
    sortedItems = sorted(items, key=(lambda item: item.Value))

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes)

    def fnCreate():
        return create(items, maxWeight, maxVolume)

    def fnMutate(genes):
        mutate(genes, sortedItems, maxWeight, maxVolume, window)
    best = genetic.get_best(fnGetFitness, None, optimalFitness, None, fnDisplay, fnMutate, fnCreate, maxAge=50)
    self.assertTrue((not (optimalFitness > best.Fitness)))

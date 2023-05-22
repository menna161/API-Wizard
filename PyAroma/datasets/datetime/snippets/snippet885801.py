import datetime
import random
import re
import unittest
from functools import partial
import genetic


def find_regex(self, wanted, unwanted, expectedLength, customOperators=None):
    startTime = datetime.datetime.now()
    textGenes = (wanted | set((c for w in wanted for c in w)))
    fullGeneset = [i for i in (allMetas | textGenes)]

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes, wanted, unwanted)
    mutationRoundCounts = [1]
    mutationOperators = [partial(mutate_add, geneset=fullGeneset), partial(mutate_replace, geneset=fullGeneset), mutate_remove, mutate_swap, mutate_move]
    if (customOperators is not None):
        mutationOperators.extend(customOperators)

    def fnMutate(genes):
        mutate(genes, fnGetFitness, mutationOperators, mutationRoundCounts)
    optimalFitness = Fitness(len(wanted), len(wanted), 0, expectedLength)
    best = genetic.get_best(fnGetFitness, max((len(i) for i in textGenes)), optimalFitness, fullGeneset, fnDisplay, fnMutate, poolSize=10)
    self.assertTrue((not (optimalFitness > best.Fitness)))
    for info in regexErrorsSeen.values():
        print('')
        print(info[0])
        print(info[1])
        print(info[2])

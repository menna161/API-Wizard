import datetime
import random
import unittest
from functools import partial
import genetic


def test_perfect_knowledge(self):
    minGenes = 10
    maxGenes = 20
    geneset = create_geneset()
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes)
    mutationRoundCounts = [1]
    mutationOperators = [partial(mutate_add, geneset=geneset), partial(mutate_replace, geneset=geneset), mutate_remove, mutate_swap_adjacent, mutate_move]

    def fnMutate(genes):
        mutate(genes, fnGetFitness, mutationOperators, mutationRoundCounts)

    def fnCrossover(parent, donor):
        child = (parent[0:int((len(parent) / 2))] + donor[int((len(donor) / 2)):])
        fnMutate(child)
        return child

    def fnCreate():
        return random.sample(geneset, random.randrange(minGenes, maxGenes))
    optimalFitness = Fitness(620, 120, 0, 11)
    best = genetic.get_best(fnGetFitness, minGenes, optimalFitness, None, fnDisplay, fnMutate, fnCreate, maxAge=500, poolSize=20, crossover=fnCrossover)
    self.assertTrue((not (optimalFitness > best.Fitness)))

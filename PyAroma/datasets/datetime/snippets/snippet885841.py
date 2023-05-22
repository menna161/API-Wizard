import datetime
import random
import unittest
from functools import partial
import genetic


def test_tornament(self):
    minGenes = 10
    maxGenes = 20
    geneset = create_geneset()
    startTime = datetime.datetime.now()

    def fnDisplay(genes, wins, ties, losses, generation):
        print('-- generation {} --'.format(generation))
        display(genetic.Chromosome(genes, Fitness(wins, ties, losses, len(genes)), None), startTime)
    mutationRoundCounts = [1]
    mutationOperators = [partial(mutate_add, geneset=geneset), partial(mutate_replace, geneset=geneset), mutate_remove, mutate_swap_adjacent, mutate_move]

    def fnMutate(genes):
        mutate(genes, (lambda x: 0), mutationOperators, mutationRoundCounts)

    def fnCrossover(parent, donor):
        child = (parent[0:int((len(parent) / 2))] + donor[int((len(donor) / 2)):])
        fnMutate(child)
        return child

    def fnCreate():
        return random.sample(geneset, random.randrange(minGenes, maxGenes))

    def fnSortKey(genes, wins, ties, losses):
        return ((((- 1000) * losses) - ties) + (1 / len(genes)))
    genetic.tournament(fnCreate, fnCrossover, play1on1, fnDisplay, fnSortKey, 13)

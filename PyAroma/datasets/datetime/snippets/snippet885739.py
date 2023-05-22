import datetime
import random
import unittest
import circuits
import genetic


def find_circuit(self, rules, expectedLength):
    startTime = datetime.datetime.now()

    def fnDisplay(candidate, length=None):
        if (length is not None):
            print('-- distinct nodes in circuit:', len(nodes_to_circuit(candidate.Genes)[1]))
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes, rules, self.inputs)

    def fnCreateGene(index):
        return create_gene(index, self.gates, self.sources)

    def fnMutate(genes):
        mutate(genes, fnCreateGene, fnGetFitness, len(self.sources))
    maxLength = 50

    def fnCreate():
        return [fnCreateGene(i) for i in range(maxLength)]

    def fnOptimizationFunction(variableLength):
        nonlocal maxLength
        maxLength = variableLength
        return genetic.get_best(fnGetFitness, None, len(rules), None, fnDisplay, fnMutate, fnCreate, poolSize=3, maxSeconds=30)

    def fnIsImprovement(currentBest, child):
        return ((child.Fitness == len(rules)) and (len(nodes_to_circuit(child.Genes)[1]) < len(nodes_to_circuit(currentBest.Genes)[1])))

    def fnIsOptimal(child):
        return ((child.Fitness == len(rules)) and (len(nodes_to_circuit(child.Genes)[1]) <= expectedLength))

    def fnGetNextFeatureValue(currentBest):
        return len(nodes_to_circuit(currentBest.Genes)[1])
    best = genetic.hill_climbing(fnOptimizationFunction, fnIsImprovement, fnIsOptimal, fnGetNextFeatureValue, fnDisplay, maxLength)
    self.assertTrue((best.Fitness == len(rules)))
    self.assertFalse((len(nodes_to_circuit(best.Genes)[1]) > expectedLength))

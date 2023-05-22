import datetime
import unittest
import genetic


def color(self, file, colors):
    (rules, nodes) = load_data(file)
    optimalValue = len(rules)
    colorLookup = {color[0]: color for color in colors}
    geneset = list(colorLookup.keys())
    startTime = datetime.datetime.now()
    nodeIndexLookup = {key: index for (index, key) in enumerate(sorted(nodes))}

    def fnDisplay(candidate):
        display(candidate, startTime)

    def fnGetFitness(genes):
        return get_fitness(genes, rules, nodeIndexLookup)
    best = genetic.get_best(fnGetFitness, len(nodes), optimalValue, geneset, fnDisplay)
    self.assertTrue((not (optimalValue > best.Fitness)))
    keys = sorted(nodes)
    for index in range(len(nodes)):
        print(((keys[index] + ' is ') + colorLookup[best.Genes[index]]))

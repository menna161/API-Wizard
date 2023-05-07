import numpy as np
import itertools
from .ind import Ind, getLayer, getNodeOrder


def recombine(self, species, innov, gen):
    ' Creates next generation of child solutions from a species\n\n  Procedure:\n    ) Sort all individuals by rank\n    ) Eliminate lower percentage of individuals from breeding pool\n    ) Pass upper percentage of individuals to child population unchanged\n    ) Select parents by tournament selection\n    ) Produce new population through crossover and mutation\n\n  Args:\n      species - (Species) -\n        .members    - [Ind] - parent population\n        .nOffspring - (int) - number of children to produce\n      innov   - (np_array)  - innovation record\n                [5 X nUniqueGenes]\n                [0,:] == Innovation Number\n                [1,:] == Source\n                [2,:] == Destination\n                [3,:] == New Node?\n                [4,:] == Generation evolved\n      gen     - (int) - current generation\n\n  Returns:\n      children - [Ind]      - newly created population\n      innov   - (np_array)  - updated innovation record\n\n  '
    p = self.p
    nOffspring = int(species.nOffspring)
    pop = species.members
    children = []
    pop.sort(key=(lambda x: x.rank))
    numberToCull = int(np.floor((p['select_cullRatio'] * len(pop))))
    if (numberToCull > 0):
        pop[(- numberToCull):] = []
    nElites = int(np.floor((len(pop) * p['select_eliteRatio'])))
    for i in range(nElites):
        children.append(pop[i])
        nOffspring -= 1
    parentA = np.random.randint(len(pop), size=(nOffspring, p['select_tournSize']))
    parentB = np.random.randint(len(pop), size=(nOffspring, p['select_tournSize']))
    parents = np.vstack((np.min(parentA, 1), np.min(parentB, 1)))
    parents = np.sort(parents, axis=0)
    for i in range(nOffspring):
        if (np.random.rand() > p['prob_crossover']):
            child = Ind(pop[parents[(0, i)]].conn, pop[parents[(0, i)]].node)
        else:
            child = self.crossover(pop[parents[(0, i)]], pop[parents[(1, i)]])
        (child, innov) = self.topoMutate(child, innov, gen)
        child.express()
        children.append(child)
    return (children, innov)

from random import random, randint
from copy import deepcopy
from model.root.root_algo import RootAlgo


def _create_neigh_bee__(self, individual=None, patch_size=None):
    t1 = randint(0, (len(individual) - 1))
    new_bee = deepcopy(individual)
    new_bee[t1] = ((individual[t1] + (random() * patch_size)) if (random() < 0.5) else (individual[t1] - (random() * patch_size)))
    if (random() < 0.5):
        new_bee[t1] = (individual[t1] + (random() * patch_size))
        if (new_bee[t1] > self.domain_range[1]):
            new_bee[t1] = self.domain_range[1]
    else:
        new_bee[t1] = (individual[t1] - (random() * patch_size))
        if (new_bee[t1] < self.domain_range[0]):
            new_bee[t1] = self.domain_range[0]
    return [new_bee, self._fitness_model__(new_bee)]

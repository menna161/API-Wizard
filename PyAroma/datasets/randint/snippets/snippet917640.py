import numpy as np
from copy import deepcopy
from model.root.root_algo import RootAlgo


def _mutation__(self, p0, p1, p2, p3):
    cut_point = np.random.randint(1, (self.problem_size - 1))
    sample = []
    for i in range(self.problem_size):
        if ((i == cut_point) or (np.random.uniform() < self.crossover_rate)):
            v = (p1[i] + (self.weighting_factor * (p2[i] - p3[i])))
            v = (self.domain_range[0] if (v < self.domain_range[0]) else v)
            v = (self.domain_range[1] if (v > self.domain_range[1]) else v)
            sample.append(v)
        else:
            sample.append(p0[i])
    return sample

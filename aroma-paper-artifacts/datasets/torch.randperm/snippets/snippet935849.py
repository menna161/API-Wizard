from __future__ import division
import math
import torch
import numpy as np
from mmcv.runner.utils import get_dist_info
from torch.utils.data import Sampler
from torch.utils.data import DistributedSampler as _DistributedSampler


def __iter__(self):
    g = torch.Generator()
    g.manual_seed(self.epoch)
    indices = []
    for (i, size) in enumerate(self.group_sizes):
        if (size > 0):
            indice = np.where((self.flag == i))[0]
            assert (len(indice) == size)
            indice = indice[list(torch.randperm(int(size), generator=g))].tolist()
            extra = (((int(math.ceil((((size * 1.0) / self.samples_per_gpu) / self.num_replicas))) * self.samples_per_gpu) * self.num_replicas) - len(indice))
            indice += indice[:extra]
            indices += indice
    assert (len(indices) == self.total_size)
    indices = [indices[j] for i in list(torch.randperm((len(indices) // self.samples_per_gpu), generator=g)) for j in range((i * self.samples_per_gpu), ((i + 1) * self.samples_per_gpu))]
    offset = (self.num_samples * self.rank)
    indices = indices[offset:(offset + self.num_samples)]
    assert (len(indices) == self.num_samples)
    return iter(indices)

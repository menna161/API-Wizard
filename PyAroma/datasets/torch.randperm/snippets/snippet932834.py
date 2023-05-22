from __future__ import absolute_import
from collections import defaultdict
import numpy as np
import torch
from torch.utils.data.sampler import Sampler, SequentialSampler, RandomSampler, SubsetRandomSampler, WeightedRandomSampler


def __iter__(self):
    indices = torch.randperm(self.num_samples)
    ret = []
    for i in indices:
        pid = self.pids[i]
        t = self.index_dic[pid]
        if (len(t) >= self.num_instances):
            t = np.random.choice(t, size=self.num_instances, replace=False)
        else:
            t = np.random.choice(t, size=self.num_instances, replace=True)
        ret.extend(t)
    return iter(ret)

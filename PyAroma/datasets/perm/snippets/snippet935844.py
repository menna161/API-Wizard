from __future__ import division
import math
import torch
import numpy as np
from mmcv.runner.utils import get_dist_info
from torch.utils.data import Sampler
from torch.utils.data import DistributedSampler as _DistributedSampler


def __iter__(self):
    if self.shuffle:
        g = torch.Generator()
        g.manual_seed(self.epoch)
        indices = torch.randperm(len(self.dataset), generator=g).tolist()
    else:
        indices = torch.arange(len(self.dataset)).tolist()
    indices += indices[:(self.total_size - len(indices))]
    assert (len(indices) == self.total_size)
    indices = indices[self.rank:self.total_size:self.num_replicas]
    assert (len(indices) == self.num_samples)
    return iter(indices)

import os
import logging
import shutil
import torch
from datetime import datetime
from torch.utils.data.sampler import Sampler
import torch.distributed as dist
import math
import numpy as np
import torch


def __iter__(self):
    g = torch.Generator()
    g.manual_seed(self.epoch)
    indices = list(torch.randperm(len(self.dataset), generator=g))
    if self.round_up:
        indices += indices[:(self.total_size - len(indices))]
    assert (len(indices) == self.total_size)
    offset = (self.num_samples * self.rank)
    indices = indices[offset:(offset + self.num_samples)]
    if (self.round_up or ((not self.round_up) and (self.rank < (self.world_size - 1)))):
        assert (len(indices) == self.num_samples)
    return iter(indices)

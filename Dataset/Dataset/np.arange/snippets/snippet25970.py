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


def gen_new_list(self):
    np.random.seed(0)
    all_size = (self.total_size * self.world_size)
    indices = np.arange(len(self.dataset))
    np.random.shuffle(indices)
    indices = indices[:all_size]
    num_repeat = (((all_size - 1) // indices.shape[0]) + 1)
    indices = np.tile(indices, num_repeat)
    indices = indices[:all_size]
    np.random.shuffle(indices)
    beg = (self.total_size * self.rank)
    indices = indices[beg:(beg + self.total_size)]
    assert (len(indices) == self.total_size)
    return indices

import torch as th
from torch.utils.data.sampler import Sampler
import numpy as np


def __iter__(self):
    idx = np.arange(self.n_sample)
    if ((self.n_sample % self.seq_len) != 0):
        idx = self._pad_ind(idx)
    idx = np.reshape(idx, ((- 1), self.seq_len))
    np.random.shuffle(idx)
    idx = np.reshape(idx, (- 1))
    return iter(idx.astype(int))

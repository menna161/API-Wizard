import numpy as np
import torch
import math
from . import data_utils, FairseqDataset


def ordered_indices(self):
    'Return an ordered list of indices. Batches will be constructed based\n        on this order.'
    if self.shuffle:
        indices = np.random.permutation(len(self))
    else:
        indices = np.arange(len(self))
    return indices[np.argsort(self.sizes[indices], kind='mergesort')]

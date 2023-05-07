import logging
import numpy as np
from . import BaseWrapperDataset


def ordered_indices(self):
    'Return an ordered list of indices. Batches will be constructed based\n        on this order.'
    if self.shuffle:
        order = [np.random.permutation(len(self))]
    else:
        order = [np.arange(len(self))]
    order.append(self.sizes)
    return np.lexsort(order)

import numpy as np
from . import BaseWrapperDataset, plasma_utils


def ordered_indices(self):
    if self.batch_by_size:
        order = [np.arange(len(self)), self.sizes]
        return np.lexsort(order)
    else:
        return np.arange(len(self))

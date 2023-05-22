from collections import OrderedDict
import numpy as np
from . import FairseqDataset


def ordered_indices(self):
    'Ordered indices for batching.'
    if (self._ordered_indices is None):
        self._ordered_indices = OrderedDict([(key, dataset.ordered_indices()) for (key, dataset) in self.datasets.items()])
    return np.arange(len(self))

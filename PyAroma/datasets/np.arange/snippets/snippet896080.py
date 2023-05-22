from collections import OrderedDict
from typing import Callable, Dict, List
import numpy as np
from . import FairseqDataset


def ordered_indices(self):
    "\n        Ordered indices for batching. Here we call the underlying\n        dataset's ordered_indices() so that we get the same random ordering\n        as we would have from using the underlying dataset directly.\n        "
    if (self._ordered_indices is None):
        self._ordered_indices = OrderedDict([(key, dataset.ordered_indices()) for (key, dataset) in self.datasets.items()])
    return np.arange(len(self))

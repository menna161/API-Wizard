import numpy as np
import torch.utils.data


def ordered_indices(self):
    'Return an ordered list of indices. Batches will be constructed based\n        on this order.'
    return np.arange(len(self))

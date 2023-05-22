import numpy as np
import torch.nn.functional as F
from fairseq.data import BaseWrapperDataset


def __init__(self, dataset, sizes, num_buckets, pad_idx, left_pad):
    super().__init__(dataset)
    self.pad_idx = pad_idx
    self.left_pad = left_pad
    assert (num_buckets > 0)
    self.buckets = np.unique(np.percentile(sizes, np.linspace(0, 100, (num_buckets + 1)), interpolation='lower')[1:])

    def get_bucketed_sizes(orig_sizes, buckets):
        sizes = np.copy(orig_sizes)
        assert (np.min(sizes) >= 0)
        start_val = (- 1)
        for end_val in buckets:
            mask = ((sizes > start_val) & (sizes <= end_val))
            sizes[mask] = end_val
            start_val = end_val
        return sizes
    self._bucketed_sizes = get_bucketed_sizes(sizes, self.buckets)

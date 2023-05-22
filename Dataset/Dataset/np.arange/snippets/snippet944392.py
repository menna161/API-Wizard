import logging
import numpy as np
import torch
from fairseq.data import data_utils, FairseqDataset
from fairseq.data import BucketPadLengthDataset


def ordered_indices(self):
    'Return an ordered list of indices. Batches will be constructed based\n        on this order.'
    if self.shuffle:
        indices = np.random.permutation(len(self))
    else:
        indices = np.arange(len(self))
    if (self.buckets is None):
        if (self.tgt_sizes is not None):
            indices = indices[np.argsort(self.tgt_sizes[indices], kind='mergesort')]
        return indices[np.argsort(self.src_sizes[indices], kind='mergesort')]
    else:
        return indices[np.argsort(self.bucketed_num_tokens[indices], kind='mergesort')]

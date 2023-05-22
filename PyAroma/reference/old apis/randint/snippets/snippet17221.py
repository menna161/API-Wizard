import sys
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from . import BaseFairseqModel, register_model, register_model_architecture


def sample_negatives(self, y):
    (bsz, fsz, tsz) = y.shape
    y = y.transpose(0, 1)
    y = y.contiguous().view(fsz, (- 1))
    if self.cross_sample_negatives:
        high = (tsz * bsz)
        assert (self.sample_distance is None), 'sample distance is not supported with cross sampling'
    else:
        high = (tsz if (self.sample_distance is None) else min(tsz, self.sample_distance))
    neg_idxs = torch.randint(low=0, high=high, size=(bsz, (self.n_negatives * tsz)))
    if ((self.sample_distance is not None) and (self.sample_distance < tsz)):
        neg_idxs += torch.cat([torch.arange(start=1, end=(tsz - self.sample_distance), device=neg_idxs.device, dtype=neg_idxs.dtype), torch.arange(start=(tsz - self.sample_distance), end=((tsz - (self.sample_distance * 2)) - 1), step=(- 1), device=neg_idxs.device, dtype=neg_idxs.dtype)])
    if (not self.cross_sample_negatives):
        for i in range(1, bsz):
            neg_idxs[i] += (i * high)
    negs = y[(..., neg_idxs.view((- 1)))]
    negs = negs.view(fsz, bsz, self.n_negatives, tsz).permute(2, 1, 0, 3)
    return negs

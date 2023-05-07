import logging
import math
import sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from fairseq.models import BaseFairseqModel, register_model, register_model_architecture
from fairseq.modules import Fp32GroupNorm, Fp32LayerNorm, GumbelVectorQuantizer, KmeansVectorQuantizer
from fairseq.utils import buffered_arange


def sample_negatives(self, y):
    (bsz, fsz, tsz) = y.shape
    y = y.transpose(0, 1)
    y = y.contiguous().view(fsz, (- 1))
    cross_high = (tsz * bsz)
    high = (tsz if (self.sample_distance is None) else min(tsz, self.sample_distance))
    assert (high > 1)
    neg_idxs = torch.randint(low=0, high=high, size=(bsz, (self.n_negatives * tsz)))
    with torch.no_grad():
        if (self.n_negatives > 0):
            tszs = buffered_arange(tsz).unsqueeze((- 1)).expand((- 1), self.n_negatives).flatten()
            neg_idxs = torch.randint(low=0, high=(high - 1), size=(bsz, (self.n_negatives * tsz)))
            neg_idxs[(neg_idxs >= tszs)] += 1
        if (self.cross_sample_negatives > 0):
            tszs = buffered_arange(tsz).unsqueeze((- 1)).expand((- 1), self.cross_sample_negatives).flatten()
            cross_neg_idxs = torch.randint(low=0, high=(cross_high - 1), size=(bsz, (self.cross_sample_negatives * tsz)))
            cross_neg_idxs[(cross_neg_idxs >= tszs)] += 1
    if (self.n_negatives > 0):
        for i in range(1, bsz):
            neg_idxs[i] += (i * high)
    else:
        neg_idxs = cross_neg_idxs
    if ((self.cross_sample_negatives > 0) and (self.n_negatives > 0)):
        neg_idxs = torch.cat([neg_idxs, cross_neg_idxs], dim=1)
    negs = y[(..., neg_idxs.view((- 1)))]
    negs = negs.view(fsz, bsz, (self.n_negatives + self.cross_sample_negatives), tsz).permute(2, 1, 0, 3)
    return negs

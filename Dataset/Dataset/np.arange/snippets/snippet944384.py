import logging
import numpy as np
import torch
from fairseq.data import data_utils, FairseqDataset
from fairseq.data import BucketPadLengthDataset


def compute_alignment_weights(alignments):
    '\n        Given a tensor of shape [:, 2] containing the source-target indices\n        corresponding to the alignments, a weight vector containing the\n        inverse frequency of each target index is computed.\n        For e.g. if alignments = [[5, 7], [2, 3], [1, 3], [4, 2]], then\n        a tensor containing [1., 0.5, 0.5, 1] should be returned (since target\n        index 3 is repeated twice)\n        '
    align_tgt = alignments[(:, 1)]
    (_, align_tgt_i, align_tgt_c) = torch.unique(align_tgt, return_inverse=True, return_counts=True)
    align_weights = align_tgt_c[align_tgt_i[np.arange(len(align_tgt))]]
    return (1.0 / align_weights.float())

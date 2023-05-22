from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from tqdm import tqdm
import mxnet as mx
import numpy as np


def get_metric_at_ranks(self, distmat, labels, ranks):
    np.fill_diagonal(distmat, 100000.0)
    recall_at_ranks = []
    recall_dict = {k: 0 for k in ranks}
    max_k = np.max(ranks)
    arange_idx = np.arange(len(distmat))[(:, None)]
    part_idx = np.argpartition(distmat, max_k, axis=1)[(:, :max_k)]
    part_mat = distmat[(arange_idx, part_idx)]
    sorted_idx = np.argsort(part_mat, axis=1)
    top_k_idx = part_idx[(arange_idx, sorted_idx)]
    for (top_k, gt) in zip(top_k_idx, labels):
        top_k_labels = labels[top_k]
        for r in ranks:
            if (gt in top_k_labels[:r]):
                recall_dict[r] += 1
    for r in ranks:
        recall_at_ranks.append((recall_dict[r] / len(distmat)))
    return recall_at_ranks

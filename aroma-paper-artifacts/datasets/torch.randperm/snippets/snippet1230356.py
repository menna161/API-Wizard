import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
import numpy as np
from data.base import sample_partitions


def sample_idxs(idx_to_class, B, N, K, rand_N=True, rand_K=True):
    N = (np.random.randint(int((0.3 * N)), N) if rand_N else N)
    labels = sample_partitions(B, N, K, rand_K=rand_K, device='cpu', alpha=5.0)
    idxs = torch.zeros(B, N, dtype=torch.long)
    abs_labels = torch.zeros(B, N, dtype=torch.long)
    classes_pool = list(idx_to_class.keys())
    for b in range(B):
        classes = np.random.permutation(classes_pool)[:K]
        for (i, c) in enumerate(classes):
            if ((labels[b] == i).int().sum() > 0):
                members = (labels[b] == i).nonzero().view((- 1))
                idx_pool = idx_to_class[c]
                idx_pool = idx_pool[torch.randperm(len(idx_pool))]
                n_repeat = ((len(members) // len(idx_pool)) + 1)
                idxs[(b, members)] = torch.cat(([idx_pool] * n_repeat))[:len(members)]
                abs_labels[(b, members)] = np.long(c)
    oh_labels = F.one_hot(labels, K)
    return {'idxs': idxs, 'oh_labels': oh_labels, 'abs_labels': abs_labels}

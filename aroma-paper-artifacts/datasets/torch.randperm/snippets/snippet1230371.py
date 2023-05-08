import torch
import torch.nn.functional as F
import numpy as np
from torch.utils.data import DataLoader
from torchvision.datasets import EMNIST
import torchvision.transforms as tvt
from data.base import sample_partitions
from utils.paths import datasets_path
import matplotlib.pyplot as plt
from torchvision.utils import make_grid


def sample_idxs(idx_to_class, B, N, K, rand_N=True, rand_K=True, train=True):
    N = (np.random.randint(int((0.3 * N)), N) if rand_N else N)
    labels = sample_partitions(B, N, K, rand_K=rand_K, device='cpu', alpha=5.0)
    idxs = torch.zeros(B, N, NUM_DIGITS, dtype=torch.long)
    abs_labels = torch.zeros(B, N, dtype=torch.long)
    cluster_pool = (np.arange((NUM_CLUSTERS // 2)) if train else np.arange((NUM_CLUSTERS // 2), NUM_CLUSTERS))
    for b in range(B):
        clusters = np.random.permutation(cluster_pool)[:K]
        for (i, cls) in enumerate(clusters):
            if ((labels[b] == i).int().sum() > 0):
                members = (labels[b] == i).nonzero().view((- 1))
                abs_labels[(b, members)] = np.long(cls)
                classes = decode(cls)
                for (d, c) in enumerate(classes):
                    idx_pool = idx_to_class[c]
                    idx_pool = idx_pool[torch.randperm(len(idx_pool))]
                    n_repeat = ((len(members) // len(idx_pool)) + 1)
                    idxs[(b, members, d)] = torch.cat(([idx_pool] * n_repeat))[:len(members)]
    idxs = idxs.view(B, (- 1))
    oh_labels = F.one_hot(labels, K)
    return {'idxs': idxs, 'oh_labels': oh_labels, 'abs_labels': abs_labels}

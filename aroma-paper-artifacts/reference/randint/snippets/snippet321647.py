import numpy as np
import torch
import torch.utils.data as data


def sample_random_negatives(self, idx, num_to_sample):
    idx_sample = np.random.randint(0, len(idx), size=num_to_sample)
    idx_values = idx[idx_sample]
    return (idx_values, idx_sample)

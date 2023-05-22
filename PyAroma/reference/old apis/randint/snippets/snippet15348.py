import numpy as np
import torch
import math
from . import data_utils, FairseqDataset


def add_insertion_noise(self, tokens, p):
    if (p == 0.0):
        return tokens
    num_tokens = len(tokens)
    n = int(math.ceil((num_tokens * p)))
    noise_indices = (torch.randperm(((num_tokens + n) - 2))[:n] + 1)
    noise_mask = torch.zeros(size=((num_tokens + n),), dtype=torch.bool)
    noise_mask[noise_indices] = 1
    result = torch.LongTensor((n + len(tokens))).fill_((- 1))
    num_random = int(math.ceil((n * self.random_ratio)))
    result[noise_indices[num_random:]] = self.mask_idx
    result[noise_indices[:num_random]] = torch.randint(low=1, high=len(self.vocab), size=(num_random,))
    result[(~ noise_mask)] = tokens
    assert (result >= 0).all()
    return result

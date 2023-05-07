import numpy as np
import torch
import math
from . import data_utils, FairseqDataset


def add_permuted_noise(self, tokens, p):
    num_words = len(tokens)
    num_to_permute = math.ceil((((num_words * 2) * p) / 2.0))
    substitutions = (torch.randperm((num_words - 2))[:num_to_permute] + 1)
    tokens[substitutions] = tokens[substitutions[torch.randperm(num_to_permute)]]
    return tokens

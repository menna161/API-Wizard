import numpy as np
import torch
import math
from . import data_utils, FairseqDataset


def add_rolling_noise(self, tokens):
    offset = np.random.randint(1, (max(1, (tokens.size((- 1)) - 1)) + 1))
    tokens = torch.cat((tokens[0:1], tokens[offset:(- 1)], tokens[1:offset], tokens[(- 1):]), dim=0)
    return tokens

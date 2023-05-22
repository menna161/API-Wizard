import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from scipy.stats import multivariate_normal
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler
from tqdm import trange
from pyodds.algo.algorithm_utils import deepBase, PyTorchUtils
from pyodds.algo.base import Base


def __init__(self, n_features: int, sequence_length: int, hidden_size: int, seed: int, gpu: int):
    super().__init__()
    PyTorchUtils.__init__(self, seed, gpu)
    input_length = (n_features * sequence_length)
    dec_steps = (2 ** np.arange(max(np.ceil(np.log2(hidden_size)), 2), np.log2(input_length))[1:])
    dec_setup = np.concatenate([[hidden_size], dec_steps.repeat(2), [input_length]])
    enc_setup = dec_setup[::(- 1)]
    layers = np.array([[nn.Linear(int(a), int(b)), nn.Tanh()] for (a, b) in enc_setup.reshape((- 1), 2)]).flatten()[:(- 1)]
    self._encoder = nn.Sequential(*layers)
    self.to_device(self._encoder)
    layers = np.array([[nn.Linear(int(a), int(b)), nn.Tanh()] for (a, b) in dec_setup.reshape((- 1), 2)]).flatten()[:(- 1)]
    self._decoder = nn.Sequential(*layers)
    self.to_device(self._decoder)

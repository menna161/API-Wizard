import torch
import torch.nn as nn
import numpy as np
import math
from torch.autograd import Variable
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence


def __init__(self, dim, use_cuda=True):
    "\n        Args\n            dim (int or Tuple) : dimension of the query vector and memory* vectors if int\n                if tuple it should be a tuple (query dim, memory dim, output_dim)\n                *Note I do not condone the usage of this term, it just seems to be unfortunately common, so eh, I'll use it.\n        "
    super(Attention, self).__init__()
    if isinstance(dim, tuple):
        (self.query_dim, self.memory_dim, self.output_dim) = dim
    else:
        self.query_dim = self.memory_dim = self.output_dim = dim
    self.linear_in = nn.Linear(self.query_dim, self.memory_dim, bias=False)
    self.linear_out = nn.Linear((self.query_dim + self.memory_dim), self.output_dim, bias=False)
    self.use_cuda = use_cuda

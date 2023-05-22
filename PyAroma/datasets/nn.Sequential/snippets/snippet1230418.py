import torch
import torch.nn as nn
from torch.nn import functional as F
import math
from utils.tensor import chunk_two, cat_two, sum_except_batch as sumeb
from flows.transform import Transform


def __init__(self, dim_inputs, dim_outputs, dim_context=None):
    super().__init__()
    self.net = nn.Sequential(nn.Linear(dim_inputs, dim_outputs), nn.ELU(), nn.Linear(dim_outputs, dim_outputs))
    if (dim_context > 0):
        self.params_net = nn.Linear(dim_context, dim_outputs, bias=False)

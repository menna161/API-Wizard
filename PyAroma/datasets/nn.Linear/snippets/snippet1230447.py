import torch
import torch.nn as nn
import torch.nn.functional as F
from flows.transform import Transform
from utils.tensor import chunk_two, sum_except_batch as sumeb


def __init__(self, dim_inputs, dim_context=0):
    super().__init__()
    self.init = False
    self.dim_inputs = dim_inputs
    self.log_scale = nn.Parameter(torch.zeros(dim_inputs))
    self.shift = nn.Parameter(torch.zeros(dim_inputs))
    if (dim_context > 0):
        self.linear = nn.Linear(dim_context, (2 * dim_inputs))
        nn.init.uniform_(self.linear.weight, a=(- 0.001), b=0.001)
        nn.init.constant_(self.linear.bias, 0)
    else:
        self.linear = None

import torch
import torch.nn as nn
import torch.nn.functional as F
from utils.tensor import chunk_two, sum_except_batch as sumeb
from flows.transform import Transform, Composite, Inverse
from flows.permutations import Flip, InvertibleLinear


def __init__(self, dim_inputs, dim_outputs, mask):
    super().__init__()
    self.linear = nn.Linear(dim_inputs, dim_outputs)
    self.register_buffer('mask', mask)

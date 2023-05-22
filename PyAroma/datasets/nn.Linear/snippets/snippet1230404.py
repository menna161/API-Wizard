import torch
import torch.nn as nn
import torch.nn.functional as F
from utils.tensor import chunk_two, sum_except_batch as sumeb
from flows.transform import Transform, Composite, Inverse
from flows.permutations import Flip, InvertibleLinear


def __init__(self, dim_inputs, dim_hids, dim_context=0):
    super().__init__()
    self.dim_inputs = dim_inputs
    self.linear = MaskedLinear(dim_inputs, dim_hids, build_mask(dim_inputs, dim_hids, dim_inputs, mask_type='input'))
    self.ctx_linear = (nn.Linear(dim_context, dim_hids, bias=False) if (dim_context > 0) else None)
    self.mlp = nn.Sequential(nn.ELU(), MaskedLinear(dim_hids, dim_hids, build_mask(dim_hids, dim_hids, dim_inputs)), nn.ELU(), MaskedLinear(dim_hids, (2 * dim_inputs), build_mask(dim_hids, (2 * dim_inputs), dim_inputs, mask_type='output')))

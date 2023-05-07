import torch
import torch.nn as nn
from onmt.utils.misc import aeq
from onmt.utils.loss import NMTLossCompute


def __init__(self, input_size, output_size, pad_idx):
    super(CopyGenerator, self).__init__()
    self.linear = nn.Linear(input_size, output_size)
    self.linear_copy = nn.Linear(input_size, 1)
    self.pad_idx = pad_idx

import torch
import torch.nn as nn
import torch.nn.functional as F
from onmt.utils.misc import aeq


def __init__(self, input_size):
    super(ConvMultiStepAttention, self).__init__()
    self.linear_in = nn.Linear(input_size, input_size)
    self.mask = None

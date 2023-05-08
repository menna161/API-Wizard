import torch
import torch.nn as nn
import numpy as np
from hrl4in.utils.networks import AddBias


def __init__(self, num_inputs, num_outputs):
    super().__init__()
    self.linear = nn.Linear(num_inputs, num_outputs)
    nn.init.orthogonal_(self.linear.weight, gain=0.01)
    nn.init.constant_(self.linear.bias, 0.0)

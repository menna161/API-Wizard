import numpy as np
import torch
from torch import nn
from torch.distributions import Independent, Normal
from torch.nn import Parameter, functional as F


def __init__(self, state_size, action_size, hidden_size, discount, state_only=False):
    super().__init__()
    (self.action_size, self.state_only) = (action_size, state_only)
    self.discount = discount
    self.g = nn.Linear((state_size if state_only else (state_size + action_size)), 1)
    self.h = _create_fcnn(state_size, hidden_size, 1, 'tanh')

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal


def __init__(self, num_inputs, hidden_dim):
    super(ValueNetwork, self).__init__()
    self.linear1 = nn.Linear(num_inputs, hidden_dim)
    self.linear2 = nn.Linear(hidden_dim, hidden_dim)
    self.linear3 = nn.Linear(hidden_dim, 1)
    self.apply(weights_init_)

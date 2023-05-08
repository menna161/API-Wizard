import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal


def __init__(self, num_inputs, num_actions, hidden_dim):
    super(QNetwork, self).__init__()
    self.linear1 = nn.Linear((num_inputs + num_actions), hidden_dim)
    self.linear2 = nn.Linear(hidden_dim, hidden_dim)
    self.linear3 = nn.Linear(hidden_dim, 1)
    self.linear4 = nn.Linear((num_inputs + num_actions), hidden_dim)
    self.linear5 = nn.Linear(hidden_dim, hidden_dim)
    self.linear6 = nn.Linear(hidden_dim, 1)
    self.apply(weights_init_)

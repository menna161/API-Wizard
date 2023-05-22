import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Normal


def __init__(self, num_inputs, num_actions, hidden_dim, action_space=None):
    super(DeterministicPolicy, self).__init__()
    self.linear1 = nn.Linear(num_inputs, hidden_dim)
    self.linear2 = nn.Linear(hidden_dim, hidden_dim)
    self.mean = nn.Linear(hidden_dim, num_actions)
    self.noise = torch.Tensor(num_actions)
    self.apply(weights_init_)
    if (action_space is None):
        self.action_scale = 1.0
        self.action_bias = 0.0
    else:
        self.action_scale = torch.FloatTensor(((action_space.high - action_space.low) / 2.0))
        self.action_bias = torch.FloatTensor(((action_space.high + action_space.low) / 2.0))

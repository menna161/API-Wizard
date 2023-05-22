import torch
import torch.nn as nn
import numpy as np
from hrl4in.utils.networks import AddBias


def __init__(self, num_inputs, num_outputs, action_space, squash_mean=False, squash_distribution=False, initial_stddev=(1 / 3.0), min_stddev=0.0, stddev_transform=torch.nn.functional.softplus):
    super().__init__()
    self.fc_mean = nn.Linear(num_inputs, num_outputs)
    self.action_space_mean = torch.nn.Parameter(torch.tensor(((action_space.low + action_space.high) / 2.0), dtype=torch.float), requires_grad=False)
    self.action_space_magnitude = torch.nn.Parameter(torch.tensor(((action_space.high - action_space.low) / 2.0), dtype=torch.float), requires_grad=False)
    self.squash_mean = squash_mean
    self.squash_distribution = squash_distribution
    initial_stddev_before_transform = torch.tensor(initial_stddev, dtype=torch.float)
    if (stddev_transform == torch.exp):
        initial_stddev_before_transform = torch.log(initial_stddev_before_transform)
    elif (stddev_transform == torch.nn.functional.softplus):
        initial_stddev_before_transform = torch.log((torch.exp(initial_stddev_before_transform) - 1.0))
    else:
        assert False, 'unknown stddev transform function'
    self.stddev_before_transform = AddBias((torch.ones(num_outputs) * initial_stddev_before_transform))
    self.stddev_transform = stddev_transform
    min_stddev = (torch.ones(num_outputs) * torch.tensor(min_stddev, dtype=torch.float))
    self.min_stddev = torch.nn.Parameter(min_stddev, requires_grad=False)
    nn.init.orthogonal_(self.fc_mean.weight, gain=0.5)
    nn.init.constant_(self.fc_mean.bias, 0.0)

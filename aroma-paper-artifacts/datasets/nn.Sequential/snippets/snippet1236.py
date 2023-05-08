import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable


def __init__(self, num_actions):
    ' Basic convolutional actor-critic network for Atari 2600 games\n\n        Equivalent to the network in the original DQN paper.\n\n        Args:\n            num_actions (int): the number of available discrete actions\n        '
    super().__init__()
    self.conv = nn.Sequential(nn.Conv2d(4, 32, 8, stride=4), nn.ReLU(inplace=True), nn.Conv2d(32, 64, 4, stride=2), nn.ReLU(inplace=True), nn.Conv2d(64, 64, 3, stride=1), nn.ReLU(inplace=True))
    self.fc = nn.Sequential(nn.Linear(((64 * 7) * 7), 512), nn.ReLU(inplace=True))
    self.pi = nn.Linear(512, num_actions)
    self.v = nn.Linear(512, 1)
    self.num_actions = num_actions
    self.apply(atari_initializer)
    self.pi.weight.data = ortho_weights(self.pi.weight.size(), scale=0.01)
    self.v.weight.data = ortho_weights(self.v.weight.size())

import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import torch.optim as optim
import time
import os
from Env.AtariEnv.atari_wrappers import LazyFrames


def __init__(self, num_actions, device):
    ' Basic convolutional actor-critic network for Atari 2600 games\n\n        Equivalent to the network in the original DQN paper.\n\n        Args:\n            num_actions (int): the number of available discrete actions\n        '
    super().__init__()
    self.conv = nn.Sequential(nn.Conv2d(4, 16, 3, stride=4), nn.ReLU(inplace=True), nn.Conv2d(16, 16, 3, stride=4), nn.ReLU(inplace=True))
    self.fc = nn.Sequential(nn.Linear(((16 * 5) * 5), 64), nn.ReLU(inplace=True))
    self.pi = nn.Linear(64, num_actions)
    self.v = nn.Linear(64, 1)
    self.num_actions = num_actions
    self.device = device

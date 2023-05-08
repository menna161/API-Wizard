import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random
from PIL import Image
import ipdb


def __init__(self, obs_shape, num_actions, lr):
    super(Model, self).__init__()
    self.obs_shape = obs_shape
    self.num_action = num_actions
    self.conv_net = torch.nn.Sequential(nn.BatchNorm2d(3), nn.Conv2d(3, 32, 8, 4), nn.ReLU(), nn.Conv2d(32, 64, 4, 2), nn.ReLU(), nn.Conv2d(64, 64, 3, 1), nn.ReLU())
    self.linear_layer = torch.nn.Sequential(torch.nn.Linear(50176, 256), torch.nn.ReLU(), torch.nn.Linear(256, num_actions))
    self.opt = optim.Adam(self.conv_net.parameters(), lr=lr)
    self.opt2 = optim.Adam(self.linear_layer.parameters(), lr=lr)
    if torch.cuda.is_available():
        print('Using CUDA')
    self.device = torch.device(('cuda:0' if torch.cuda.is_available() else 'cuda:1'))
    self.to(self.device)

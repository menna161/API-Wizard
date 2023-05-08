import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random


def __init__(self, obs_shape, num_actions, lr):
    super(Model, self).__init__()
    assert (len(obs_shape) == 1), 'This network only works on flat observations'
    self.obs_shape = obs_shape
    self.num_action = num_actions
    self.net = torch.nn.Sequential(torch.nn.Linear(obs_shape[0], 32), torch.nn.ReLU(), torch.nn.Linear(32, num_actions))
    self.opt = optim.Adam(self.net.parameters(), lr=lr)
    if torch.cuda.is_available():
        print('Using CUDA')
    self.device = torch.device(('cuda:0' if torch.cuda.is_available() else 'cuda:1'))
    self.to(self.device)

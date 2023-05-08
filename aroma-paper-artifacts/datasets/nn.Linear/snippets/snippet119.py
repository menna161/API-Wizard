import collections
import random
import os
import torch
from torch import nn
from torch.nn import functional as F
import gym
import numpy as np
from skimage.transform import resize
from estorch import ES, VirtualBatchNorm
from mpi4py import MPI


def __init__(self, n_actions, xref):
    super(Policy, self).__init__()
    self.xref = xref
    self.conv1 = nn.Conv2d(4, 16, 8, 4)
    self.bn1 = VirtualBatchNorm(16)
    self.conv2 = nn.Conv2d(16, 32, 4, 2)
    self.bn2 = VirtualBatchNorm(32)
    self.fc1 = nn.Linear(2592, 256)
    self.fc2 = nn.Linear(256, n_actions)

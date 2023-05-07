from __future__ import division
import os
import numpy as np
import torch
from torch import optim
from torch.nn.utils import clip_grad_norm_
import kornia.augmentation as aug
import torch.nn as nn
from model import DQN


def act_e_greedy(self, state, epsilon=0.001):
    return (np.random.randint(0, self.action_space) if (np.random.random() < epsilon) else self.act(state))

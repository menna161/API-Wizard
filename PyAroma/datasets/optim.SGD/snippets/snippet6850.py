import unittest
import torch
import gym
from torch import nn
from torch.nn.functional import smooth_l1_loss
import torch_testing as tt
import numpy as np
from rlil.environments import State, Action
from rlil.approximation import QNetwork, FixedTarget


def optimizer(params):
    return torch.optim.SGD(params, lr=0.1)

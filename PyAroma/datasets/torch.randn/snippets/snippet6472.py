import os
import torch
import numpy as np
from torch.distributions.normal import Normal
from torch.nn.functional import mse_loss
from copy import deepcopy
from rlil.environments import State, action_decorator, Action
from rlil.initializer import get_writer, get_device, get_replay_buffer
from rlil import nn
from .base import Agent, LazyAgent


def __init__(self, qs, encoder, decoder, policy, kernel_type='laplacian', num_samples_match=5, mmd_sigma=10.0, discount_factor=0.99, lambda_q=0.75, _lambda=0.4, delta_conf=0.1, minibatch_size=32):
    self.qs = qs
    self.encoder = encoder
    self.decoder = decoder
    self.policy = policy
    self.replay_buffer = get_replay_buffer()
    self.device = get_device()
    self.writer = get_writer()
    self.kernel_type = kernel_type
    self.mmd_sigma = mmd_sigma
    self.num_samples_match = num_samples_match
    self.minibatch_size = minibatch_size
    self.discount_factor = discount_factor
    self.lambda_q = lambda_q
    self._lambda = _lambda
    self.delta_conf = delta_conf
    self.log_lagrange2 = torch.randn((), requires_grad=True, device=self.device)
    self.lagrange2_opt = torch.optim.Adam([self.log_lagrange2], lr=0.001)
    self._train_count = 0

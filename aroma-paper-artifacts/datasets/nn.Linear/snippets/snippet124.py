import gym
import torch
from estorch import ES


def __init__(self, n_input, n_output):
    super(Policy, self).__init__()
    self.linear_1 = torch.nn.Linear(n_input, 64)
    self.activation_1 = torch.nn.ReLU()
    self.linear_2 = torch.nn.Linear(64, 64)
    self.activation_2 = torch.nn.ReLU()
    self.linear_3 = torch.nn.Linear(64, n_output)

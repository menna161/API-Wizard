import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import warnings


def __init__(self, lr, input_dims, fc1_dims, fc2_dims, n_actions):
    super(DeepQNetwork, self).__init__()
    self.input_dims = (input_dims[0] + n_actions)
    self.fc1_dims = fc1_dims
    self.fc2_dims = fc2_dims
    self.n_actions = 1
    self.fc1 = nn.Linear(self.input_dims, self.fc1_dims)
    self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
    self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)
    self.optimizer = optim.Adam(self.parameters(), lr=lr)
    self.loss = nn.MSELoss()
    if torch.cuda.is_available():
        print('Using CUDA')
    self.device = torch.device(('cuda:0' if torch.cuda.is_available() else 'cuda:1'))
    self.to(self.device)

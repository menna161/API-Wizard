from __future__ import division
import math
import torch
from torch import nn
from torch.nn import functional as F


def __init__(self, args, action_space):
    super(DQN, self).__init__()
    self.atoms = args.atoms
    self.action_space = action_space
    if (args.architecture == 'canonical'):
        self.convs = nn.Sequential(nn.Conv2d(args.history_length, 32, 8, stride=4, padding=0), nn.ReLU(), nn.Conv2d(32, 64, 4, stride=2, padding=0), nn.ReLU(), nn.Conv2d(64, 64, 3, stride=1, padding=0), nn.ReLU())
        self.conv_output_size = 3136
    elif (args.architecture == 'data-efficient'):
        self.convs = nn.Sequential(nn.Conv2d(args.history_length, 32, 5, stride=5, padding=0), nn.ReLU(), nn.Conv2d(32, 64, 5, stride=5, padding=0), nn.ReLU())
        self.conv_output_size = 576
    self.fc_h_v = NoisyLinear(self.conv_output_size, args.hidden_size, std_init=args.noisy_std)
    self.fc_h_a = NoisyLinear(self.conv_output_size, args.hidden_size, std_init=args.noisy_std)
    self.fc_z_v = NoisyLinear(args.hidden_size, self.atoms, std_init=args.noisy_std)
    self.fc_z_a = NoisyLinear(args.hidden_size, (action_space * self.atoms), std_init=args.noisy_std)
    self.W_h = nn.Parameter(torch.rand(self.conv_output_size, args.hidden_size))
    self.W_c = nn.Parameter(torch.rand(args.hidden_size, 128))
    self.b_h = nn.Parameter(torch.zeros(args.hidden_size))
    self.b_c = nn.Parameter(torch.zeros(128))
    self.W = nn.Parameter(torch.rand(128, 128))

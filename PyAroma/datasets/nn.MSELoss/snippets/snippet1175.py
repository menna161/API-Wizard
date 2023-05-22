import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import torch.optim as optim
import time
import os
from Env.AtariEnv.atari_wrappers import LazyFrames


def __init__(self, num_actions, device='cpu', checkpoint_dir=''):
    self.num_actions = num_actions
    self.device = torch.device(device)
    self.checkpoint_dir = checkpoint_dir
    self.model = SmallPolicyAtariCNN(num_actions, self.device)
    if ((checkpoint_dir != '') and os.path.exists(checkpoint_dir)):
        checkpoint = torch.load(checkpoint_dir, map_location='cpu')
    self.model.to(device)
    self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
    self.mseLoss = nn.MSELoss()

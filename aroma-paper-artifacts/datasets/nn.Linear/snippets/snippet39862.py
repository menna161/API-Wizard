import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


def __init__(self, channel_n, fire_rate, device, hidden_size=128):
    super(CAModel, self).__init__()
    self.device = device
    self.channel_n = channel_n
    self.fc0 = nn.Linear((channel_n * 3), hidden_size)
    self.fc1 = nn.Linear(hidden_size, channel_n, bias=False)
    with torch.no_grad():
        self.fc1.weight.zero_()
    self.fire_rate = fire_rate
    self.to(self.device)

import torch
import torch.nn as nn


def __init__(self, out_dim=10, in_channel=1, img_sz=32, hidden_dim=256):
    super(MLP, self).__init__()
    self.in_dim = ((in_channel * img_sz) * img_sz)
    self.linear = nn.Sequential(nn.Linear(self.in_dim, hidden_dim), nn.ReLU(inplace=True), nn.Linear(hidden_dim, hidden_dim), nn.ReLU(inplace=True))
    self.last = nn.Linear(hidden_dim, out_dim)

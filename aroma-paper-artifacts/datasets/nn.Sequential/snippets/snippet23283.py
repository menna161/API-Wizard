import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, gate_channels, reduction_ratio=16, pool_types=['avg', 'max']):
    super(ChannelGate, self).__init__()
    self.gate_channels = gate_channels
    self.mlp = nn.Sequential(Flatten(), nn.Linear(gate_channels, (gate_channels // reduction_ratio)), nn.ReLU(), nn.Linear((gate_channels // reduction_ratio), gate_channels))
    self.pool_types = pool_types

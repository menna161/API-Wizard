import torch.nn as nn
from ppln.utils.freeze import freeze_modules, lock_norm_modules


def __init__(self):
    super().__init__()
    self.layer1 = nn.Sequential(nn.Linear(2, 2), nn.Linear(2, 2), nn.ReLU())
    self.bn = nn.BatchNorm1d(2)

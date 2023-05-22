import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torch.nn.init as init
import numpy as np


def __init__(self):
    super(Discriminator, self).__init__()
    self.conv1 = nn.Conv2d(1, 32, (9, 9))
    self.bn1 = nn.BatchNorm2d(32)
    self.conv2 = nn.Conv2d(32, 64, (5, 5))
    self.bn2 = nn.BatchNorm2d(64)
    self.conv3 = nn.Conv2d(64, 64, (5, 5))
    self.bn3 = nn.BatchNorm2d(64)
    self.fc1 = nn.Linear(((64 * 4) * 4), 512)
    self.fc2 = nn.Linear(512, 64)
    self.fc3 = nn.Linear(64, 1)

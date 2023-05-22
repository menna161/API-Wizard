import argparse
import os
import time
import tinynn as tn
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


def __init__(self):
    super(Conv, self).__init__()
    self.conv1 = nn.Conv2d(1, 6, 5, 1, padding='same')
    self.conv2 = nn.Conv2d(6, 16, 5, 1, padding='same')
    self.fc1 = nn.Linear(784, 120)
    self.fc2 = nn.Linear(120, 84)
    self.fc3 = nn.Linear(84, 10)

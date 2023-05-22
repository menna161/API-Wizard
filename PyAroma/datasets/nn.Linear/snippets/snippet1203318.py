import argparse
import os
import time
import tinynn as tn
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


def __init__(self):
    super(RNN, self).__init__()
    self.recurrent = nn.RNN(28, 30, batch_first=True)
    self.fc1 = nn.Linear(30, 10)

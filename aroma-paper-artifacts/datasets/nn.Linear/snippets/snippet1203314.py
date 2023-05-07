import argparse
import os
import time
import tinynn as tn
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


def __init__(self):
    super(Dense, self).__init__()
    self.fc1 = nn.Linear(784, 200)
    self.fc2 = nn.Linear(200, 100)
    self.fc3 = nn.Linear(100, 70)
    self.fc4 = nn.Linear(70, 30)
    self.fc5 = nn.Linear(30, 10)
    torch.nn.init.xavier_uniform_(self.fc1.weight)
    torch.nn.init.xavier_uniform_(self.fc2.weight)
    torch.nn.init.xavier_uniform_(self.fc3.weight)
    torch.nn.init.xavier_uniform_(self.fc4.weight)
    torch.nn.init.xavier_uniform_(self.fc5.weight)

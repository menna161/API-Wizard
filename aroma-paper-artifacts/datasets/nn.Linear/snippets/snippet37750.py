import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self):
    super(VAE, self).__init__()
    self.fc1 = nn.Linear(784, 400)
    self.fc21 = nn.Linear(400, 20)
    self.fc22 = nn.Linear(400, 20)
    self.fc3 = nn.Linear(20, 400)
    self.fc4 = nn.Linear(400, 784)

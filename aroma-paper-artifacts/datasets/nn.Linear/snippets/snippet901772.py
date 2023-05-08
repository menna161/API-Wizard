from __future__ import print_function
import argparse
import numpy as np
import torch
import torch.nn.functional as F
from torch.autograd import Variable
from torch import nn, optim
from torch.nn import functional as F
from torchvision import datasets, transforms
from torchvision.utils import save_image


def __init__(self, temp):
    super(VAE_gumbel, self).__init__()
    self.fc1 = nn.Linear(784, 512)
    self.fc2 = nn.Linear(512, 256)
    self.fc3 = nn.Linear(256, (latent_dim * categorical_dim))
    self.fc4 = nn.Linear((latent_dim * categorical_dim), 256)
    self.fc5 = nn.Linear(256, 512)
    self.fc6 = nn.Linear(512, 784)
    self.relu = nn.ReLU()
    self.sigmoid = nn.Sigmoid()

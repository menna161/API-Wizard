import torch
import torchvision
from torchvision.datasets import ImageFolder
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import torch.optim as optim
import random


def __init__(self):
    super(Network, self).__init__()
    self.layer1 = nn.Sequential(nn.Conv2d(1, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(kernel_size=2, stride=2))
    self.layer2 = nn.Sequential(nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(kernel_size=2, stride=2))
    self.dropout1 = nn.Dropout(p=0.25)
    self.dropout2 = nn.Dropout(p=0.5)
    self.fc1 = nn.Sequential(nn.Linear(((8 * 8) * 64), 128), nn.ReLU())
    self.fc2 = nn.Linear(128, 10)

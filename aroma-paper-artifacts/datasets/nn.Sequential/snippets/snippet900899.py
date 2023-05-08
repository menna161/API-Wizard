import numpy as np
import torch
import torchvision
import cv2
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms
import christopher as chris


def __init__(self):
    super(Network, self).__init__()
    self.layer1 = nn.Sequential(nn.Conv2d(1, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(kernel_size=2, stride=2))
    self.layer2 = nn.Sequential(nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(kernel_size=2, stride=2))
    self.dropout = nn.Dropout(p=0.4)
    self.fc1 = nn.Sequential(nn.Linear(((8 * 8) * 64), 128), nn.ReLU())
    self.fc2 = nn.Linear(128, 10)

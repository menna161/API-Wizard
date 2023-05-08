import torch
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import argparse
from utils_red_green import gen_box_data, gen_box_data_test


def __init__(self):
    super(Net, self).__init__()
    self.conv1 = nn.Conv2d(3, 32, 3, stride=1, padding=padding_size, bias=False, padding_mode=pad_type)
    self.conv2 = nn.Conv2d(32, 32, 3, stride=2, padding=padding_size, bias=False, padding_mode=pad_type)
    self.conv3 = nn.Conv2d(32, 64, 3, stride=2, padding=padding_size, bias=False, padding_mode=pad_type)
    self.conv4 = nn.Conv2d(64, 64, 3, stride=2, padding=padding_size, bias=False, padding_mode=pad_type)
    self.fc1 = nn.Linear(((64 * 1) * 1), 2)
    self.adap_max = nn.AdaptiveMaxPool2d(1)

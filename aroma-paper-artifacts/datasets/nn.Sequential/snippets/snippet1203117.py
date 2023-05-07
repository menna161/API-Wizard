from __future__ import print_function
import sys
import os
import shutil
import time
import argparse
import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import glob
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as Data
import torchvision
import torchvision.utils as vutils
import torchvision.transforms as transforms
from torch.distributions.one_hot_categorical import OneHotCategorical
import torchvision.datasets as datasets
from torch.autograd import Variable
from torch.utils.serialization import load_lua
from data_loader import Dataset


def __init__(self, model=None):
    super(SmallEncoder4_2, self).__init__()
    self.vgg = nn.Sequential(nn.Conv2d(3, 3, (1, 1)), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(3, 16, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(16, 16, (3, 3)), nn.ReLU(), nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(16, 32, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(32, 32, (3, 3)), nn.ReLU(), nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(32, 64, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(64, 64, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(64, 64, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(64, 64, (3, 3)), nn.ReLU(), nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(64, 128, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(128, 512, (3, 3)), nn.ReLU())
    if model:
        self.load_state_dict(torch.load(model, map_location=(lambda storage, location: storage))['model'])

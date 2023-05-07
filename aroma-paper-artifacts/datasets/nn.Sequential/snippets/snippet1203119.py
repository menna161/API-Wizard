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


def __init__(self, model=None, fixed=False):
    super(SmallEncoder4_16x_plus, self).__init__()
    self.fixed = fixed
    self.vgg = nn.Sequential(nn.Conv2d(3, 3, (1, 1)), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(3, 16, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(16, 16, (3, 3)), nn.ReLU(), nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(16, 32, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(32, 32, (3, 3)), nn.ReLU(), nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(32, 64, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(64, 64, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(64, 64, (3, 3)), nn.ReLU(), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(64, 64, (3, 3)), nn.ReLU(), nn.MaxPool2d((2, 2), (2, 2), (0, 0), ceil_mode=True), nn.ReflectionPad2d((1, 1, 1, 1)), nn.Conv2d(64, 128, (3, 3)), nn.ReLU())
    if model:
        assert (os.path.splitext(model)[1] in {'.t7', '.pth'})
        if model.endswith('.t7'):
            t7_model = load_lua(model)
            load_param(t7_model, 0, self.vgg[0])
            load_param(t7_model, 2, self.vgg[2])
            load_param(t7_model, 5, self.vgg[5])
            load_param(t7_model, 9, self.vgg[9])
            load_param(t7_model, 12, self.vgg[12])
            load_param(t7_model, 16, self.vgg[16])
            load_param(t7_model, 19, self.vgg[19])
            load_param(t7_model, 22, self.vgg[22])
            load_param(t7_model, 25, self.vgg[25])
            load_param(t7_model, 29, self.vgg[29])
        else:
            net = torch.load(model)
            odict_keys = list(net.keys())
            cnt = 0
            i = 0
            for m in self.vgg.children():
                if isinstance(m, nn.Conv2d):
                    print(('layer %s is loaded with trained params' % i))
                    m.weight.data.copy_(net[odict_keys[cnt]])
                    cnt += 1
                    m.bias.data.copy_(net[odict_keys[cnt]])
                    cnt += 1
                i += 1

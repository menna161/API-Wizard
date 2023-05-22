import argparse
import os
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from PIL import Image
from kymatio.torch import Scattering2D as Scattering
from kymatio.caching import get_cache_dir
from ...datasets import get_dataset_dir


def build(self):
    padding = ((self.filter_size - 1) // 2)
    self.main = nn.Sequential(nn.ReflectionPad2d(padding), nn.Conv2d(self.num_input_channels, self.num_hidden_channels, self.filter_size, bias=False), nn.BatchNorm2d(self.num_hidden_channels, eps=0.001, momentum=0.9), nn.ReLU(inplace=True), nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False), nn.ReflectionPad2d(padding), nn.Conv2d(self.num_hidden_channels, self.num_hidden_channels, self.filter_size, bias=False), nn.BatchNorm2d(self.num_hidden_channels, eps=0.001, momentum=0.9), nn.ReLU(inplace=True), nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False), nn.ReflectionPad2d(padding), nn.Conv2d(self.num_hidden_channels, self.num_output_channels, self.filter_size, bias=False), nn.BatchNorm2d(self.num_output_channels, eps=0.001, momentum=0.9), nn.Tanh())

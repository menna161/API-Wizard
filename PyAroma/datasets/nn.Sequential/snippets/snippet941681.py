import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from .vgg import Vgg19
import math
import cv2
import numpy as np
import scipy.stats as st
import code


def __init__(self, in_channels, out_channels, n_feats):
    super(Generator_drop, self).__init__()
    self.conv1 = nn.Sequential(nn.Conv2d(in_channels, 64, 5, 1, 2), nn.ReLU())
    self.conv2 = nn.Sequential(nn.Conv2d(64, 128, 3, 2, 1), nn.ReLU())
    self.conv3 = nn.Sequential(nn.Conv2d(128, 128, 3, 1, 1), nn.ReLU())
    self.conv4 = nn.Sequential(nn.Conv2d(128, 256, 3, 2, 1), nn.ReLU())
    self.conv5 = nn.Sequential(nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU())
    self.conv6 = nn.Sequential(nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU())
    self.diconv1 = nn.Sequential(nn.Conv2d(256, 256, 3, 1, 2, dilation=2), nn.ReLU())
    self.diconv2 = nn.Sequential(nn.Conv2d(256, 256, 3, 1, 4, dilation=4), nn.ReLU())
    self.diconv3 = nn.Sequential(nn.Conv2d(256, 256, 3, 1, 8, dilation=8), nn.ReLU())
    self.diconv4 = nn.Sequential(nn.Conv2d(256, 256, 3, 1, 16, dilation=16), nn.ReLU())
    self.conv7 = nn.Sequential(nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU())
    self.conv_i = nn.Sequential(nn.Conv2d((n_feats * 8), (n_feats * 4), 3, 1, 1), nn.Sigmoid())
    self.conv_f = nn.Sequential(nn.Conv2d((n_feats * 8), (n_feats * 4), 3, 1, 1), nn.Sigmoid())
    self.conv_g = nn.Sequential(nn.Conv2d((n_feats * 8), (n_feats * 4), 3, 1, 1), nn.Tanh())
    self.conv_o = nn.Sequential(nn.Conv2d((n_feats * 8), (n_feats * 4), 3, 1, 1), nn.Sigmoid())
    self.conv8 = nn.Sequential(nn.Conv2d(256, 256, 3, 1, 1), nn.ReLU(True))
    self.deconv1 = nn.Sequential(nn.ConvTranspose2d(256, 128, 4, 2, 1), nn.ReflectionPad2d((1, 0, 1, 0)), nn.AvgPool2d(2, stride=1), nn.ReLU())
    self.conv9 = nn.Sequential(nn.Conv2d(128, 128, 3, 1, 1), nn.ReLU(), nn.Dropout(0.3))
    self.deconv2 = nn.Sequential(nn.ConvTranspose2d(128, 64, 4, 2, 1), nn.ReflectionPad2d((1, 0, 1, 0)), nn.AvgPool2d(2, stride=1), nn.ReLU())
    self.conv10 = nn.Sequential(nn.Conv2d(64, 32, 3, 1, 1), nn.ReLU())
    self.outframe1 = nn.Sequential(nn.Conv2d(256, 3, 3, 1, 1), nn.ReLU())
    self.outframe2 = nn.Sequential(nn.Conv2d(128, 3, 3, 1, 1), nn.ReLU())
    self.output = nn.Sequential(nn.Conv2d(32, out_channels, 3, 1, 1), nn.ReLU())

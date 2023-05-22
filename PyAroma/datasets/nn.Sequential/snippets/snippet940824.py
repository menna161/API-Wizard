import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models
import collections
import math
import sys
import Utils
from Utils.CubePad import CustomPad
from . import resnet
import resnet


def __init__(self):
    super(Refine, self).__init__()
    self.refine_1 = nn.Sequential(nn.Conv2d(5, 32, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(32), nn.ReLU(inplace=True), nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1, bias=False), nn.BatchNorm2d(64), nn.ReLU(inplace=True), nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(64), nn.ReLU(inplace=True))
    self.refine_2 = nn.Sequential(nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1, bias=False), nn.BatchNorm2d(128), nn.ReLU(inplace=True), nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(128), nn.ReLU(inplace=True))
    self.deconv_1 = nn.Sequential(nn.ConvTranspose2d(128, 64, kernel_size=4, stride=2, padding=1, output_padding=0, groups=1, bias=True, dilation=1), nn.BatchNorm2d(64), nn.LeakyReLU(inplace=True))
    self.deconv_2 = nn.Sequential(nn.ConvTranspose2d(192, 32, kernel_size=4, stride=2, padding=1, output_padding=0, groups=1, bias=True, dilation=1), nn.BatchNorm2d(32), nn.LeakyReLU(inplace=True))
    self.refine_3 = nn.Sequential(nn.Conv2d(96, 16, kernel_size=3, stride=1, padding=1, bias=False), nn.BatchNorm2d(16), nn.ReLU(inplace=True), nn.Conv2d(16, 1, kernel_size=3, stride=1, padding=1, bias=False))
    self.bilinear_1 = nn.UpsamplingBilinear2d(size=(256, 512))
    self.bilinear_2 = nn.UpsamplingBilinear2d(size=(512, 1024))

import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import numpy as np
from models_lpf import *
from IPython import embed


def __init__(self, num_classes=1000, filter_size=1, pool_only=False, relu_first=True):
    super(AlexNet, self).__init__()
    if pool_only:
        first_ds = [nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2)]
    elif relu_first:
        first_ds = [nn.Conv2d(3, 64, kernel_size=11, stride=2, padding=2), nn.ReLU(inplace=True), Downsample(filt_size=filter_size, stride=2, channels=64)]
    else:
        first_ds = [nn.Conv2d(3, 64, kernel_size=11, stride=2, padding=2), Downsample(filt_size=filter_size, stride=2, channels=64), nn.ReLU(inplace=True)]
    first_ds += [nn.MaxPool2d(kernel_size=3, stride=1), Downsample(filt_size=filter_size, stride=2, channels=64), nn.Conv2d(64, 192, kernel_size=5, padding=2), nn.ReLU(inplace=True), nn.MaxPool2d(kernel_size=3, stride=1), Downsample(filt_size=filter_size, stride=2, channels=192), nn.Conv2d(192, 384, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.Conv2d(384, 256, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.Conv2d(256, 256, kernel_size=3, padding=1), nn.ReLU(inplace=True), nn.MaxPool2d(kernel_size=3, stride=1), Downsample(filt_size=filter_size, stride=2, channels=256)]
    self.features = nn.Sequential(*first_ds)
    self.avgpool = nn.AdaptiveAvgPool2d((6, 6))
    self.classifier = nn.Sequential(nn.Dropout(), nn.Linear(((256 * 6) * 6), 4096), nn.ReLU(inplace=True), nn.Dropout(), nn.Linear(4096, 4096), nn.ReLU(inplace=True), nn.Linear(4096, num_classes))

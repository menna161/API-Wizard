import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as torch_models
import numpy as np


def __init__(self, input_channel, output_channel):
    super().__init__()
    self.layers = nn.Sequential(nn.Conv2d(input_channel, output_channel, kernel_size=3, padding=1), nn.BatchNorm2d(output_channel))

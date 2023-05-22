import torch
import torch.nn as nn
from unet_parts import *
from torch.autograd import Variable


def __init__(self):
    super(Discriminator, self).__init__()
    self.have_cuda = True
    self.discriminator = nn.Sequential(nn.Conv2d(3, 16, 4, 2, 1, bias=False), nn.ReLU(True), nn.Conv2d(16, 32, 4, 2, 1, bias=False), nn.ReLU(True), nn.Conv2d(32, 64, 4, 2, 1, bias=False), nn.ReLU(True), nn.Conv2d(64, 128, 4, 2, 1, bias=False), nn.ReLU(True))
    self.adv_layer = nn.Sequential(nn.Linear(((128 * 16) * 16), 1), nn.Sigmoid())

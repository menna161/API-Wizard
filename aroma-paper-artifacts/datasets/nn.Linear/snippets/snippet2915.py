import torch
import torch.nn as nn
import torch.utils.data
from torch.nn import functional as F


def __init__(self, input_nc=3, num_classes=1200, img_size=64, **kwargs):
    super(Discriminator, self).__init__()
    self.img_size = img_size
    self.conv1 = ResidualBlockDown(input_nc, 64)
    self.conv2 = ResidualBlockDown(64, 128)
    self.conv3 = ResidualBlockDown(128, 256)
    self.conv4 = ResidualBlockDown(256, 512)
    if (img_size == 128):
        self.conv5 = ResidualBlockDown(512, 512)
    self.dense0 = nn.Linear(8192, 1024)
    self.dense1 = nn.Linear(1024, 1)

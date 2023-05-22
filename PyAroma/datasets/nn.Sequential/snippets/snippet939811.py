import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import Parameter
from collections import OrderedDict


def __init__(self, in_channels=2048, key_channels=512, value_channels=2048, height=224, width=304):
    super(SADecoder, self).__init__()
    out_channels = 512
    self.saconv = SelfAttentionBlock_(in_channels, key_channels, value_channels)
    self.image_context = nn.Sequential(OrderedDict([('avgpool', nn.AvgPool2d(((height // 8), (width // 8)), padding=0)), ('dropout', nn.Dropout2d(0.5, inplace=True)), ('reshape1', Reshape(2048)), ('linear1', nn.Linear(2048, 512)), ('relu1', nn.ReLU(inplace=True)), ('linear2', nn.Linear(512, 512)), ('relu2', nn.ReLU(inplace=True)), ('reshape2', Reshape(512, 1, 1)), ('upsample', nn.Upsample(size=((height // 8), (width // 8)), mode='bilinear', align_corners=True))]))
    self.merge = nn.Sequential(OrderedDict([('dropout1', nn.Dropout2d(0.5, inplace=True)), ('conv1', nn.Conv2d((value_channels + out_channels), value_channels, kernel_size=1, stride=1)), ('relu', nn.ReLU(inplace=True)), ('dropout2', nn.Dropout2d(0.5, inplace=False))]))

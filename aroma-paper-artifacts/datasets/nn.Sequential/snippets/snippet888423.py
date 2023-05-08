import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, ratio=1, class_num=100):
    super().__init__()
    if (ratio == 0.5):
        out_channels = [48, 96, 192, 1024]
    elif (ratio == 1):
        out_channels = [116, 232, 464, 1024]
    elif (ratio == 1.5):
        out_channels = [176, 352, 704, 1024]
    elif (ratio == 2):
        out_channels = [244, 488, 976, 2048]
    else:
        ValueError('unsupported ratio number')
    self.pre = nn.Sequential(nn.Conv2d(3, 24, 3, padding=1), nn.BatchNorm2d(24))
    self.stage2 = self._make_stage(24, out_channels[0], 3)
    self.stage3 = self._make_stage(out_channels[0], out_channels[1], 7)
    self.stage4 = self._make_stage(out_channels[1], out_channels[2], 3)
    self.conv5 = nn.Sequential(nn.Conv2d(out_channels[2], out_channels[3], 1), nn.BatchNorm2d(out_channels[3]), nn.ReLU(inplace=True))
    self.fc = nn.Linear(out_channels[3], class_num)

import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, class_num=100):
    super().__init__()
    self.pre = nn.Sequential(nn.Conv2d(3, 32, 1, padding=1), nn.BatchNorm2d(32), nn.ReLU6(inplace=True))
    self.stage1 = LinearBottleNeck(32, 16, 1, 1)
    self.stage2 = self._make_stage(2, 16, 24, 2, 6)
    self.stage3 = self._make_stage(3, 24, 32, 2, 6)
    self.stage4 = self._make_stage(4, 32, 64, 2, 6)
    self.stage5 = self._make_stage(3, 64, 96, 1, 6)
    self.stage6 = self._make_stage(3, 96, 160, 1, 6)
    self.stage7 = LinearBottleNeck(160, 320, 1, 6)
    self.conv1 = nn.Sequential(nn.Conv2d(320, 1280, 1), nn.BatchNorm2d(1280), nn.ReLU6(inplace=True))
    self.conv2 = nn.Conv2d(1280, class_num, 1)

import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import torch.nn.functional as F


def __init__(self, base_inplanes, base_planes, stride=1, is_downsample=False):
    super(Bottleneck, self).__init__()
    expansion = 4
    max_inp = base_inplanes
    max_oup = base_planes
    max_mid = int((base_planes / expansion))
    self.max_inp = max_inp
    self.max_oup = max_oup
    self.max_mid = max_mid
    self.stride = stride
    self.fc11 = nn.Linear(3, 32)
    self.fc12 = nn.Linear(32, (((max_mid * max_inp) * 1) * 1))
    self.fc21 = nn.Linear(3, 32)
    self.fc22 = nn.Linear(32, (((max_mid * max_mid) * 3) * 3))
    self.fc31 = nn.Linear(3, 32)
    self.fc32 = nn.Linear(32, (((max_oup * max_mid) * 1) * 1))
    self.bn1 = nn.ModuleList()
    for mid_scale in channel_scale:
        mid = int((self.max_mid * mid_scale))
        self.bn1.append(nn.BatchNorm2d(mid, affine=False))
    self.bn2 = nn.ModuleList()
    for mid_scale in channel_scale:
        mid = int((self.max_mid * mid_scale))
        self.bn2.append(nn.BatchNorm2d(mid, affine=False))
    self.bn3 = nn.ModuleList()
    for oup_scale in channel_scale:
        oup = int((self.max_oup * oup_scale))
        self.bn3.append(nn.BatchNorm2d(oup, affine=False))
    self.is_downsample = is_downsample
    if is_downsample:
        self.fc11_downsample = nn.Linear(3, 32)
        self.fc12_downsample = nn.Linear(32, (((max_oup * max_inp) * 1) * 1))
        self.bn_downsample = nn.ModuleList()
        for oup_scale in channel_scale:
            oup = int((self.max_oup * oup_scale))
            self.bn_downsample.append(nn.BatchNorm2d(oup, affine=False))

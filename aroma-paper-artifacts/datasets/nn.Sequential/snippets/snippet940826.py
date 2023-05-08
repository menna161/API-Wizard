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


def __init__(self, layers, decoder, output_size=None, in_channels=3, pretrained=True):
    super(MyModel, self).__init__()
    bs = 1
    self.equi_model = fusion_ResNet(bs, layers, decoder, (512, 1024), 3, pretrained, padding='ZeroPad')
    self.cube_model = fusion_ResNet((bs * 6), layers, decoder, (256, 256), 3, pretrained, padding='SpherePad')
    self.refine_model = Refine()
    if (layers <= 34):
        num_channels = 512
    elif (layers >= 50):
        num_channels = 2048
    self.equi_decoder = choose_decoder(decoder, (num_channels // 2), padding='ZeroPad')
    self.equi_conv3 = nn.Sequential(nn.Conv2d((num_channels // 32), 1, kernel_size=3, stride=1, padding=1, bias=False), nn.UpsamplingBilinear2d(size=(512, 1024)))
    self.cube_decoder = choose_decoder(decoder, (num_channels // 2), padding='SpherePad')
    mypad = getattr(Utils.CubePad, 'SpherePad')
    self.cube_conv3 = nn.Sequential(mypad(1), nn.Conv2d((num_channels // 32), 1, kernel_size=3, stride=1, padding=0, bias=False), nn.UpsamplingBilinear2d(size=(256, 256)))
    self.equi_decoder.apply(weights_init)
    self.equi_conv3.apply(weights_init)
    self.cube_decoder.apply(weights_init)
    self.cube_conv3.apply(weights_init)
    self.ce = CETransform()
    if (layers <= 34):
        ch_lst = [64, 64, 128, 256, 512, 256, 128, 64, 32]
    else:
        ch_lst = [64, 256, 512, 1024, 2048, 1024, 512, 256, 128]
    self.conv_e2c = nn.ModuleList([])
    self.conv_c2e = nn.ModuleList([])
    self.conv_mask = nn.ModuleList([])
    for i in range(9):
        conv_c2e = nn.Sequential(nn.Conv2d(ch_lst[i], ch_lst[i], kernel_size=3, padding=1), nn.ReLU(inplace=True))
        conv_e2c = nn.Sequential(nn.Conv2d(ch_lst[i], ch_lst[i], kernel_size=3, padding=1), nn.ReLU(inplace=True))
        conv_mask = nn.Sequential(nn.Conv2d((ch_lst[i] * 2), 1, kernel_size=1, padding=0), nn.Sigmoid())
        self.conv_e2c.append(conv_e2c)
        self.conv_c2e.append(conv_c2e)
        self.conv_mask.append(conv_mask)
    self.grid = Utils.Equirec2Cube(None, 512, 1024, 256, 90).GetGrid()
    self.d2p = Utils.Depth2Points(self.grid)

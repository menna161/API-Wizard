import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, PackedSequence
import math
from lib.pytorch_convolutional_rnn import convolutional_rnn
import numpy as np


def __init__(self, block=Bottleneck, layers_scene=[3, 4, 6, 3, 2], layers_face=[3, 4, 6, 3, 2]):
    self.inplanes_scene = 64
    self.inplanes_face = 64
    super(ModelSpatial, self).__init__()
    self.relu = nn.ReLU(inplace=True)
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
    self.avgpool = nn.AvgPool2d(7, stride=1)
    self.conv1_scene = nn.Conv2d(4, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1_scene = nn.BatchNorm2d(64)
    self.layer1_scene = self._make_layer_scene(block, 64, layers_scene[0])
    self.layer2_scene = self._make_layer_scene(block, 128, layers_scene[1], stride=2)
    self.layer3_scene = self._make_layer_scene(block, 256, layers_scene[2], stride=2)
    self.layer4_scene = self._make_layer_scene(block, 512, layers_scene[3], stride=2)
    self.layer5_scene = self._make_layer_scene(block, 256, layers_scene[4], stride=1)
    self.conv1_face = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
    self.bn1_face = nn.BatchNorm2d(64)
    self.layer1_face = self._make_layer_face(block, 64, layers_face[0])
    self.layer2_face = self._make_layer_face(block, 128, layers_face[1], stride=2)
    self.layer3_face = self._make_layer_face(block, 256, layers_face[2], stride=2)
    self.layer4_face = self._make_layer_face(block, 512, layers_face[3], stride=2)
    self.layer5_face = self._make_layer_face(block, 256, layers_face[4], stride=1)
    self.attn = nn.Linear(1808, ((1 * 7) * 7))
    self.compress_conv1 = nn.Conv2d(2048, 1024, kernel_size=1, stride=1, padding=0, bias=False)
    self.compress_bn1 = nn.BatchNorm2d(1024)
    self.compress_conv2 = nn.Conv2d(1024, 512, kernel_size=1, stride=1, padding=0, bias=False)
    self.compress_bn2 = nn.BatchNorm2d(512)
    self.compress_conv1_inout = nn.Conv2d(2048, 512, kernel_size=1, stride=1, padding=0, bias=False)
    self.compress_bn1_inout = nn.BatchNorm2d(512)
    self.compress_conv2_inout = nn.Conv2d(512, 1, kernel_size=1, stride=1, padding=0, bias=False)
    self.compress_bn2_inout = nn.BatchNorm2d(1)
    self.fc_inout = nn.Linear(49, 1)
    self.deconv1 = nn.ConvTranspose2d(512, 256, kernel_size=3, stride=2)
    self.deconv_bn1 = nn.BatchNorm2d(256)
    self.deconv2 = nn.ConvTranspose2d(256, 128, kernel_size=3, stride=2)
    self.deconv_bn2 = nn.BatchNorm2d(128)
    self.deconv3 = nn.ConvTranspose2d(128, 1, kernel_size=4, stride=2)
    self.deconv_bn3 = nn.BatchNorm2d(1)
    self.conv4 = nn.Conv2d(1, 1, kernel_size=1, stride=1)
    for m in self.modules():
        if (isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d)):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()

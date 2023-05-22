from __future__ import division, print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from data import widerface_640
import os
import pdb
import torchvision
import time
from layers import *


def __init__(self, phase, size, num_classes):
    super(SSD, self).__init__()
    self.phase = phase
    self.num_classes = num_classes
    assert (num_classes == 2)
    self.cfg = cfg
    self.size = size
    if (backbone in ['facebox']):
        self.conv1 = CRelu(3, 32, kernel_size=7, stride=4, padding=3)
        self.conv3 = CRelu(64, 64, kernel_size=5, stride=2, padding=2)
        self.inception1 = Inception2d(64)
        self.inception2 = Inception2d(64)
        self.inception3 = Inception2d(128)
        self.inception4 = Inception2d(128)
        self.conv5_1 = BasicConv2d(128, 128, kernel_size=1, stride=1, padding=0)
        self.conv5_2 = BasicConv2d(128, 256, kernel_size=3, stride=2, padding=1)
        self.conv6_1 = BasicConv2d(256, 128, kernel_size=1, stride=1, padding=0)
        self.conv6_2 = BasicConv2d(128, 256, kernel_size=3, stride=2, padding=1)
        fpn_in = [64, 64, 128, 128, 256, 256]
        cpm_in = [64, 64, 64, 64, 64, 64]
        fpn_channel = 64
        cpm_channels = 64
        output_channels = cpm_in
    elif (backbone in ['mobilenet']):
        self.base = nn.ModuleList(MobileNet())
        self.layer1 = nn.Sequential(*[self.base[i] for i in range(0, 4)])
        self.layer2 = nn.Sequential(*[self.base[i] for i in range(4, 6)])
        self.layer3 = nn.Sequential(*[self.base[i] for i in range(6, 12)])
        self.layer4 = nn.Sequential(*[self.base[i] for i in range(12, 14)])
        self.layer5 = nn.Sequential(*[BasicConv(1024, 256, kernel_size=1, stride=1), BasicConv(256, 512, kernel_size=3, stride=2, padding=1)])
        self.layer6 = nn.Sequential(*[BasicConv(512, 128, kernel_size=1, stride=1), BasicConv(128, 256, kernel_size=3, stride=2, padding=1)])
        fpn_in = [128, 256, 512, 1024, 512, 256]
        cpm_in = [128, 128, 128, 128, 128, 128]
        output_channels = [128, 128, 128, 128, 128, 128]
        fpn_channel = 128
        cpm_channels = 128
    elif (backbone in ['resnet18']):
        resnet = torchvision.models.resnet18(pretrained=True)
        self.layer1 = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu, resnet.maxpool, resnet.layer1)
        self.layer2 = nn.Sequential(resnet.layer2)
        self.layer3 = nn.Sequential(resnet.layer3)
        self.layer4 = nn.Sequential(resnet.layer4)
        self.layer5 = nn.Sequential(*[BasicConv(512, 128, kernel_size=1, stride=1), BasicConv(128, 256, kernel_size=3, stride=2, padding=1)])
        self.layer6 = nn.Sequential(*[BasicConv(256, 64, kernel_size=1, stride=1), BasicConv(64, 128, kernel_size=3, stride=2, padding=1)])
        fpn_in = [64, 128, 256, 512, 256, 128]
        cpm_in = [128, 128, 128, 128, 128, 128]
        output_channels = [64, 128, 256, 512, 256, 128]
        fpn_channel = 128
        cpm_channels = 128
    if fpn:
        self.smooth3 = nn.Conv2d(fpn_channel, fpn_channel, kernel_size=1, stride=1, padding=0)
        self.smooth2 = nn.Conv2d(fpn_channel, fpn_channel, kernel_size=1, stride=1, padding=0)
        self.smooth1 = nn.Conv2d(fpn_channel, fpn_channel, kernel_size=1, stride=1, padding=0)
        self.latlayer6 = nn.Conv2d(fpn_in[5], fpn_channel, kernel_size=1, stride=1, padding=0)
        self.latlayer5 = nn.Conv2d(fpn_in[4], fpn_channel, kernel_size=1, stride=1, padding=0)
        self.latlayer4 = nn.Conv2d(fpn_in[3], fpn_channel, kernel_size=1, stride=1, padding=0)
        self.latlayer3 = nn.Conv2d(fpn_in[2], fpn_channel, kernel_size=1, stride=1, padding=0)
        self.latlayer2 = nn.Conv2d(fpn_in[1], fpn_channel, kernel_size=1, stride=1, padding=0)
        self.latlayer1 = nn.Conv2d(fpn_in[0], fpn_channel, kernel_size=1, stride=1, padding=0)
    if cpm:
        self.cpm1 = Inception2d(cpm_in[0])
        self.cpm2 = Inception2d(cpm_in[1])
        self.cpm3 = Inception2d(cpm_in[2])
        self.cpm4 = Inception2d(cpm_in[3])
        self.cpm5 = Inception2d(cpm_in[4])
        self.cpm6 = Inception2d(cpm_in[5])
    if pa:
        face_head = face_multibox(output_channels, cfg['mbox'], num_classes, cpm_channels)
        self.loc = nn.ModuleList(face_head[0])
        self.conf = nn.ModuleList(face_head[1])
        if (phase == 'train'):
            pa_head = pa_multibox(output_channels, cfg['mbox'], num_classes, cpm_channels)
            self.pa_loc = nn.ModuleList(pa_head[0])
            self.pa_conf = nn.ModuleList(pa_head[1])
    else:
        head = multibox(output_channels, cfg['mbox'], num_classes)
        self.loc = nn.ModuleList(head[0])
        self.conf = nn.ModuleList(head[1])
    if refine:
        arm_head = arm_multibox(output_channels, cfg['mbox'], num_classes)
        self.arm_loc = nn.ModuleList(arm_head[0])
        self.arm_conf = nn.ModuleList(arm_head[1])
    if (phase == 'test'):
        self.softmax = nn.Softmax(dim=(- 1))
        self.detect = Detect(num_classes, 0, cfg['num_thresh'], cfg['conf_thresh'], cfg['nms_thresh'])
    if (phase == 'train'):
        print('init weight!')
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.xavier_normal(m.weight.data)
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

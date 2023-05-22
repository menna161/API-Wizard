from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from model.utils.config import cfg
from model.fpn.fpn import _FPN
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math
import torch.utils.model_zoo as model_zoo
import pdb


def _init_modules(self):
    resnet = resnet101()
    if (self.pretrained == True):
        print(('Loading pretrained weights from %s' % self.model_path))
        state_dict = torch.load(self.model_path)
        resnet.load_state_dict({k: v for (k, v) in state_dict.items() if (k in resnet.state_dict())})
    self.RCNN_layer0 = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu, resnet.maxpool)
    self.RCNN_layer1 = nn.Sequential(resnet.layer1)
    self.RCNN_layer2 = nn.Sequential(resnet.layer2)
    self.RCNN_layer3 = nn.Sequential(resnet.layer3)
    self.RCNN_layer4 = nn.Sequential(resnet.layer4)
    self.RCNN_toplayer = nn.Conv2d(2048, 256, kernel_size=1, stride=1, padding=0)
    self.RCNN_smooth1 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
    self.RCNN_smooth2 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
    self.RCNN_smooth3 = nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1)
    self.RCNN_latlayer1 = nn.Conv2d(1024, 256, kernel_size=1, stride=1, padding=0)
    self.RCNN_latlayer2 = nn.Conv2d(512, 256, kernel_size=1, stride=1, padding=0)
    self.RCNN_latlayer3 = nn.Conv2d(256, 256, kernel_size=1, stride=1, padding=0)
    self.RCNN_roi_feat_ds = nn.Conv2d(256, 256, kernel_size=3, stride=2, padding=1)
    self.RCNN_altitude = nn.Sequential(nn.Conv2d(256, 1024, kernel_size=cfg.POOLING_SIZE, stride=cfg.POOLING_SIZE, padding=0), nn.ReLU(True), nn.Conv2d(1024, 1024, kernel_size=1, stride=1, padding=0), nn.ReLU(True))
    self.RCNN_altitude_score = nn.Linear(1024, 2)
    self.RCNN_angle = nn.Sequential(nn.Conv2d(256, 1024, kernel_size=cfg.POOLING_SIZE, stride=cfg.POOLING_SIZE, padding=0), nn.ReLU(True), nn.Conv2d(1024, 1024, kernel_size=1, stride=1, padding=0), nn.ReLU(True))
    self.RCNN_angle_score = nn.Linear(1024, 2)
    self.RCNN_weather = nn.Sequential(nn.Conv2d(256, 1024, kernel_size=cfg.POOLING_SIZE, stride=cfg.POOLING_SIZE, padding=0), nn.ReLU(True), nn.Conv2d(1024, 1024, kernel_size=1, stride=1, padding=0), nn.ReLU(True))
    self.RCNN_weather_score = nn.Linear(1024, 2)
    self.RCNN_top = nn.Sequential(nn.Conv2d(256, 1024, kernel_size=cfg.POOLING_SIZE, stride=cfg.POOLING_SIZE, padding=0), nn.ReLU(True), nn.Conv2d(1024, 1024, kernel_size=1, stride=1, padding=0), nn.ReLU(True))
    self.RCNN_cls_score = nn.Linear(1024, self.n_classes)
    if self.class_agnostic:
        self.RCNN_bbox_pred = nn.Linear(1024, 4)
    else:
        self.RCNN_bbox_pred = nn.Linear(1024, (4 * self.n_classes))
    for p in self.RCNN_layer0[0].parameters():
        p.requires_grad = False
    for p in self.RCNN_layer0[1].parameters():
        p.requires_grad = False
    assert (0 <= cfg.RESNET.FIXED_BLOCKS < 4)
    if (cfg.RESNET.FIXED_BLOCKS >= 3):
        for p in self.RCNN_layer3.parameters():
            p.requires_grad = False
    if (cfg.RESNET.FIXED_BLOCKS >= 2):
        for p in self.RCNN_layer2.parameters():
            p.requires_grad = False
    if (cfg.RESNET.FIXED_BLOCKS >= 1):
        for p in self.RCNN_layer1.parameters():
            p.requires_grad = False

    def set_bn_fix(m):
        classname = m.__class__.__name__
        if (classname.find('BatchNorm') != (- 1)):
            for p in m.parameters():
                p.requires_grad = False
    self.RCNN_layer0.apply(set_bn_fix)
    self.RCNN_layer1.apply(set_bn_fix)
    self.RCNN_layer2.apply(set_bn_fix)
    self.RCNN_layer3.apply(set_bn_fix)
    self.RCNN_layer4.apply(set_bn_fix)

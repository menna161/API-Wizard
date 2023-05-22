from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from model.utils.config import cfg
from model.faster_rcnn.faster_rcnn import _fasterRCNN
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
    self.RCNN_base = nn.Sequential(resnet.conv1, resnet.bn1, resnet.relu, resnet.maxpool, resnet.layer1, resnet.layer2, resnet.layer3)
    self.RCNN_top = nn.Sequential(resnet.layer4)
    self.RCNN_altitude = nn.Sequential(self._make_layer(Bottleneck, 512, 3, stride=2))
    self.RCNN_altitude_score = nn.Linear(2048, 3)
    self.inplanes = 1024
    self.RCNN_angle = nn.Sequential(self._make_layer(Bottleneck, 512, 3, stride=2))
    self.RCNN_angle_score = nn.Linear(2048, 3)
    self.inplanes = 1024
    self.RCNN_weather = nn.Sequential(self._make_layer(Bottleneck, 512, 3, stride=2))
    self.RCNN_weather_score = nn.Linear(2048, 2)
    self.RCNN_cls_score = nn.Linear(2048, self.n_classes)
    if self.class_agnostic:
        self.RCNN_bbox_pred = nn.Linear(2048, 4)
    else:
        self.RCNN_bbox_pred = nn.Linear(2048, (4 * self.n_classes))
    for p in self.RCNN_base[0].parameters():
        p.requires_grad = False
    for p in self.RCNN_base[1].parameters():
        p.requires_grad = False
    assert (0 <= cfg.RESNET.FIXED_BLOCKS < 4)
    if (cfg.RESNET.FIXED_BLOCKS >= 3):
        for p in self.RCNN_base[6].parameters():
            p.requires_grad = False
    if (cfg.RESNET.FIXED_BLOCKS >= 2):
        for p in self.RCNN_base[5].parameters():
            p.requires_grad = False
    if (cfg.RESNET.FIXED_BLOCKS >= 1):
        for p in self.RCNN_base[4].parameters():
            p.requires_grad = False

    def set_bn_fix(m):
        classname = m.__class__.__name__
        if (classname.find('BatchNorm') != (- 1)):
            for p in m.parameters():
                p.requires_grad = False
    self.RCNN_base.apply(set_bn_fix)
    self.RCNN_top.apply(set_bn_fix)

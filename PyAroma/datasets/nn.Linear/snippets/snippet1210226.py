from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import math
import torchvision.models as models
from model.faster_rcnn.faster_rcnn import _fasterRCNN
import pdb


def _init_modules(self):
    vgg = models.vgg16()
    if self.pretrained:
        print(('Loading pretrained weights from %s' % self.model_path))
        state_dict = torch.load(self.model_path)
        vgg.load_state_dict({k: v for (k, v) in state_dict.items() if (k in vgg.state_dict())})
    vgg.classifier = nn.Sequential(*list(vgg.classifier._modules.values())[:(- 1)])
    self.RCNN_base = nn.Sequential(*list(vgg.features._modules.values())[:(- 1)])
    for layer in range(10):
        for p in self.RCNN_base[layer].parameters():
            p.requires_grad = False
    self.RCNN_top = vgg.classifier
    self.RCNN_cls_score = nn.Linear(4096, self.n_classes)
    if self.class_agnostic:
        self.RCNN_bbox_pred = nn.Linear(4096, 4)
    else:
        self.RCNN_bbox_pred = nn.Linear(4096, (4 * self.n_classes))

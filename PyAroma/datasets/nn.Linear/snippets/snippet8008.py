import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn


def __init__(self, pretrained, id_num_classes, color_num_classes, type_num_classes):
    super(ResNet50AttrBackbone, self).__init__()
    self.model = resnet50(**{'pretrained': pretrained})
    del self.model.fc
    self.fc1 = nn.Linear(2048, 2048)
    self.feat_bn = nn.BatchNorm1d(2048)
    self.feat_bn.bias.requires_grad_(False)
    self.id_fc = nn.Linear(2048, 1024)
    self.color_fc = nn.Linear(2048, 512)
    self.type_fc = nn.Linear(2048, 512)
    self.combine_fc = nn.Linear(2048, 2048)
    self.id_pred_fc = nn.Linear(2048, id_num_classes)
    self.color_pred_fc = nn.Linear(512, color_num_classes)
    self.type_pred_fc = nn.Linear(512, type_num_classes)

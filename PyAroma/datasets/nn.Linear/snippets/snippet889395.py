import torch
import torch.nn as nn
import ResNet
import lmmd


def __init__(self, num_classes=31, bottle_neck=True):
    super(DSAN, self).__init__()
    self.feature_layers = ResNet.resnet50(True)
    self.lmmd_loss = lmmd.LMMD_loss(class_num=num_classes)
    self.bottle_neck = bottle_neck
    if bottle_neck:
        self.bottle = nn.Linear(2048, 256)
        self.cls_fc = nn.Linear(256, num_classes)
    else:
        self.cls_fc = nn.Linear(2048, num_classes)
import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import mmd
import torch


def __init__(self, num_classes=31):
    super(DANNet, self).__init__()
    self.sharedNet = resnet50(True)
    self.cls_fc = nn.Linear(2048, num_classes)

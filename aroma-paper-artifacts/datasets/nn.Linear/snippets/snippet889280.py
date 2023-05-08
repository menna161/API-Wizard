import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import mmd
import torch.nn.functional as F
from torch.autograd import Variable
import torch


def __init__(self, num_classes=31):
    super(MFSAN, self).__init__()
    self.sharedNet = resnet50(True)
    self.sonnet1 = ADDneck(2048, 256)
    self.sonnet2 = ADDneck(2048, 256)
    self.cls_fc_son1 = nn.Linear(256, num_classes)
    self.cls_fc_son2 = nn.Linear(256, num_classes)
    self.avgpool = nn.AvgPool2d(7, stride=1)

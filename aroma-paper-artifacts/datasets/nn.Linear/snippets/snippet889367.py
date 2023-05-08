import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import torch
from torch.autograd import Function


def __init__(self, num_classes=31):
    super(RevGrad, self).__init__()
    self.sharedNet = resnet50(False)
    self.cls_fc = nn.Linear(2048, num_classes)
    self.domain_fc = nn.Linear(2048, 2)

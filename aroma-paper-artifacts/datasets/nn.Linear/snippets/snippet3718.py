import numpy as np
from numpy import linalg as la
import math
import logging
import json
import torch
from torch import nn
from torch.nn import init
import torch.nn.functional as F
from torch.autograd import Variable
import nn as mynn
from core.config import cfg
from modeling_rel.sparse_targets_rel import FrequencyBias
from modeling_rel.draw_rectangles.draw_rectangles import draw_union_boxes


def _init_weights(self):
    for m in self.modules():
        if (isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear)):
            mynn.init.XavierFill(m.weight)
            if (m.bias is not None):
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)

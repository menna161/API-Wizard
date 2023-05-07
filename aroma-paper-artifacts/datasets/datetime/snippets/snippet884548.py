from __future__ import division
import datetime
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from utils.parse_config import *
from utils.utils import build_targets, to_cpu, non_max_suppression
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import datetime
from torch2trt import torch2trt


def forward(self, backbone_out):
    print('forwarding...........')
    prevtime = time.time()
    if (len(self.yolo_layer) == 2):
        (x1, loss1) = self.yolo_layer[0](backbone_out[0], targets=None, img_dim=self.img_size)
        (x2, loss2) = self.yolo_layer[1](backbone_out[1], targets=None, img_dim=self.img_size)
        yolo_out = to_cpu(torch.cat((x1, x2), 1))
        print(('\t+ forward:Time:%s' % datetime.timedelta(seconds=(time.time() - prevtime))))
        return yolo_out
    else:
        start = time.time()
        (x1, loss1) = self.yolo_layer[0](backbone_out[0], targets=None, img_dim=self.img_size)
        print(('\t+ loss1 Time: %s' % str((time.time() - start))))
        start = time.time()
        (x2, loss2) = self.yolo_layer[1](backbone_out[1], targets=None, img_dim=self.img_size)
        print(('\t+ loss2 Time: %s' % str((time.time() - start))))
        start = time.time()
        (x3, loss3) = self.yolo_layer[2](backbone_out[2], targets=None, img_dim=self.img_size)
        print(('\t+ loss3 Time: %s' % str((time.time() - start))))
        start = time.time()
        yolo_out = to_cpu(torch.cat((x1, x2, x3), 1))
        print(('\t+ to_cpu Time: %s' % str((time.time() - start))))
        print(('\t+ forward:Time:%s' % datetime.timedelta(seconds=(time.time() - prevtime))))
        return yolo_out

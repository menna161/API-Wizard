import torch.nn as nn
from mmcv.cnn.weight_init import normal_init, xavier_init
from mmdet.ops import ConvModule
from ..backbones.resnet import Bottleneck
from ..registry import HEADS
from .bbox_head import BBoxHead


def init_weights(self):
    normal_init(self.fc_cls, std=0.01)
    normal_init(self.fc_reg, std=0.001)
    for m in self.fc_branch.modules():
        if isinstance(m, nn.Linear):
            xavier_init(m, distribution='uniform')
